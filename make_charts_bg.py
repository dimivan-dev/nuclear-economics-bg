#!/usr/bin/env python3
"""
Generate the 3 article charts with Bulgarian labels.

Charts produced:
  charts/cost_vs_cf.png         — себестойност спрямо коефициент на използване
  charts/feb15_2026_prices.png  — цени на 15 февруари 2026
  charts/strategy_comparison.png — печалба по стратегия
"""
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from collections import defaultdict

CHART_DIR = '/home/yyoncho/Sources/claude/nuclear-economics-bg/charts'

# ── shared helpers ──────────────────────────────────────────────────────────

def get_text(v):
    if isinstance(v, dict):
        return v.get('text', '') or v.get('#text', '')
    return str(v) if v else ''

def ensure_list(obj):
    if obj is None:
        return []
    if isinstance(obj, list):
        return obj
    return [obj]

def load_entsoe_prices(path):
    with open(path) as f:
        d = json.load(f)
    prices = {}
    for ts in ensure_list(d.get('prices', {}).get('TimeSeries', [])):
        for p in ensure_list(ts.get('Period', {})):
            ti = p.get('timeInterval', {})
            start = get_text(ti.get('start', '')) if isinstance(ti, dict) else ''
            if not start:
                continue
            start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
            for pt in ensure_list(p.get('Point', [])):
                pos = int(get_text(pt.get('position', '0')))
                price_raw = pt.get('price.amount')
                if price_raw is None:
                    price_raw = pt.get('price', {})
                val = float(get_text(price_raw))
                hour_dt = start_dt + timedelta(hours=pos - 1)
                key = hour_dt.strftime('%Y-%m-%d %H:00')
                prices[key] = val
    return prices


# ── Chart 1: Себестойност на МВтч спрямо коефициент на използване ──────────

NUCLEAR_FIXED_EUR = 617e6
NUCLEAR_VAR_EUR_MWH = 6.8
NUCLEAR_NAMEPLATE_MW = 2000
HOURS_YEAR = 8760

cfs = np.linspace(0.25, 1.0, 300)
output_mwh = cfs * NUCLEAR_NAMEPLATE_MW * HOURS_YEAR
cost_per_mwh = (NUCLEAR_FIXED_EUR + NUCLEAR_VAR_EUR_MWH * output_mwh) / output_mwh

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(cfs * 100, cost_per_mwh, 'r-', linewidth=2.5)

# Reference lines
ax.axhline(y=120, color='orange', linestyle='--', linewidth=1.5,
           label='Газов паритет (120 EUR/MWh)')
ax.axhline(y=103.5, color='green', linestyle='--', linewidth=1.5,
           label='Средна пазарна цена 2024 (103.5)')
ax.axhline(y=80, color='gray', linestyle='--', linewidth=1.5,
           label='Прогнозна цена с 14 ГВт слънчева (~80)')

# Key points
key_points = [
    (0.31, '  Газов паритет\n  31% / 120€'),
    (0.55, '  +лято изкл.\n  55% / 71€'),
    (0.69, '  ЕСО 2034\n  69% / 59€'),
    (0.89, '  2024\n  89% / 46€'),
]
for cf_val, label in key_points:
    out = cf_val * NUCLEAR_NAMEPLATE_MW * HOURS_YEAR
    cost = (NUCLEAR_FIXED_EUR + NUCLEAR_VAR_EUR_MWH * out) / out
    ax.plot(cf_val * 100, cost, 'ko', markersize=7)
    ax.annotate(label, xy=(cf_val * 100, cost), fontsize=9, fontweight='bold',
                va='center')

ax.set_xlabel('Коефициент на използване (%)', fontsize=12)
ax.set_ylabel('Себестойност (EUR/MWh)', fontsize=12)
ax.set_title('АЕЦ Козлодуй: Себестойност на МВтч\nспрямо коефициент на използване',
             fontsize=13, fontweight='bold')
ax.legend(fontsize=9, loc='upper right')
ax.set_xlim(25, 100)
ax.set_ylim(40, 160)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(f'{CHART_DIR}/cost_vs_cf.png', dpi=150, bbox_inches='tight')
plt.close()
print(f'Saved: {CHART_DIR}/cost_vs_cf.png')


# ── Chart 2: 15 февруари 2026 — България срещу Румъния ──────────────────────

bg_prices = load_entsoe_prices('/home/yyoncho/Sources/claude/entso-e/data/BG/2026.json')
ro_prices = load_entsoe_prices('/home/yyoncho/Sources/claude/entso-e/data/RO/2026.json')

