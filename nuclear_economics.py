#!/usr/bin/env python3
"""Nuclear economics analysis with ACTUAL Kozloduy costs from 2024 annual report."""
import json
import numpy as np

# === ACTUAL KOZLODUY COSTS (2024 Annual Report, BGN thousands -> EUR) ===
BGN_EUR = 1.956  # fixed rate

# From report (in thousand BGN):
total_annual_bgn = 1_842_450
operating_bgn = 1_803_416  # 98%
variable_bgn = 523_210     # 28% - production + RAO/decom funds + grid access
fixed_bgn = 891_242        # 48% - O&M + staff + depreciation
ses_fund_bgn = 388_964     # 21% - SES fund

# Convert to EUR (millions)
total_eur = total_annual_bgn / BGN_EUR / 1000
operating_eur = operating_bgn / BGN_EUR / 1000
variable_eur = variable_bgn / BGN_EUR / 1000
fixed_eur = fixed_bgn / BGN_EUR / 1000
ses_eur = ses_fund_bgn / BGN_EUR / 1000

production_bgn = 154_617
fuel_and_production_eur = production_bgn / BGN_EUR / 1000

print("=" * 70)
print("KOZLODUY NPP - 2024 ACTUAL COSTS")
print("=" * 70)
print("Total annual expenses:    %d M EUR (%d M BGN)" % (total_eur, total_annual_bgn/1000))
print("  Operating expenses:     %d M EUR (98%%)" % operating_eur)
print("    Variable costs:       %d M EUR (28%%)" % variable_eur)
print("      - Production:       %d M EUR" % fuel_and_production_eur)
print("      - RAO/decom funds:  %d M EUR" % (315_251/BGN_EUR/1000))
print("      - Grid access:      %d M EUR" % (53_341/BGN_EUR/1000))
print("    Fixed costs:          %d M EUR (48%%)" % fixed_eur)
print("      - O&M:              %d M EUR" % (289_881/BGN_EUR/1000))
print("      - Staff:            %d M EUR" % (391_944/BGN_EUR/1000))
print("      - Depreciation:     %d M EUR" % (209_417/BGN_EUR/1000))
print("    SES fund:             %d M EUR (21%%)" % ses_eur)
print()

output_twh_2024 = 14.64
output_mwh_2024 = output_twh_2024 * 1e6

print("=" * 70)
print("COST STRUCTURE BREAKDOWN")
print("=" * 70)

truly_fixed_bgn = 891_242 + 388_964
truly_variable_bgn = 154_617 + 53_341
truly_fixed_eur = truly_fixed_bgn / BGN_EUR / 1000
truly_variable_eur = truly_variable_bgn / BGN_EUR / 1000
rao_eur = 315_251 / BGN_EUR / 1000

print("Truly fixed (staff+O&M+depr+SES): %d M EUR" % truly_fixed_eur)
print("RAO/decommissioning funds:         %d M EUR" % rao_eur)
print("Truly variable (fuel+grid):        %d M EUR" % truly_variable_eur)
print("Variable per MWh:                  %.1f EUR/MWh" % (truly_variable_eur*1e6/output_mwh_2024))
print()

total_opex_per_mwh = operating_eur * 1e6 / output_mwh_2024
print("Total OPEX per MWh (2024, %.2f TWh): %.1f EUR/MWh" % (output_twh_2024, total_opex_per_mwh))
print()

print("=" * 70)
print("NUCLEAR ECONOMICS vs CAPACITY FACTOR")
print("=" * 70)

nameplate_mw = 2000
max_output_twh = nameplate_mw * 8760 / 1e6

fixed_no_ses = fixed_eur
fixed_with_ses = fixed_eur + ses_eur
fixed_all = fixed_eur + ses_eur + rao_eur

var_per_mwh = truly_variable_eur * 1e6 / output_mwh_2024

print("Nameplate: %d MW, max annual output: %.1f TWh" % (nameplate_mw, max_output_twh))
print("Variable cost: %.1f EUR/MWh" % var_per_mwh)
print()

