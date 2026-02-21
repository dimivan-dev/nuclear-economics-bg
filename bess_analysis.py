#!/usr/bin/env python3
"""
Market Impact Analysis of 15 GWh BESS Integration – Bulgaria DAM
=================================================================
Implements:
  A. Merit Order Proxy (piecewise linear price-elasticity model)
  B. Daily LP Arbitrage Optimizer (scipy.optimize.linprog) with export arbitrage
  C. Cannibalization & Saturation Module (2 GWh increments)
  D. KPI Report (price delta, renewable integration, cross-border, cycles)
  E. Structural Price Convergence – models the "missing money" equilibrium where
     BESS kills the peak premium, coal/gas can no longer recover fixed costs as
     overnight baseload, and prices re-anchor at coal/gas full-cost recovery.

Scenario parameters (all overridable via CLI):
  --year          primary analysis year            (default: 2025)
  --solar-addon   additional solar MW to install   (default: 2000)
  --solar-base    current installed solar MW       (default: 5300)
  --coal-dereg    coal MW leaving regulated market (default: 600)
  --coal-vc       coal variable + fixed cost floor (default: 88 EUR/MWh)
  --gas-vc        gas variable + fixed cost floor  (default: 120 EUR/MWh)
  --export        enable cross-border export arb   (flag)
  --structural    use structural equilibrium prices (flag)
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import linprog
from scipy.stats import linregress

# ──────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ──────────────────────────────────────────────────────────────────────────────

DATA_DIR     = Path('./data')
RAW_DATA_DIR = Path('./raw_data')
YEARS_FOR_SWEEP = [2023, 2024, 2025]

BESS_CAPACITY_MWH = 15_000
BESS_POWER_MW     = 3_750
ROUNDTRIP_EFF     = 0.875
CHARGE_EFF        = ROUNDTRIP_EFF ** 0.5
DISCHARGE_EFF     = ROUNDTRIP_EFF ** 0.5

# Cost of one full cycle (degradation + efficiency loss), EUR/MWh cycled
CYCLE_DEGRADATION_COST_EUR_PER_MWH = 10.0

# Bulgarian supply stack defaults (2025 calibration)
COAL_CAPACITY_MW      = 2_000   # total coal / lignite installed (MW)
GAS_CAPACITY_MW       = 1_200   # gas turbines + imports baseload (MW)
COAL_VC_EUR_MWH       = 88.0    # coal full-cost floor (from data: ~86 EUR/MWh when coal is marginal)
GAS_VC_EUR_MWH        = 120.0   # gas/CCGT full-cost floor

# Export interconnector capacities (MW) from meta
MAX_EXPORT = {'ro': 1_891, 'gr': 886, 'tr': 490}
MAX_IMPORT = {'ro': 1_891, 'gr': 886, 'tr': 490}   # symmetric assumption

# ──────────────────────────────────────────────────────────────────────────────
# DATA LOADING
# ──────────────────────────────────────────────────────────────────────────────

def load_year(year: int) -> pd.DataFrame:
    """Load preprocessed hourly data for a given year into a DataFrame."""
    path = DATA_DIR / f'{year}.json'
    if not path.exists():
        raise FileNotFoundError(f'Missing preprocessed data: {path}')
    with open(path) as f:
        raw = json.load(f)
    df = pd.DataFrame(raw['hours'])
    df['t'] = pd.to_datetime(df['t'], utc=True)
    df = df.set_index('t').sort_index()
    # Unpack flows dict into separate columns
    flows_df = pd.json_normalize(df['flows'].tolist())
    flows_df.index = df.index
    for c in ['ro', 'tr', 'gr']:
        df[f'flow_{c}'] = flows_df.get(c, 0)
    df.drop(columns=['flows'], inplace=True)
    # Cast numeric columns, coerce bad values to NaN
    numeric_cols = ['demand', 'gen', 'net', 'price',
                    'nuclear', 'coal', 'gas', 'hydro', 'solar', 'wind', 'biomass',
                    'flow_ro', 'flow_tr', 'flow_gr']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df


def load_years(years: list[int]) -> pd.DataFrame:
    frames = []
    for y in years:
        try:
            frames.append(load_year(y))
        except FileNotFoundError as e:
            print(f'  WARNING: {e}')
    return pd.concat(frames).sort_index()


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Keep only rows with valid price and positive demand/generation."""
    mask = (
        df['price'].notna() &
        df['demand'].notna() &
        (df['demand'] > 100) &
        (df['gen'] > 0) &
        (df['price'] > -200)
    )
    return df[mask].copy()


# ──────────────────────────────────────────────────────────────────────────────
# SCENARIO ADJUSTMENTS
# ──────────────────────────────────────────────────────────────────────────────

def scale_solar(df: pd.DataFrame, addon_mw: float, base_installed_mw: float) -> pd.DataFrame:
    """
    Scale solar generation to reflect additional installed capacity.

    Uses the generation-to-installed ratio from the base data to derive
    the proportional increase.  Daytime generation scales linearly with
    capacity; nighttime stays at zero.
    """
    if addon_mw <= 0:
        return df
    df = df.copy()
    factor = (base_installed_mw + addon_mw) / base_installed_mw
    df['solar'] = df['solar'] * factor
    return df