feb15_bg = {k: v for k, v in bg_prices.items() if k.startswith('2026-02-15')}
feb15_ro = {k: v for k, v in ro_prices.items() if k.startswith('2026-02-15')}

hours_list = sorted(feb15_bg.keys())
bg_vals = [feb15_bg[k] for k in hours_list]
ro_vals = [feb15_ro[k] for k in hours_list]
hour_nums = list(range(len(hours_list)))

avg_bg = np.mean(bg_vals)
avg_ro = np.mean(ro_vals)

fig, ax = plt.subplots(figsize=(12, 5))
ax.fill_between(hour_nums, ro_vals, alpha=0.25, color='steelblue')
ax.fill_between(hour_nums, bg_vals, alpha=0.35, color='slategray')
ax.plot(hour_nums, bg_vals, 'r-o', linewidth=2, markersize=5, label='България')
ax.plot(hour_nums, ro_vals, 'b-s', linewidth=2, markersize=5, label='Румъния')

ax.text(9, avg_ro + 8, f'RO ср.: {avg_ro:.1f} EUR', color='blue',
        fontsize=11, fontweight='bold')
ax.text(3, avg_bg + 8, f'BG ср.: {avg_bg:.1f} EUR', color='red',
        fontsize=11, fontweight='bold')

ax.set_xlabel('Час на деня', fontsize=12)
ax.set_ylabel('Цена ден напред (EUR/MWh)', fontsize=12)
ax.set_title('15 февруари 2026: България срещу Румъния — Цени', fontsize=13, fontweight='bold')
ax.legend(fontsize=11)
ax.set_xticks(hour_nums)
ax.set_xticklabels([str(h) for h in hour_nums], fontsize=8)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(f'{CHART_DIR}/feb15_2026_prices.png', dpi=150, bbox_inches='tight')
plt.close()
print(f'Saved: {CHART_DIR}/feb15_2026_prices.png')


# ── Chart 3: Ядрена печалба по оперативна стратегия ─────────────────────────
# Re-run the model to get fresh scenario data

NUCLEAR_FIXED_EUR_MODEL = 617e6
NUCLEAR_VAR_EUR_MWH_MODEL = 6.8
NUCLEAR_NAMEPLATE_MW_MODEL = 2000
COAL_FULL_COST = 88
MERIT_SLOPE = 0.018
BASE_SOLAR_GW = 5.3

with open('/home/yyoncho/Sources/claude/nuclear-economics-bg/data/2025.json') as f:
    data = json.load(f)
hours_data = [h for h in data['hours'] if h.get('demand') and h.get('price') is not None]


def get_month(h):
    return int(h['t'][5:7])


def get_hour_num(h):
    return int(h['t'][11:13])


def is_weekend(h):
    dt = datetime.fromisoformat(h['t'].replace('Z', '+00:00'))
    return dt.weekday() >= 5


def model_prices(hours, solar_gw, battery_gwh):
    solar_factor = solar_gw / BASE_SOLAR_GW
    results = []
    for h in hours:
        solar_base = h.get('solar', 0) or 0
        solar_new = solar_base * solar_factor
        extra_solar = solar_new - solar_base
        demand = h['demand']
        price = h['price']

        nuc_actual = h.get('nuclear', 0) or 0
        nuc_shortfall = max(0, NUCLEAR_NAMEPLATE_MW_MODEL - nuc_actual)
        price = max(0, price - nuc_shortfall * MERIT_SLOPE)

        price_adj = max(price - extra_solar * MERIT_SLOPE, 0)
        results.append({
            't': h['t'], 'price': price_adj, 'demand': demand,
            'solar': solar_new, 'month': get_month(h),
            'hour': get_hour_num(h), 'weekend': is_weekend(h),
            'nuclear': h.get('nuclear', 0) or 0,
        })

    if battery_gwh > 0:
        battery_mwh = battery_gwh * 1000
        battery_power_mw = battery_mwh / 4
        efficiency = 0.875
        CHARGE_THRESHOLD = 20
        discharge_impact = battery_power_mw * MERIT_SLOPE
        daily = defaultdict(list)
        for i, h in enumerate(results):
            daily[h['t'][:10]].append(i)
        for day, indices in daily.items():
            cheap_hours = sum(1 for idx in indices if results[idx]['price'] <= CHARGE_THRESHOLD)
            charge_energy = min(battery_mwh, cheap_hours * battery_power_mw)
            available_energy = charge_energy * efficiency
            if available_energy <= 0:
                continue
            expensive = sorted(
                [(idx, results[idx]['price']) for idx in indices],
                key=lambda x: -x[1]
            )
            remaining = available_energy
            for idx, price in expensive:
                if remaining <= 0:
                    break
                discharge = min(battery_power_mw, remaining)
                new_price = max(0, price - discharge * MERIT_SLOPE)
                if new_price >= price:
                    continue
                results[idx]['price'] = new_price
                remaining -= discharge
    return results