print("%5s %6s %18s %18s %18s" % ("CF", "TWh", "A: excl SES+RAO", "B: incl SES", "C: full opex"))
print("%5s %6s %18s %18s %18s" % ("", "", "EUR/MWh", "EUR/MWh", "EUR/MWh"))
print("-" * 70)

cf_levels = [0.90, 0.83, 0.75, 0.70, 0.65, 0.60, 0.55, 0.50, 0.45, 0.40, 0.35, 0.30, 0.25]
for cf in cf_levels:
    twh = nameplate_mw * 8760 * cf / 1e6
    mwh = twh * 1e6
    cost_a = (fixed_no_ses * 1e6 + var_per_mwh * mwh) / mwh
    cost_b = ((fixed_no_ses + ses_eur) * 1e6 + var_per_mwh * mwh) / mwh
    cost_c = (fixed_all * 1e6 + var_per_mwh * mwh) / mwh
    marker = " <-- 2024 actual" if abs(cf - 0.83) < 0.02 else ""
    if abs(cost_c - 120) < 5:
        marker = " <-- GAS PARITY"
    print("%5.0f%% %6.1f %18.1f %18.1f %18.1f%s" % (cf*100, twh, cost_a, cost_b, cost_c, marker))

print()

print("=" * 70)
print("SOLAR GROWTH -> NUCLEAR CF REDUCTION")
print("=" * 70)

with open('/home/yyoncho/Sources/claude/entso-e/app/public/data/2024.json') as f:
    data = json.load(f)

hours = [h for h in data['hours'] if h['demand'] is not None and h['price'] is not None]

base_solar_mw = 5300
nuc_min_mw = 1000
nuc_nameplate = 2000

scenarios = [
    ("2024 actual (5.3 GW)", 0),
    ("+2 GW (7.3 GW)", 2000),
    ("+5 GW (10.3 GW)", 5000),
    ("+9 GW (14.3 GW) - ESO 2034", 9000),
    ("+15 GW (20.3 GW)", 15000),
]

print()
print("%-30s %12s %10s %8s %12s" % ("Scenario", "Curtail hrs", "Lost TWh", "CF", "Full cost"))
print("-" * 75)

for name, addon in scenarios:
    factor = (base_solar_mw + addon) / base_solar_mw
    curtail_hours = 0
    lost_mwh = 0
    nuc_output_mwh = 0
    
    for h in hours:
        solar = (h['solar'] or 0) * factor
        nuc = h['nuclear'] if h['nuclear'] is not None else 1770
        demand = h['demand']
        other_must_run = 300
        available_for_nuc = demand - solar - other_must_run
        
        if available_for_nuc < nuc_min_mw:
            actual_nuc = max(0, available_for_nuc)
            lost = nuc - actual_nuc
            if lost > 0:
                curtail_hours += 1
                lost_mwh += lost
                nuc_output_mwh += actual_nuc
            else:
                nuc_output_mwh += nuc
        elif available_for_nuc < nuc:
            curtail_hours += 1
            lost_mwh += (nuc - available_for_nuc)
            nuc_output_mwh += available_for_nuc
        else:
            nuc_output_mwh += nuc
    
    cf = nuc_output_mwh / (nuc_nameplate * len(hours))
    full_cost = (fixed_all * 1e6 + var_per_mwh * nuc_output_mwh) / nuc_output_mwh if nuc_output_mwh > 0 else float('inf')
    
    print("%-30s %12d %10.2f %7.0f%% %11.1f" % (name, curtail_hours, lost_mwh/1e6, cf*100, full_cost))

print()
print("=" * 70)
print("SUMMER BREAK SCENARIOS (June-August shutdown)")
print("=" * 70)

summer_months = {6, 7, 8}
summer_hours_count = sum(1 for h in hours if int(h['t'][5:7]) in summer_months)
actual_summer_nuc = sum(h['nuclear'] for h in hours if int(h['t'][5:7]) in summer_months and h['nuclear'] is not None)

print("Summer hours (Jun-Aug): %d" % summer_hours_count)
print("Current summer nuclear output: %.2f TWh" % (actual_summer_nuc/1e6))
print()