def load_neighbor_prices(year: int) -> dict[str, pd.Series]:
    """
    Parse raw ENTSOE JSON for RO and GR and return hourly price Series,
    indexed by UTC timestamp.
    """
    def _parse(path: Path) -> pd.Series:
        if not path.exists():
            return pd.Series(dtype=float)
        with open(path) as f:
            raw = json.load(f)
        result: dict[str, float] = {}
        ts_list = raw.get('prices', {}).get('TimeSeries', [])
        if isinstance(ts_list, dict):
            ts_list = [ts_list]
        for ts in ts_list:
            periods = ts.get('Period', [])
            if isinstance(periods, dict):
                periods = [periods]
            for period in periods:
                si = period.get('timeInterval', {}).get('start', {})
                start_str = si.get('text', '') if isinstance(si, dict) else si
                if not start_str:
                    continue
                start_dt = datetime.fromisoformat(start_str.replace('Z', '+00:00'))
                pts = period.get('Point', [])
                if isinstance(pts, dict):
                    pts = [pts]
                for pt in pts:
                    pos_raw = pt.get('position', 0)
                    pos = int(pos_raw.get('text', 0) if isinstance(pos_raw, dict) else pos_raw)
                    val = pt.get('price.amount') or (pt.get('price', {}) or {}).get('amount')
                    if val is None:
                        continue
                    v = float(val.get('text', val) if isinstance(val, dict) else val)
                    t = start_dt + timedelta(hours=pos - 1)
                    result[t.strftime('%Y-%m-%dT%H:%MZ')] = v
        s = pd.Series(result)
        s.index = pd.to_datetime(s.index, utc=True)
        return s.sort_index()

    out: dict[str, pd.Series] = {}
    for country in ('RO', 'GR'):
        path = RAW_DATA_DIR / country / f'{year}.json'
        out[country.lower()] = _parse(path)
        if len(out[country.lower()]):
            print(f'  Loaded {country} {year} prices: {len(out[country.lower()])} hours')
        else:
            print(f'  WARNING: no {country} price data for {year}')
    return out


def compute_structural_prices(
    df: pd.DataFrame,
    coal_vc: float = COAL_VC_EUR_MWH,
    gas_vc: float = GAS_VC_EUR_MWH,
    coal_capacity_mw: float = COAL_CAPACITY_MW,
    coal_deregulated_mw: float = 600.0,
    gas_capacity_mw: float = GAS_CAPACITY_MW,
    bess_peak_coverage_fraction: float = 0.0,
) -> pd.Series:
    """
    Compute structural equilibrium prices for a future scenario where:

      1. BESS + extra solar flatten peak premiums (coal/gas can no longer
         recover fixed costs purely from overnight baseload).
      2. Coal/gas only run when the residual load exceeds their economic
         threshold; otherwise they back off and prices rise to their
         FULL COST RECOVERY level (not just variable cost).
      3. The peak premium (scarcity above gas_vc) erodes proportionally
         to how often BESS covers peak demand.

    Price formation by residual load band:
      L_res < 0              →  curtailment pricing (0 to negative)
      0  – 300               →  hydro / must-run biomass (≈10 EUR/MWh)
      300 – coal_regulated   →  regulated coal at coal_vc (linear)
      coal_regulated –       →  deregulated coal bids at coal_vc (step)
        coal_total
      coal_total –           →  gas at gas_vc (step)
        coal+gas
      > coal+gas             →  scarcity, but eroded by BESS coverage

    bess_peak_coverage_fraction: fraction of peak hours covered by BESS.
      At 0, scarcity premium fully preserved.
      At 1, scarcity premium fully eroded → prices converge to gas_vc.
    """
    coal_regulated_mw = coal_capacity_mw - coal_deregulated_mw
    res_load = df['residual_load'] if 'residual_load' in df.columns \
               else compute_residual_load(df)

    def price_from_res(L: float) -> float:
        if L < 0:
            # Renewable/nuclear surplus → curtailment
            return max(-100.0, L * 0.03)
        if L < 300:
            return 10.0
        if L < coal_regulated_mw:
            # Regulated coal marginal – linear ramp
            frac = (L - 300) / max(coal_regulated_mw - 300, 1)
            return 10.0 + frac * (coal_vc - 10.0)
        if L < coal_capacity_mw:
            # Deregulated coal: bids at full cost (no regulated floor)
            return coal_vc
        if L < coal_capacity_mw + gas_capacity_mw:
            # Gas marginal
            return gas_vc
        # Scarcity / imports – premium erodes as BESS covers peak more
        excess = L - coal_capacity_mw - gas_capacity_mw
        raw_scarcity_premium = min(400.0, excess * 0.15)
        eroded_premium = raw_scarcity_premium * (1.0 - bess_peak_coverage_fraction)
        return gas_vc + eroded_premium

    return res_load.apply(price_from_res)


# ──────────────────────────────────────────────────────────────────────────────
# A.  MERIT ORDER PROXY
# ──────────────────────────────────────────────────────────────────────────────

def compute_residual_load(df: pd.DataFrame) -> pd.Series:
    """L_res = demand – solar – wind – nuclear  (MW)."""
    return df['demand'] - df['solar'] - df['wind'] - df['nuclear']


