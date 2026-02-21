#!/usr/bin/env python3
"""
Pre-process raw ENTSOE data into compact JSON for the browser app.

Reads:
  data/BG/{year}.json            (generation + prices)
  data/BG_DEMAND/{year}.json     (demand)
  data/BG_BILATERAL/{year}.json  (cross-border flows)

Outputs:
  app/public/data/{year}.json

Output format:
  {
    "meta": { "maxExport": { "ro": 1891, "tr": 490, "gr": 700 } },
    "hours": [
      {"t":"2024-01-01T00:00Z","demand":4800,"gen":5200,"net":400,"price":85.5,
       "nuclear":2000,"coal":800,...,"flows":{"ro":123,"tr":-45,"gr":67}}
    ]
  }
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

DATA_DIR = Path('./data')
OUTPUT_DIR = Path('./data')
YEARS = range(2015, 2027)

# PSR type -> category
PSR_MAP = {
    'B14': 'nuclear',
    'B02': 'coal',
    'B05': 'coal',
    'B04': 'gas',
    'B10': 'hydro',
    'B11': 'hydro',
    'B12': 'hydro',
    'B16': 'solar',
    'B19': 'wind',
    'B01': 'biomass',
    'B17': 'biomass',
}

GEN_CATEGORIES = ['nuclear', 'coal', 'gas', 'hydro', 'solar', 'wind', 'biomass']
FLOW_COUNTRIES = ['ro', 'tr', 'gr']


def get_text(obj):
    """Extract text value from ENTSOE parsed dict."""
    if isinstance(obj, dict):
        return obj.get('text', '')
    return str(obj) if obj is not None else ''


def ensure_list(obj):
    """Ensure value is a list (ENTSOE XML can produce single dict or list)."""
    if obj is None:
        return []
    if isinstance(obj, list):
        return obj
    return [obj]


def parse_iso(s):
    """Parse ISO timestamp string to datetime."""
    return datetime.fromisoformat(s.replace('Z', '+00:00'))


def ts_key(dt):
    """Format datetime as compact timestamp key."""
    return dt.strftime('%Y-%m-%dT%H:%MZ')


def parse_points_by_timestamp(periods):
    """Parse periods (list of Period dicts) into {timestamp: value} using position offsets."""
    result = {}
    for period in periods:
        start_str = get_text(period.get('timeInterval', {}).get('start', ''))
        if not start_str:
            continue
        start_dt = parse_iso(start_str)
        points = ensure_list(period.get('Point'))
        for pt in points:
            pos = int(get_text(pt.get('position', '0')))
            # Quantity or price
            if 'quantity' in pt:
                val = float(get_text(pt.get('quantity', '0')))
            elif 'price.amount' in pt:
                val = float(get_text(pt.get('price.amount', '0')))
            elif 'price' in pt:
                val = float(get_text(pt.get('price', {}).get('amount', '0')))
            else:
                continue
            hour_dt = start_dt + timedelta(hours=pos - 1)
            result[ts_key(hour_dt)] = val
    return result


def parse_generation(gen_data):
    """Parse generation data into {category: {timestamp: MW}}."""
    result = {cat: {} for cat in GEN_CATEGORIES}

    ts_list = ensure_list(gen_data.get('TimeSeries'))
    for ts in ts_list:
        psr_type_obj = ts.get('MktPSRType', {})
        psr_code = get_text(psr_type_obj.get('psrType', ''))
        category = PSR_MAP.get(psr_code)
        if not category:
            continue

        periods = ensure_list(ts.get('Period', {}))
        values = parse_points_by_timestamp(periods)
        for key, val in values.items():
            result[category][key] = result[category].get(key, 0) + val

    return result


def parse_prices(price_data):
    """Parse price data into {timestamp: EUR/MWh}."""
    result = {}
    ts_list = ensure_list(price_data.get('TimeSeries'))
    for ts in ts_list:
        periods = ensure_list(ts.get('Period', {}))
        values = parse_points_by_timestamp(periods)
        result.update(values)
    return result


def parse_demand(demand_data):
    """Parse demand data into {timestamp: MW}."""
    result = {}
    ts_list = ensure_list(demand_data.get('TimeSeries'))
    for ts in ts_list:
        periods = ensure_list(ts.get('Period', {}))
        values = parse_points_by_timestamp(periods)
        result.update(values)
    return result


def parse_flow_direction(flow_data):
    """Parse one direction of cross-border flow into {timestamp: MW}."""
    if flow_data is None:
        return {}
    ts_list = ensure_list(flow_data.get('TimeSeries'))
    result = {}
    for ts in ts_list:
        periods = ensure_list(ts.get('Period', {}))
        values = parse_points_by_timestamp(periods)
        result.update(values)
    return result


def parse_bilateral_flows(bilateral_data):
    """Parse bilateral flow data into per-country {timestamp: net_MW}.

    Returns:
      flows: {country: {timestamp: net_flow}} where positive = BG exports
      max_export: {country: max_export_MW}
    """
    flows = {}
    max_export = {}

    for country in FLOW_COUNTRIES:
        country_data = bilateral_data.get(country, {})
        export_vals = parse_flow_direction(country_data.get('export'))
        import_vals = parse_flow_direction(country_data.get('import'))

        # Compute net: positive = BG exports to country
        all_ts = set(export_vals.keys()) | set(import_vals.keys())
        net = {}
        peak_export = 0
        for ts in all_ts:
            exp = export_vals.get(ts, 0)
            imp = import_vals.get(ts, 0)
            n = exp - imp
            net[ts] = n
            if exp > peak_export:
                peak_export = exp

        flows[country] = net
        max_export[country] = round(peak_export, 1)

    return flows, max_export


def process_year(year):
    gen_file = DATA_DIR / 'BG' / '{}.json'.format(year)
    demand_file = DATA_DIR / 'BG_DEMAND' / '{}.json'.format(year)
    bilateral_file = DATA_DIR / 'BG_BILATERAL' / '{}.json'.format(year)

    if not gen_file.exists():
        print('  {}: missing generation data, skipping'.format(year))
        return
    if not demand_file.exists():
        print('  {}: missing demand data, skipping'.format(year))
        return

    with open(gen_file) as f:
        gen_raw = json.load(f)
    with open(demand_file) as f:
        demand_raw = json.load(f)

    # Parse bilateral flows if available
    bilateral_data = {}
    if bilateral_file.exists():
        with open(bilateral_file) as f:
            bilateral_data = json.load(f)

    # Parse all data into timestamp-indexed dicts
    gen_by_cat = parse_generation(gen_raw.get('generation', {}))
    prices = parse_prices(gen_raw.get('prices', {}))
    demand = parse_demand(demand_raw)
    country_flows, max_export = parse_bilateral_flows(bilateral_data)

    # Collect all timestamps across all data sources
    all_keys = set()
    for cat in GEN_CATEGORIES:
        all_keys.update(gen_by_cat[cat].keys())
    all_keys.update(prices.keys())
    all_keys.update(demand.keys())
    for country in FLOW_COUNTRIES:
        all_keys.update(country_flows.get(country, {}).keys())

    # Sort by timestamp
    sorted_keys = sorted(all_keys)

    records = []
    for key in sorted_keys:
        dem = demand.get(key)
        price = prices.get(key)

        gen_vals = {}
        total_gen = 0
        for cat in GEN_CATEGORIES:
            val = gen_by_cat[cat].get(key, 0)
            gen_vals[cat] = round(val, 1)
            total_gen += val

        dem_val = round(dem, 1) if dem is not None else None
        net = round(total_gen - dem, 1) if dem is not None else None

        # Per-country flows
        flows = {}
        for country in FLOW_COUNTRIES:
            flow_val = country_flows.get(country, {}).get(key)
            flows[country] = round(flow_val, 1) if flow_val is not None else 0

        record = {
            't': key,
            'demand': dem_val,
            'gen': round(total_gen, 1),
            'net': net,
            'price': round(price, 2) if price is not None else None,
            'flows': flows,
        }
        record.update(gen_vals)
        records.append(record)

    # Fix nuclear data gaps: ENTSOE often omits hours from the nuclear
    # timeseries while other sources (demand, flows) cover them.  Kozloduy
    # runs at near-constant output, so forward-fill from the last known value.
    nuc_keys = set(gen_by_cat['nuclear'].keys())
    nuc_gaps = 0
    last_nuc = None
    for rec in records:
        if rec['t'] in nuc_keys:
            last_nuc = rec['nuclear']
        elif rec['nuclear'] == 0 and last_nuc is not None:
            rec['nuclear'] = last_nuc
            rec['gen'] = round(rec['gen'] + last_nuc, 1)
            if rec['demand'] is not None:
                rec['net'] = round(rec['gen'] - rec['demand'], 1)
            nuc_gaps += 1
    if nuc_gaps:
        print('    filled {} nuclear data gaps via forward-fill'.format(nuc_gaps))

    # Write output with metadata
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_file = OUTPUT_DIR / '{}.json'.format(year)
    output = {
        'meta': {
            'maxExport': max_export,
        },
        'hours': records,
    }
    with open(output_file, 'w') as f:
        json.dump(output, f, separators=(',', ':'))

    size_kb = output_file.stat().st_size / 1024
    valid = sum(1 for r in records if r['demand'] is not None)
    flow_hours = sum(1 for r in records if any(r['flows'].get(c, 0) != 0 for c in FLOW_COUNTRIES))
    print('  {}: {} hours ({} with demand, {} with flows), {:.0f} KB'.format(
        year, len(records), valid, flow_hours, size_kb))
    print('    max export: {}'.format(max_export))


def main():
    print('Pre-processing ENTSOE data for browser app')
    for year in YEARS:
        process_year(year)
    print('Done!')


if __name__ == '__main__':
    main()