for name, addon in scenarios:
    factor = (base_solar_mw + addon) / base_solar_mw
    nuc_output_mwh = 0
    
    for h in hours:
        month = int(h['t'][5:7])
        nuc = h['nuclear'] if h['nuclear'] is not None else 1770
        
        if month in summer_months:
            continue
        
        solar = (h['solar'] or 0) * factor
        demand = h['demand']
        other_must_run = 300
        available_for_nuc = demand - solar - other_must_run
        
        if available_for_nuc < nuc:
            actual_nuc = max(0, available_for_nuc)
            nuc_output_mwh += actual_nuc
        else:
            nuc_output_mwh += nuc
    
    cf = nuc_output_mwh / (nuc_nameplate * 8760)
    full_cost = (fixed_all * 1e6 + var_per_mwh * nuc_output_mwh) / nuc_output_mwh if nuc_output_mwh > 0 else float('inf')
    
    print("%-30s CF=%5.0f%%  cost=%6.1f EUR/MWh  output=%.2f TWh" % (name, cf*100, full_cost, nuc_output_mwh/1e6))

print()
print("=" * 70)
print("REVENUE vs COST - PROFIT/LOSS SCENARIOS")
print("=" * 70)

prices = [h['price'] for h in hours if h['price'] is not None]
avg_price = np.mean(prices)
p10 = np.percentile(prices, 10)
p50 = np.percentile(prices, 50)
p90 = np.percentile(prices, 90)

print("2024 BG price: avg=%.1f, median=%.1f, P10=%.1f, P90=%.1f EUR/MWh" % (avg_price, p50, p10, p90))
print()

print("%5s %6s %12s %12s %12s %10s" % ("CF", "TWh", "Revenue", "Full OPEX", "Profit", "per MWh"))
print("-" * 60)
for cf in [0.83, 0.75, 0.65, 0.55, 0.50, 0.45, 0.40]:
    twh = nuc_nameplate * 8760 * cf / 1e6
    mwh = twh * 1e6
    revenue = avg_price * mwh / 1e6
    cost = fixed_all + var_per_mwh * mwh / 1e6
    profit = revenue - cost
    per_mwh = profit * 1e6 / mwh
    print("%5.0f%% %6.1f %11.0fM %11.0fM %+11.0fM %+9.1f" % (cf*100, twh, revenue, cost, profit, per_mwh))

print()
print("=" * 70)
print("NUCLEAR DEATH THRESHOLD: when opex >= gas electricity cost")
print("=" * 70)
gas_price = 120
death_mwh = fixed_all * 1e6 / (gas_price - var_per_mwh)
death_twh = death_mwh / 1e6
death_cf = death_mwh / (nuc_nameplate * 8760)
print("Gas electricity cost: %d EUR/MWh" % gas_price)
print("Nuclear fixed costs: %d M EUR" % fixed_all)
print("Nuclear variable: %.1f EUR/MWh" % var_per_mwh)
print("Death CF: %.0f%% (%.1f TWh)" % (death_cf*100, death_twh))
print("At this point, replacing nuclear with gas imports is cheaper.")

print()
print("=" * 70)
print("FEB 15, 2026 - ZERO PRICE WINTER EVENT")
print("=" * 70)
with open('/home/yyoncho/Sources/claude/entso-e/data/BG/2026.json') as f:
    raw2026 = json.load(f)

from datetime import datetime, timedelta
def get_text(obj):
    if isinstance(obj, dict): return obj.get('text', '')
    return str(obj) if obj else ''
def ensure_list(obj):
    if obj is None: return []
    if isinstance(obj, list): return obj
    return [obj]

prices_2026 = {}
for ts in ensure_list(raw2026.get('prices', {}).get('TimeSeries', [])):
    for p in ensure_list(ts.get('Period', {})):
        start = get_text(p.get('timeInterval', {}).get('start', ''))
        if not start: continue
        start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
        for pt in ensure_list(p.get('Point', [])):
            pos = int(get_text(pt.get('position', '0')))
            price_raw = pt.get('price.amount') or pt.get('price', {})
            if isinstance(price_raw, dict):
                price_raw = price_raw.get('amount', '0')
            val = float(get_text(price_raw))
            hour_dt = start_dt + timedelta(hours=pos-1)
            key = hour_dt.strftime('%Y-%m-%d %H:00')
            prices_2026[key] = val