def piecewise_linear_fit(
    x: np.ndarray,
    y: np.ndarray,
    n_segments: int = 3,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Fit a piecewise linear function to (x, y) using n_segments segments.

    Returns:
        breakpoints  – the interior x breakpoints (length n_segments - 1)
        slopes       – slope of each segment (length n_segments)
        intercepts   – intercept of each segment (length n_segments)
    """
    # Bin x into quantiles, fit a line to each bin
    q = np.linspace(0, 100, n_segments + 1)
    pct = np.percentile(x, q)
    slopes, intercepts = [], []
    for i in range(n_segments):
        lo, hi = pct[i], pct[i + 1]
        mask = (x >= lo) & (x <= hi)
        if mask.sum() < 5:
            slopes.append(0.0); intercepts.append(np.median(y)); continue
        xi, yi = x[mask], y[mask]
        slope, intercept, *_ = linregress(xi, yi)
        slopes.append(float(slope))
        intercepts.append(float(intercept))
    breakpoints = pct[1:-1]
    return breakpoints, np.array(slopes), np.array(intercepts)


def build_merit_order_model(df: pd.DataFrame) -> dict:
    """
    Build the Merit Order Proxy from historical data.

    Returns a dict with:
      'breakpoints'    – residual load kink points (MW)
      'slopes'         – EUR/MWh per MW increase in residual load
      'intercepts'     – EUR/MWh at zero load for each segment
      'global_slope'   – single aggregate price sensitivity (EUR/MWh per MW)
      'residual_load'  – full residual load series (for downstream use)
    """
    print('\n── A. Merit Order Proxy ──────────────────────────────────────')
    df = df.copy()
    df['residual_load'] = compute_residual_load(df)

    # Clip extreme prices for regression (keep the ±3 σ range)
    p_mean, p_std = df['price'].mean(), df['price'].std()
    mask = (df['price'] > p_mean - 3 * p_std) & (df['price'] < p_mean + 3 * p_std)
    rdf = df[mask].dropna(subset=['residual_load', 'price'])

    x = rdf['residual_load'].values
    y = rdf['price'].values

    # Global price-demand slope
    global_slope, global_intercept, r, *_ = linregress(x, y)
    print(f'  Global price-demand slope : {global_slope:.4f} EUR/MWh per MW')
    print(f'  R² (global linear)        : {r**2:.3f}')

    # Piecewise (3 segments: renewables, lignite, gas/imports)
    bps, slopes, intercepts = piecewise_linear_fit(x, y, n_segments=3)
    labels = ['Renewables-dominated', 'Lignite base-load', 'Gas/imports marginal']
    for i, (s, bp_label) in enumerate(zip(slopes, labels)):
        print(f'  Segment {i+1} ({bp_label}): slope = {s:.4f} EUR/MWh per MW')
    print(f'  Kink points at residual load: {bps[0]:.0f} MW, {bps[1]:.0f} MW')

    return {
        'breakpoints': bps,
        'slopes': slopes,
        'intercepts': intercepts,
        'global_slope': float(global_slope),
        'global_intercept': float(global_intercept),
        'residual_load': df['residual_load'],
    }


def merit_order_price_impact(
    bess_net_mw: float,          # positive = discharge (reduces demand), negative = charge
    residual_load_mw: float,
    merit_model: dict,
) -> float:
    """
    Return the price change (EUR/MWh) caused by BESS injecting bess_net_mw MW.
    Discharge reduces effective demand → price falls.
    Charging increases effective demand → price rises.
    """
    # Which segment does current residual load fall in?
    bps = merit_model['breakpoints']
    slopes = merit_model['slopes']
    if residual_load_mw < bps[0]:
        seg_slope = slopes[0]
    elif residual_load_mw < bps[1]:
        seg_slope = slopes[1]
    else:
        seg_slope = slopes[2]

    # Price impact: bess_net_mw > 0 → discharge → effective demand falls → price drops
    delta_price = -bess_net_mw * seg_slope
    return delta_price


# ──────────────────────────────────────────────────────────────────────────────
# B.  LP ARBITRAGE OPTIMIZER  (daily)
# ──────────────────────────────────────────────────────────────────────────────

def run_daily_lp(
    prices: np.ndarray,               # (H,) domestic EUR/MWh
    initial_soc: float,
    capacity_mwh: float,
    power_mw: float,
    charge_eff: float,
    discharge_eff: float,
    export_prices: np.ndarray | None = None,  # (H,) best neighbor price each hour
    export_cap_mw: float = 0.0,               # max export MW available
) -> dict:
    """
    LP arbitrage optimizer for one day, optionally including export arbitrage.

    When export_prices are provided, the BESS can earn the *differential*
    (export_price − domestic_price) by discharging and exporting, limited
    by the interconnector capacity.  This is modelled as an additional
    revenue on top of domestic discharge:

        effective_discharge_price_t = max(domestic_price_t,
                                          export_price_t)    [up to export_cap_mw]

    Variables (per hour t):
      c_t   ∈ [0, power_mw]       : charging (MW from domestic grid)
      d_t   ∈ [0, power_mw]       : total discharging (MW)
      soc_t ∈ [0, capacity_mwh]   : state of charge (MWh)

    Constraint: c_t + d_t ≤ power_mw  (simultaneity approximation)
    """
    H = len(prices)
    n = 3 * H

    ci = np.arange(H)
    di = np.arange(H, 2 * H)
    si = np.arange(2 * H, 3 * H)

    # Effective discharge price: use best of domestic or export when available
    if export_prices is not None and export_cap_mw > 0:
        # The export premium is earned on min(d_t, export_cap_mw) when
        # export_price > domestic.  Simplification: use max price for objective.
        eff_discharge_price = np.maximum(prices, export_prices)
    else:
        eff_discharge_price = prices

    # ── Objective ──────────────────────────────────────────────────────────────
    c_obj = np.zeros(n)
    c_obj[ci] =  prices / charge_eff
    c_obj[di] = -eff_discharge_price * discharge_eff

    # ── Equality constraints: SoC continuity ──────────────────────────────────
    A_eq = np.zeros((H, n))
    b_eq = np.zeros(H)
    for t in range(H):
        A_eq[t, si[t]] = 1.0
        A_eq[t, ci[t]] = -charge_eff
        A_eq[t, di[t]] = 1.0 / discharge_eff
        if t > 0:
            A_eq[t, si[t - 1]] = -1.0
    b_eq[0] = initial_soc

    # ── Inequality constraints: simultaneity  c_t + d_t ≤ power_mw ────────────
    A_ub = np.zeros((H, n))
    b_ub = np.full(H, power_mw)
    for t in range(H):
        A_ub[t, ci[t]] = 1.0
        A_ub[t, di[t]] = 1.0

    # ── Variable bounds ────────────────────────────────────────────────────────
    bounds = (
        [(0, power_mw)] * H +       # charging bounds
        [(0, power_mw)] * H +       # discharging bounds
        [(0, capacity_mwh)] * H     # SoC bounds
    )

    result = linprog(
        c_obj,
        A_ub=A_ub, b_ub=b_ub,
        A_eq=A_eq, b_eq=b_eq,
        bounds=bounds,
        method='highs',
        options={'disp': False},
    )

    if result.status not in (0, 1):
        # Infeasible or numerical issue – return zero dispatch
        return {
            'charge': np.zeros(H), 'discharge': np.zeros(H),
            'soc': np.full(H, initial_soc),
            'profit': 0.0, 'final_soc': initial_soc,
        }

    x = result.x
    charge    = np.clip(x[ci], 0, power_mw)
    discharge = np.clip(x[di], 0, power_mw)
    soc       = np.clip(x[si], 0, capacity_mwh)

    profit = float(-result.fun)
    final_soc = float(soc[-1])

    return {
        'charge': charge,
        'discharge': discharge,
        'soc': soc,
        'profit': profit,
        'final_soc': final_soc,
    }


def run_annual_lp(
    df: pd.DataFrame,
    capacity_mwh: float,
    power_mw: float,
    charge_eff: float = CHARGE_EFF,
    discharge_eff: float = DISCHARGE_EFF,
    merit_model: dict | None = None,
    apply_price_feedback: bool = False,
    neighbor_prices: dict[str, pd.Series] | None = None,
    label: str = '',
) -> pd.DataFrame:
    """
    Run the daily LP optimizer for every day in df.

    neighbor_prices: dict of {country: price Series} for export arbitrage.
      When provided, the LP optimises against max(domestic, best_neighbor).
    """
    df = df.copy().sort_index()
    days = df.index.normalize().unique()

    # Build per-hour best export price Series (aligned to df index)
    if neighbor_prices:
        export_cap_mw = sum(MAX_EXPORT.get(c, 0) for c in neighbor_prices)
        best_neighbor = pd.concat(neighbor_prices.values(), axis=1).max(axis=1)
        best_neighbor = best_neighbor.reindex(df.index, method='nearest', tolerance='1h')
    else:
        export_cap_mw = 0.0
        best_neighbor = None

    results = []
    soc = 0.0

    for day in days:
        day_mask = df.index.normalize() == day
        ddf = df[day_mask]
        prices = ddf['price'].fillna(ddf['price'].median()).values
        H = len(prices)
        if H == 0:
            continue

        cap  = min(capacity_mwh, BESS_CAPACITY_MWH)
        p_mw = min(power_mw, BESS_POWER_MW)

        # Export prices for this day (if available)
        if best_neighbor is not None:
            ep_series = best_neighbor.reindex(ddf.index)
            ep_series = ep_series.fillna(pd.Series(prices, index=ddf.index))
            ep = ep_series.values
        else:
            ep = None

        day_result = run_daily_lp(
            prices, initial_soc=soc,
            capacity_mwh=cap, power_mw=p_mw,
            charge_eff=charge_eff, discharge_eff=discharge_eff,
            export_prices=ep, export_cap_mw=export_cap_mw,
        )

        charge    = day_result['charge']
        discharge = day_result['discharge']
        soc_arr   = day_result['soc']
        soc       = day_result['final_soc']

        # Net flow: positive = discharge (supply), negative = charge (demand)
        net_bess = discharge - charge

        # If price feedback enabled, compute adjusted prices
        if apply_price_feedback and merit_model is not None:
            res_load_day = ddf['residual_load'].values if 'residual_load' in ddf.columns \
                           else np.full(H, merit_model['breakpoints'].mean())
            adjusted_prices = prices.copy()
            for t in range(H):
                dp = merit_order_price_impact(
                    net_bess[t], res_load_day[t], merit_model
                )
                adjusted_prices[t] = prices[t] + dp
        else:
            adjusted_prices = prices

        # Revenue: discharge earns adjusted_price × discharge × η_dis
        # Cost:    charge costs adjusted_price × charge / η_ch (from grid side)
        revenue  = float(np.sum(adjusted_prices * discharge * discharge_eff))
        cost     = float(np.sum(adjusted_prices * charge / charge_eff))
        daily_profit = revenue - cost

        # Cycle count: each full cycle = capacity_mwh charged + capacity_mwh discharged
        total_charged_mwh = float(np.sum(charge))
        cycles = total_charged_mwh / cap if cap > 0 else 0.0

        for t in range(H):
            results.append({
                't': ddf.index[t],
                'charge': charge[t],
                'discharge': discharge[t],
                'soc': soc_arr[t],
                'net_bess': net_bess[t],
                'adjusted_price': adjusted_prices[t],
                'baseline_price': prices[t],
            })

    out = pd.DataFrame(results).set_index('t')
    return out


# ──────────────────────────────────────────────────────────────────────────────
# C.  CANNIBALIZATION & SATURATION
# ──────────────────────────────────────────────────────────────────────────────

def run_saturation_sweep(
    df: pd.DataFrame,
    merit_model: dict,
    capacity_steps_gwh: list[float] | None = None,
) -> pd.DataFrame:
    """
    Iteratively inject BESS capacity and measure spread decay.

    For each capacity level C:
      1. Run annual LP (with price feedback).
      2. Compute peak/trough price spread.
      3. Record KPIs.

    Returns a DataFrame indexed by capacity_gwh with KPI columns.
    """
    print('\n── C. Cannibalization & Saturation Sweep ────────────────────')

    if capacity_steps_gwh is None:
        capacity_steps_gwh = [0, 2, 4, 6, 8, 10, 12, 14, 15]

    # Pre-compute residual load (needed for price feedback)
    df = df.copy()
    df['residual_load'] = compute_residual_load(df)

    rows = []
    for cap_gwh in capacity_steps_gwh:
        cap_mwh = cap_gwh * 1000
        p_mw    = cap_mwh / 4   # 4-hour duration

        if cap_gwh == 0:
            # Baseline: no BESS
            valid_prices = df['price'].dropna()
            peak = float(valid_prices.quantile(0.95))
            trough = float(valid_prices.quantile(0.05))
            spread = peak - trough
            profit = 0.0
            cycles_per_day = 0.0
            avg_peak_reduction = 0.0
            avg_floor_increase = 0.0
            avg_price = float(valid_prices.mean())
            re_saved_gwh = 0.0
            net_export_twh = 0.0
            rows.append({
                'capacity_gwh': 0,
                'spread_eur_mwh': spread,
                'peak_price': peak,
                'trough_price': trough,
                'annual_profit_meur': 0.0,
                'avg_daily_cycles': 0.0,
                'peak_reduction_eur_mwh': 0.0,
                'floor_increase_eur_mwh': 0.0,
                'spread_decay_pct': 0.0,
                're_saved_gwh': 0.0,
                'net_export_change_gwh': 0.0,
            })
            baseline_peak   = peak
            baseline_trough = trough
            baseline_spread = spread
            print(f'  C={cap_gwh:5.1f} GWh | baseline spread={spread:.1f} EUR/MWh')
            continue

        sim = run_annual_lp(
            df, cap_mwh, p_mw,
            merit_model=merit_model,
            apply_price_feedback=True,
        )

        # KPIs
        adj_prices    = sim['adjusted_price']
        peak_sim      = float(adj_prices.quantile(0.95))
        trough_sim    = float(adj_prices.quantile(0.05))
        spread_sim    = peak_sim - trough_sim
        spread_decay  = (baseline_spread - spread_sim) / baseline_spread * 100

        # Report price-taking (LP) profit, not realized profit, for the sweep
        annual_profit = float(
            (sim['baseline_price'] * sim['discharge'] * DISCHARGE_EFF).sum()
            - (sim['baseline_price'] * sim['charge'] / CHARGE_EFF).sum()
        )

        total_charged = float(sim['charge'].sum())
        n_days = (df.index[-1] - df.index[0]).days + 1
        avg_cycles = (total_charged / cap_mwh) / n_days if cap_mwh > 0 else 0.0

        peak_reduction   = baseline_peak   - peak_sim
        floor_increase   = trough_sim      - baseline_trough

        # Renewable curtailment proxy: hours when solar+wind+nuclear > demand (residual_load < 0)
        surplus_series = (-df['residual_load'].fillna(0)).clip(lower=0).reindex(sim.index, fill_value=0)
        re_saved_gwh = float(sim['charge'].clip(upper=surplus_series).sum() / 1000)

        # Net export change (positive = Bulgaria exports more)
        net_export_change_gwh = float(
            (sim['discharge'] - sim['charge']).sum() / 1000
        )

        # Spread vs cycle cost
        cycle_cost = CYCLE_DEGRADATION_COST_EUR_PER_MWH * BESS_CAPACITY_MWH / 1000  # EUR/cycle
        cycle_cost_per_mwh = CYCLE_DEGRADATION_COST_EUR_PER_MWH / ROUNDTRIP_EFF

        rows.append({
            'capacity_gwh': cap_gwh,
            'spread_eur_mwh': spread_sim,
            'peak_price': peak_sim,
            'trough_price': trough_sim,
            'annual_profit_meur': annual_profit / 1e6,
            'avg_daily_cycles': avg_cycles,
            'peak_reduction_eur_mwh': peak_reduction,
            'floor_increase_eur_mwh': floor_increase,
            'spread_decay_pct': spread_decay,
            're_saved_gwh': re_saved_gwh,
            'net_export_change_gwh': net_export_change_gwh,
        })

        saturated = spread_sim < cycle_cost_per_mwh
        status = ' ← SATURATED' if saturated else ''
        print(f'  C={cap_gwh:5.1f} GWh | spread={spread_sim:.1f}  profit={annual_profit/1e6:.2f} M€'
              f'  cycles/day={avg_cycles:.2f}{status}')

    return pd.DataFrame(rows).set_index('capacity_gwh')


# ──────────────────────────────────────────────────────────────────────────────
# D.  KPI EXTRACTION
# ──────────────────────────────────────────────────────────────────────────────

def extract_kpis(
    df: pd.DataFrame,
    sim: pd.DataFrame,
    merit_model: dict,
    season_label: str = 'Full year',
) -> dict:
    """
    Compute final KPIs for the 15 GWh BESS scenario.

    Two profit measures are reported:
      arbitrage_profit  – what the LP optimizer captured (price-taking, baseline prices)
      realized_profit   – profit after applying market price feedback (cannibalization)
    """
    # Align baseline data to simulation index
    df_aligned = df.reindex(sim.index)
    base_prices = df_aligned['price'].fillna(df_aligned['price'].median())
    adj_prices  = sim['adjusted_price']

    # ── Price KPIs: compare same set of hours (baseline-defined peak/floor) ────
    # Peak = hours above P90 baseline; floor = hours below P10 baseline
    peak_threshold   = float(base_prices.quantile(0.90))
    floor_threshold  = float(base_prices.quantile(0.10))

    peak_hours_mask  = base_prices >= peak_threshold
    floor_hours_mask = base_prices <= floor_threshold

    peak_base   = float(base_prices[peak_hours_mask].mean())
    peak_sim    = float(adj_prices[peak_hours_mask].mean())
    trough_base = float(base_prices[floor_hours_mask].mean())
    trough_sim  = float(adj_prices[floor_hours_mask].mean())
    avg_price_base = float(base_prices.mean())
    avg_price_sim  = float(adj_prices.mean())

    # ── Renewable curtailment saved ─────────────────────────────────────────────
    # True curtailment occurs when solar + wind + nuclear > demand (residual_load < 0).
    # The BESS can absorb the surplus (= -residual_load when negative).
    # This represents RE that would otherwise be curtailed or exported at very low prices.
    if 'residual_load' in df_aligned.columns:
        # Surplus MWh available to charge = abs(residual_load) when it's negative
        surplus = (-df_aligned['residual_load'].fillna(0)).clip(lower=0)
    else:
        surplus = (
            df_aligned['solar'].fillna(0) +
            df_aligned['wind'].fillna(0) +
            df_aligned['nuclear'].fillna(0) -
            df_aligned['demand'].fillna(0)
        ).clip(lower=0)
    # Battery charges up to the available surplus (can't save more than available)
    charge_capped = sim['charge'].clip(upper=surplus)
    re_saved_gwh = float(charge_capped.sum() / 1000)

    # ── Cross-border impact ─────────────────────────────────────────────────────
    # Positive = BESS net discharge → Bulgaria adds supply → shift towards export
    net_bess_annual_gwh = float((sim['discharge'] - sim['charge']).sum() / 1000)

    # ── Cycle metrics ────────────────────────────────────────────────────────────
    total_charge_gwh = float(sim['charge'].sum() / 1000)
    cap_gwh = BESS_CAPACITY_MWH / 1000
    n_days = max((df.index[-1] - df.index[0]).days + 1, 1)
    avg_daily_cycles = (total_charge_gwh / cap_gwh) / n_days

    # ── Profits ──────────────────────────────────────────────────────────────────
    # Price-taking LP profit (what the optimizer captured, no feedback)
    arbitrage_revenue = float((base_prices * sim['discharge'] * DISCHARGE_EFF).sum())
    arbitrage_cost    = float((base_prices * sim['charge'] / CHARGE_EFF).sum())
    arbitrage_profit  = arbitrage_revenue - arbitrage_cost

    # Realized profit after cannibalization (adjusted prices)
    realized_revenue  = float((adj_prices * sim['discharge'] * DISCHARGE_EFF).sum())
    realized_cost     = float((adj_prices * sim['charge'] / CHARGE_EFF).sum())
    realized_profit   = realized_revenue - realized_cost

    return {
        'season':               season_label,
        'avg_price_base':       avg_price_base,
        'avg_price_sim':        avg_price_sim,
        'avg_price_delta':      avg_price_sim - avg_price_base,
        'peak_price_base':      peak_base,
        'peak_price_sim':       peak_sim,
        'peak_reduction':       peak_base - peak_sim,      # positive = BESS reduced peak
        'trough_price_base':    trough_base,
        'trough_price_sim':     trough_sim,
        'floor_increase':       trough_sim - trough_base,  # positive = BESS raised floor
        're_saved_gwh':         re_saved_gwh,
        'net_bess_annual_gwh':  net_bess_annual_gwh,
        'avg_daily_cycles':     avg_daily_cycles,
        'arbitrage_profit_meur': arbitrage_profit / 1e6,
        'realized_profit_meur':  realized_profit / 1e6,
        'annual_charge_gwh':    total_charge_gwh,
    }


def print_kpi_report(kpis: list[dict]) -> None:
    print('\n' + '=' * 70)
    print('  KPI REPORT – 15 GWh BESS IMPACT ON BULGARIA DAM')
    print('=' * 70)
    col_w = 32
    for k in kpis:
        peak_dir   = '↓' if k['peak_reduction'] > 0 else '↑'
        floor_dir  = '↑' if k['floor_increase'] > 0 else '↓'
        cross_dir  = 'export↑' if k['net_bess_annual_gwh'] > 0 else 'import↑'
        print(f'\n  Season: {k["season"]}')
        print(f'  {"Avg price delta":<{col_w}} {k["avg_price_delta"]:+.2f} EUR/MWh')
        print(f'  {"Peak price (top-10% hours)":<{col_w}} {k["peak_price_base"]:.1f} → '
              f'{k["peak_price_sim"]:.1f}  ({k["peak_reduction"]:+.1f} EUR/MWh {peak_dir})')
        print(f'  {"Floor price (bot-10% hours)":<{col_w}} {k["trough_price_base"]:.1f} → '
              f'{k["trough_price_sim"]:.1f}  ({k["floor_increase"]:+.1f} EUR/MWh {floor_dir})')
        print(f'  {"RE saved from curtailment":<{col_w}} {k["re_saved_gwh"]:.1f} GWh')
        print(f'  {"Net BESS position":<{col_w}} {k["net_bess_annual_gwh"]:+.1f} GWh/year  ({cross_dir})')
        print(f'  {"Avg daily cycles":<{col_w}} {k["avg_daily_cycles"]:.2f}')
        print(f'  {"Arbitrage profit (price-taker)":<{col_w}} {k["arbitrage_profit_meur"]:.2f} M€')
        print(f'  {"Realized profit (after cannibaliz.)":<{col_w}} {k["realized_profit_meur"]:.2f} M€')
    print('=' * 70)


# ──────────────────────────────────────────────────────────────────────────────
# CHARTS
# ──────────────────────────────────────────────────────────────────────────────

def plot_merit_order(df: pd.DataFrame, merit_model: dict, output_dir: Path) -> None:
    """Scatter plot of price vs residual load with piecewise regression lines."""
    df2 = df.copy()
    df2['residual_load'] = compute_residual_load(df2)
    rdf = df2.dropna(subset=['residual_load', 'price'])
    rdf = rdf[(rdf['price'] > -50) & (rdf['price'] < 500)]

    x = rdf['residual_load'].values
    y = rdf['price'].values

    bps = merit_model['breakpoints']
    slopes = merit_model['slopes']
    intercepts = merit_model['intercepts']

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(x, y, alpha=0.05, s=3, color='steelblue', label='Hourly observations')

    # Draw piecewise segments
    seg_bounds = [x.min(), bps[0], bps[1], x.max()]
    colors = ['green', 'saddlebrown', 'red']
    seg_labels = ['Renewables', 'Lignite', 'Gas/Imports']
    for i in range(3):
        xi = np.linspace(seg_bounds[i], seg_bounds[i + 1], 100)
        yi = slopes[i] * xi + intercepts[i]
        ax.plot(xi, yi, color=colors[i], lw=2.5, label=f'{seg_labels[i]} (slope={slopes[i]:.3f})')

    for bp in bps:
        ax.axvline(bp, color='grey', ls='--', lw=1.2, alpha=0.7)
        ax.text(bp, ax.get_ylim()[1] * 0.9, f'{bp:.0f} MW', ha='center', fontsize=8, color='grey')

    ax.set_xlabel('Residual Load (MW) = Demand − Solar − Wind − Nuclear')
    ax.set_ylabel('Day-Ahead Price (EUR/MWh)')
    ax.set_title('Bulgaria Merit Order Proxy – Price vs Residual Load')
    ax.legend(fontsize=8)
    ax.set_ylim(-30, 400)
    plt.tight_layout()
    out = output_dir / 'merit_order.png'
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f'  Chart saved: {out}')


def plot_saturation(sweep: pd.DataFrame, output_dir: Path) -> None:
    """Two-panel plot: spread decay and annual profit vs BESS capacity."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    ax1.plot(sweep.index, sweep['spread_eur_mwh'], 'o-', color='steelblue', lw=2)
    ax1.set_xlabel('BESS Capacity (GWh)')
    ax1.set_ylabel('Price Spread P95-P5 (EUR/MWh)')
    ax1.set_title('Spread Decay vs BESS Capacity')
    ax1.grid(True, alpha=0.3)

    # Mark saturation point
    cycle_cost = CYCLE_DEGRADATION_COST_EUR_PER_MWH / ROUNDTRIP_EFF
    ax1.axhline(cycle_cost, color='red', ls='--', lw=1.5,
                label=f'Cycle cost floor ({cycle_cost:.0f} EUR/MWh)')
    sat_mask = sweep['spread_eur_mwh'] < cycle_cost
    if sat_mask.any():
        sat_cap = sweep[sat_mask].index[0]
        ax1.axvline(sat_cap, color='orange', ls=':', lw=2, label=f'Saturation at {sat_cap} GWh')
    ax1.legend(fontsize=8)

    ax2.bar(sweep.index, sweep['annual_profit_meur'], color='seagreen', alpha=0.8, width=1.5)
    ax2.set_xlabel('BESS Capacity (GWh)')
    ax2.set_ylabel('Annual Gross Profit (M€)')
    ax2.set_title('BESS Annual Profit vs Capacity')
    ax2.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    out = output_dir / 'saturation_sweep.png'
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f'  Chart saved: {out}')