def compute_nuclear_economics(price_hours, strategy='full'):
    summer = {6, 7, 8}
    extended = {5, 6, 7, 8, 9}
    shoulder = {4, 5, 9}
    total_revenue = 0
    total_output_mwh = 0
    for h in price_hours:
        month = h['month']
        price = h['price']
        if strategy == 'full':
            nuc_mw = NUCLEAR_NAMEPLATE_MW_MODEL
        elif strategy == 'reduced_summer':
            nuc_mw = 1400 if month in summer else NUCLEAR_NAMEPLATE_MW_MODEL
        elif strategy == 'reduced_extended':
            nuc_mw = 1400 if month in extended else NUCLEAR_NAMEPLATE_MW_MODEL
        elif strategy == 'one_off_summer':
            nuc_mw = 1000 if month in summer else NUCLEAR_NAMEPLATE_MW_MODEL
        elif strategy == 'one_off_extended':
            nuc_mw = 1000 if month in extended else NUCLEAR_NAMEPLATE_MW_MODEL
        elif strategy == 'combo':
            if month in summer:
                nuc_mw = 1000
            elif month in shoulder:
                nuc_mw = 1400
            else:
                nuc_mw = NUCLEAR_NAMEPLATE_MW_MODEL
        else:
            nuc_mw = NUCLEAR_NAMEPLATE_MW_MODEL
        total_revenue += price * nuc_mw
        total_output_mwh += nuc_mw
    total_cost = NUCLEAR_FIXED_EUR_MODEL + NUCLEAR_VAR_EUR_MWH_MODEL * total_output_mwh
    cf = total_output_mwh / (NUCLEAR_NAMEPLATE_MW_MODEL * len(price_hours))
    return {
        'profit': total_revenue - total_cost,
        'cf': cf,
    }


strategies_bg = [
    ('full',             '2×1000 МВт\nцелогодишно'),
    ('reduced_summer',   'Намалено 1400 МВт\nюни–авг.'),
    ('reduced_extended', 'Намалено 1400 МВт\nмай–сеп.'),
    ('one_off_summer',   '1 реактор изкл.\nюни–авг.'),
    ('one_off_extended', '1 реактор изкл.\nмай–сеп.'),
    ('combo',            '1 изкл. юни–авг.\n+ нам. рамо'),
]

strat_scenarios = [(14.3, 16), (14.3, 32), (20, 16), (20, 32)]
strat_titles_bg = [
    '14.3 ГВт + 16 ГВтч (ЕСО 2034)',
    '14.3 ГВт + 32 ГВтч',
    '20 ГВт + 16 ГВтч',
    '20 ГВт + 32 ГВтч',
]

fig, axes = plt.subplots(2, 2, figsize=(16, 10))
for ax, (sg, bg), title in zip(axes.flat, strat_scenarios, strat_titles_bg):
    ph = model_prices(hours_data, sg, bg)
    names, profits, cfs = [], [], []
    for strat_key, strat_name in strategies_bg:
        econ = compute_nuclear_economics(ph, strat_key)
        names.append(strat_name)
        profits.append(econ['profit'] / 1e6)
        cfs.append(econ['cf'] * 100)

    colors = ['green' if p > 0 else 'red' for p in profits]
    bars = ax.bar(range(len(names)), profits, color=colors, alpha=0.7, edgecolor='black')
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels(names, fontsize=7.5, ha='center')
    ax.axhline(y=0, color='black', linewidth=1)
    ax.set_ylabel('М EUR')
    ax.set_title(title, fontsize=11, fontweight='bold')
    for bar, p, c in zip(bars, profits, cfs):
        ypos = bar.get_height() + 3 if p >= 0 else bar.get_height() - 12
        ax.text(bar.get_x() + bar.get_width() / 2, ypos,
                f'{p:+.0f}М\n{c:.0f}%КИ', ha='center', fontsize=8, fontweight='bold')

fig.suptitle('Ядрена печалба по оперативна стратегия', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(f'{CHART_DIR}/strategy_comparison.png', dpi=150, bbox_inches='tight')
plt.close()
print(f'Saved: {CHART_DIR}/strategy_comparison.png')

print('\n✓ Всички графики запазени в', CHART_DIR)