feb15_prices = {k: v for k, v in prices_2026.items() if k.startswith('2026-02-15')}
if feb15_prices:
    print("Feb 15, 2026 hourly prices (EUR/MWh):")
    for k in sorted(feb15_prices):
        print("  %s: %.2f" % (k, feb15_prices[k]))
    avg_feb15 = np.mean(list(feb15_prices.values()))
    zero_hours = sum(1 for v in feb15_prices.values() if v <= 1)
    print("  Average: %.1f, hours at/near zero: %d" % (avg_feb15, zero_hours))

with open('/home/yyoncho/Sources/claude/entso-e/data/RO/2026.json') as f:
    raw_ro = json.load(f)
prices_ro = {}
for ts in ensure_list(raw_ro.get('prices', {}).get('TimeSeries', [])):
    for p in ensure_list(ts.get('Period', {})):
        start = get_text(p.get('timeInterval', {}).get('start', ''))
        if not start: continue
        start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
        for pt in ensure_list(p.get('Point', [])):
            pos = int(get_text(pt.get('position', '0')))
            price_raw = pt.get('price.amount') or pt.get('price', {})
            if isinstance(price_raw, dict):
                price_raw = price_raw.get('amount', '0')
            val = float(get_text(price_raw))
            hour_dt = start_dt + timedelta(hours=pos-1)
            key = hour_dt.strftime('%Y-%m-%d %H:00')
            prices_ro[key] = val

feb15_ro = {k: v for k, v in prices_ro.items() if k.startswith('2026-02-15')}
if feb15_ro:
    avg_ro = np.mean(list(feb15_ro.values()))
    print()
    print("  Romania avg Feb 15: %.1f EUR/MWh" % avg_ro)
    print("  BG-RO spread: %.1f EUR/MWh (BG was %.0f cheaper)" % (avg_feb15 - avg_ro, avg_feb15 - avg_ro))

print()
print("=" * 70)
print("WINTER 2024 - SUNNY WINTER DAYS WITH LOW PRICES")
print("=" * 70)
winter_hours = [h for h in hours if int(h['t'][5:7]) in {1, 2, 11, 12}]
from collections import defaultdict
daily = defaultdict(lambda: {'solar': [], 'price': [], 'nuclear': []})
for h in winter_hours:
    day = h['t'][:10]
    daily[day]['solar'].append(h['solar'] or 0)
    daily[day]['price'].append(h['price'])
    if h['nuclear'] is not None:
        daily[day]['nuclear'].append(h['nuclear'])

sunny_winter = []
for day, vals in sorted(daily.items()):
    peak_solar = max(vals['solar'])
    avg_price_day = np.mean(vals['price'])
    min_price = min(vals['price'])
    if peak_solar > 2000:
        sunny_winter.append((day, peak_solar, avg_price_day, min_price))

print("Winter days (Jan/Feb/Nov/Dec) with peak solar > 2 GW: %d" % len(sunny_winter))
if sunny_winter:
    print("%-12s %12s %12s %12s" % ("Day", "Peak Solar", "Avg Price", "Min Price"))
    for day, solar, avg_p, min_p in sorted(sunny_winter, key=lambda x: x[2])[:10]:
        print("%-12s %10.0f MW %10.1f %10.1f" % (day, solar, avg_p, min_p))

all_winter_avg = np.mean([h['price'] for h in winter_hours])
sunny_avg = np.mean([x[2] for x in sunny_winter]) if sunny_winter else 0
print()
print("All winter avg price: %.1f EUR/MWh" % all_winter_avg)
print("Sunny winter avg price: %.1f EUR/MWh" % sunny_avg)
print("Price discount on sunny winter days: %.1f EUR/MWh" % (all_winter_avg - sunny_avg))