def plot_daily_profile(df: pd.DataFrame, sim: pd.DataFrame, output_dir: Path) -> None:
    """Average hourly profile: baseline price, adjusted price, BESS dispatch."""
    sim2 = sim.copy()
    sim2['hour'] = sim2.index.hour

    prof = sim2.groupby('hour').agg(
        avg_charge=('charge', 'mean'),
        avg_discharge=('discharge', 'mean'),
        avg_adj_price=('adjusted_price', 'mean'),
        avg_base_price=('baseline_price', 'mean'),
    )

    fig, ax1 = plt.subplots(figsize=(11, 5))
    hours = prof.index
    ax1.bar(hours - 0.2, prof['avg_discharge'], width=0.35, color='seagreen',
            alpha=0.8, label='Avg Discharge (MW)')
    ax1.bar(hours + 0.2, prof['avg_charge'], width=0.35, color='tomato',
            alpha=0.8, label='Avg Charge (MW)')
    ax1.set_xlabel('Hour of Day (UTC)')
    ax1.set_ylabel('Battery Power (MW)')
    ax1.set_xticks(range(24))

    ax2 = ax1.twinx()
    ax2.plot(hours, prof['avg_base_price'], 'k--', lw=1.5, label='Baseline Price')
    ax2.plot(hours, prof['avg_adj_price'],  'b-',  lw=2,   label='Adjusted Price (with BESS)')
    ax2.set_ylabel('Price (EUR/MWh)')

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=8)
    ax1.set_title('Average Daily BESS Dispatch Profile – 15 GWh')
    plt.tight_layout()
    out = output_dir / 'daily_dispatch_profile.png'
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f'  Chart saved: {out}')


def plot_seasonal_kpis(kpis: list[dict], output_dir: Path) -> None:
    """Bar chart comparing KPIs across seasons."""
    seasons = [k['season'] for k in kpis]
    metrics = {
        'Peak reduction (EUR/MWh)': [k['peak_reduction'] for k in kpis],
        'Floor increase (EUR/MWh)': [k['floor_increase'] for k in kpis],
        'RE saved (GWh)':           [k['re_saved_gwh'] for k in kpis],
        'Avg daily cycles':         [k['avg_daily_cycles'] * 100 for k in kpis],  # ×100 for visibility
    }

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    axes = axes.flatten()
    colors = ['steelblue', 'seagreen', 'tomato', 'gold']
    for ax, (title, vals), color in zip(axes, metrics.items(), colors):
        ax.bar(seasons, vals, color=color, alpha=0.8)
        ax.set_title(title + (' (×100)' if 'cycles' in title else ''))
        ax.set_xticklabels(seasons, rotation=20, ha='right', fontsize=8)
        ax.grid(True, axis='y', alpha=0.3)
    plt.suptitle('15 GWh BESS – Seasonal KPI Comparison', fontsize=13, fontweight='bold')
    plt.tight_layout()
    out = output_dir / 'seasonal_kpis.png'
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f'  Chart saved: {out}')


# ──────────────────────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description='15 GWh BESS Market Impact Analysis')
    parser.add_argument('--year',        type=int,   default=2025)
    parser.add_argument('--output',      default='./analysis_output')
    parser.add_argument('--no-sweep',    action='store_true', help='Skip saturation sweep')
    parser.add_argument('--solar-addon', type=float, default=2000.0,
                        help='Additional solar MW to install (default: 2000)')
    parser.add_argument('--solar-base',  type=float, default=5300.0,
                        help='Current installed solar MW (default: 5300)')
    parser.add_argument('--coal-dereg',  type=float, default=600.0,
                        help='Coal MW leaving regulated market (default: 600)')
    parser.add_argument('--coal-vc',     type=float, default=COAL_VC_EUR_MWH,
                        help=f'Coal full-cost floor EUR/MWh (default: {COAL_VC_EUR_MWH})')
    parser.add_argument('--gas-vc',      type=float, default=GAS_VC_EUR_MWH,
                        help=f'Gas full-cost floor EUR/MWh (default: {GAS_VC_EUR_MWH})')
    parser.add_argument('--export',      action='store_true',
                        help='Enable cross-border export arbitrage (RO + GR prices)')
    parser.add_argument('--structural',  action='store_true',
                        help='Use structural equilibrium prices (peak-premium-eroded)')
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f'15 GWh BESS Market Impact Analysis  –  Year: {args.year}')
    print(f'Scenarios: +{args.solar_addon:.0f} MW solar | {args.coal_dereg:.0f} MW coal deregulated'
          f' | export={args.export} | structural={args.structural}')
    print(f'Output: {output_dir}')

    # ── Load data ─────────────────────────────────────────────────────────────
    print(f'\nLoading data...')
    df_year  = clean(load_year(args.year))
    df_sweep = clean(load_years(YEARS_FOR_SWEEP))
    print(f'  Primary year : {len(df_year):,} valid hours')
    print(f'  Sweep dataset: {len(df_sweep):,} valid hours')

    # ── Apply solar scaling ───────────────────────────────────────────────────
    if args.solar_addon > 0:
        factor = (args.solar_base + args.solar_addon) / args.solar_base
        print(f'\n  Solar scaling: {args.solar_base:.0f} → {args.solar_base + args.solar_addon:.0f} MW'
              f' (×{factor:.3f})')
        df_year  = scale_solar(df_year,  args.solar_addon, args.solar_base)
        df_sweep = scale_solar(df_sweep, args.solar_addon, args.solar_base)

    # Compute residual load (used everywhere)
    df_year['residual_load']  = compute_residual_load(df_year)
    df_sweep['residual_load'] = compute_residual_load(df_sweep)

    # ── Structural price adjustment ───────────────────────────────────────────
    if args.structural:
        print(f'\n  Structural price model: coal_vc={args.coal_vc}, gas_vc={args.gas_vc}'
              f', coal_dereg={args.coal_dereg} MW')
        print(f'  → Replacing historical prices with supply-stack equilibrium prices')
        print(f'  → Peak-premium erosion: coal/gas refuse overnight baseload without peak')
        for df_ in (df_year, df_sweep):
            struct_prices = compute_structural_prices(
                df_,
                coal_vc=args.coal_vc,
                gas_vc=args.gas_vc,
                coal_capacity_mw=COAL_CAPACITY_MW,
                coal_deregulated_mw=args.coal_dereg,
                gas_capacity_mw=GAS_CAPACITY_MW,
                bess_peak_coverage_fraction=0.6,   # 15 GWh covers ~60% of peak hours
            )
            df_['price'] = struct_prices
        print(f'  Structural price stats: avg={df_year.price.mean():.1f}'
              f', P5={df_year.price.quantile(0.05):.1f}'
              f', P95={df_year.price.quantile(0.95):.1f} EUR/MWh')

    # ── Load neighbor prices for export arbitrage ─────────────────────────────
    neighbor_prices: dict | None = None
    if args.export:
        print(f'\n  Loading neighbor prices for export arbitrage...')
        neighbor_prices = load_neighbor_prices(args.year)

    # ── A. Merit Order Proxy ──────────────────────────────────────────────────
    merit_model = build_merit_order_model(df_sweep)
    print('\n  Generating merit order chart...')
    plot_merit_order(df_sweep, merit_model, output_dir)

    # ── B. Annual LP simulation ───────────────────────────────────────────────
    print(f'\n── B. Annual LP Optimizer ({args.year}, 15 GWh) ─────────────────')
    sim_full = run_annual_lp(
        df_year, BESS_CAPACITY_MWH, BESS_POWER_MW,
        merit_model=merit_model,
        apply_price_feedback=True,
        neighbor_prices=neighbor_prices,
    )
    total_charge = sim_full['charge'].sum()
    total_disc   = sim_full['discharge'].sum()
    print(f'  Total charged   : {total_charge/1000:.1f} GWh')
    print(f'  Total discharged: {total_disc/1000:.1f} GWh')
    arb_profit = (
        (sim_full['baseline_price'] * sim_full['discharge'] * DISCHARGE_EFF).sum()
        - (sim_full['baseline_price'] * sim_full['charge'] / CHARGE_EFF).sum()
    )
    print(f'  Arbitrage profit (price-taker): {arb_profit/1e6:.2f} M€/year')

    # ── C. Saturation sweep ───────────────────────────────────────────────────
    if not args.no_sweep:
        sweep = run_saturation_sweep(df_sweep, merit_model)
        sweep.to_csv(output_dir / 'saturation_sweep.csv')
        print('\n  Saturation Sweep Results:')
        print(sweep[['spread_eur_mwh', 'annual_profit_meur',
                     'avg_daily_cycles', 'peak_reduction_eur_mwh',
                     'floor_increase_eur_mwh']].to_string())
        plot_saturation(sweep, output_dir)
    else:
        sweep = None
        print('  (Saturation sweep skipped)')

    # ── D. KPI Report ─────────────────────────────────────────────────────────
    print(f'\n── D. KPI Extraction ─────────────────────────────────────────────')
    kpis = []
    kpis.append(extract_kpis(df_year, sim_full, merit_model, 'Full year'))

    seasons = {
        'High Solar (May–Aug)':        ((5, 8),   False),
        'High Wind (Nov–Feb)':         ((11, 14), True),   # wraps around Jan
        'Shoulder (Mar–Apr, Sep–Oct)': (None,     False),
    }
    for season_label, (month_range, wraps) in seasons.items():
        m = df_year.index.month
        if month_range is None:
            mask = ((m >= 3) & (m <= 4)) | ((m >= 9) & (m <= 10))
        elif wraps:
            mask = (m >= month_range[0]) | (m <= month_range[1] - 12)
        else:
            mask = (m >= month_range[0]) & (m <= month_range[1])

        dfs = clean(df_year[mask].copy())
        if len(dfs) < 100:
            continue
        dfs['residual_load'] = compute_residual_load(dfs)
        sim_s = run_annual_lp(
            dfs, BESS_CAPACITY_MWH, BESS_POWER_MW,
            merit_model=merit_model,
            apply_price_feedback=True,
            neighbor_prices=neighbor_prices,
        )
        kpis.append(extract_kpis(dfs, sim_s, merit_model, season_label))

    print_kpi_report(kpis)

    kpi_df = pd.DataFrame(kpis).set_index('season')
    kpi_df.to_csv(output_dir / 'kpi_report.csv')
    print(f'\n  KPI table saved to {output_dir / "kpi_report.csv"}')

    # ── Structural vs historical comparison (if structural mode) ──────────────
    if args.structural:
        print('\n── E. Structural Equilibrium Impact ─────────────────────────────')
        print('  Structural price model captures the second-order market effect:')
        print('  BESS flattens peak → coal/gas lose peak premium → refuse overnight')
        print('  baseload → prices converge to full-cost recovery band')
        struct_spread = df_year['price'].quantile(0.95) - df_year['price'].quantile(0.05)
        print(f'  Structural price spread (P95-P5): {struct_spread:.1f} EUR/MWh')
        print(f'  (vs historical spread which includes scarcity spikes)')
        print(f'  → Reduced spread = reduced BESS arbitrage opportunity in equilibrium')

    print('\nGenerating charts...')
    plot_daily_profile(df_year, sim_full, output_dir)
    if len(kpis) >= 2:
        plot_seasonal_kpis(kpis, output_dir)

    # ── Summary ────────────────────────────────────────────────────────────────
    print('\n✓ Analysis complete.')
    print(f'  Charts + CSV saved to: {output_dir}/')
    full = kpis[0]
    print(f'\n  15 GWh BESS – Key Takeaways ({args.year}):')
    print(f'    Peak price reduction     : {full["peak_reduction"]:+.1f} EUR/MWh')
    print(f'    Floor price increase     : {full["floor_increase"]:+.1f} EUR/MWh')
    print(f'    RE curtailment saved     : {full["re_saved_gwh"]:.1f} GWh/year')
    print(f'    Avg daily cycles         : {full["avg_daily_cycles"]:.2f}')
    print(f'    Arbitrage profit (LP)    : {full["arbitrage_profit_meur"]:.2f} M€')
    print(f'    Realized profit (after market impact): {full["realized_profit_meur"]:.2f} M€')


if __name__ == '__main__':
    main()
