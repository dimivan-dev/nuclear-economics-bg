#!/usr/bin/env python3
"""
Download bilateral cross-border physical flows for Bulgaria.

Downloads both directions (export and import) for each interconnection:
  BG <-> RO (Romania)
  BG <-> TR (Turkey)
  BG <-> GR (Greece)

Saves to data/BG_BILATERAL/{year}.json
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path
import logging
import requests
import xml.etree.ElementTree as ET
from urllib.parse import urlencode

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from dotenv import load_dotenv
load_dotenv()

ENTSOE_API_TOKEN = os.getenv('ENTSOE_API_TOKEN')
DATA_DIR = Path(os.getenv('DATA_DIR', './data'))
BASE_URL = 'https://web-api.tp.entsoe.eu/api'
DELAY_MS = 300
BG_EIC = '10YCA-BULGARIA-R'
START_YEAR = 2015
END_YEAR = 2025

# Neighbor EIC codes (Greece uses HTSO code for cross-border flows)
NEIGHBORS = {
    'ro': {'name': 'Romania', 'eic': '10YRO-TEL------P'},
    'tr': {'name': 'Turkey', 'eic': '10YTR-TEIAS----W'},
    'gr': {'name': 'Greece', 'eic': '10YGR-HTSO-----Y'},
}

last_request_time = 0


def rate_limited_request(url):
    global last_request_time
    now = time.time() * 1000
    elapsed = now - last_request_time
    if elapsed < DELAY_MS:
        time.sleep((DELAY_MS - elapsed) / 1000)
    last_request_time = time.time() * 1000

    response = requests.get(url, timeout=120)
    if response.status_code != 200:
        raise Exception('HTTP {}: {}'.format(response.status_code, response.text[:200]))
    return response.text


def parse_xml_to_dict(xml_str):
    try:
        root = ET.fromstring(xml_str)
        for elem in root.iter():
            if '}' in elem.tag:
                elem.tag = elem.tag.split('}', 1)[1]
        return root_to_dict(root)
    except Exception as e:
        logger.warning('Failed to parse XML: {}'.format(e))
        return {}


def root_to_dict(element):
    result = {}
    if element.text and element.text.strip():
        result['text'] = element.text.strip()
    if element.attrib:
        result.update({'@{}'.format(k): v for k, v in element.attrib.items()})
    children = {}
    for child in element:
        if '}' in child.tag:
            child.tag = child.tag.split('}', 1)[1]
        child_data = root_to_dict(child)
        if child.tag in children:
            if not isinstance(children[child.tag], list):
                children[child.tag] = [children[child.tag]]
            children[child.tag].append(child_data)
        else:
            children[child.tag] = child_data
    if children:
        result.update(children)
    return result if result else element.text


def format_date(dt):
    return dt.strftime('%Y%m%d%H%M')


def download_flow(in_domain, out_domain, year):
    """Download physical cross-border flow for one direction."""
    year_start = datetime(year, 1, 1)
    year_end = datetime(year, 12, 31, 23, 59)

    params = {
        'securityToken': ENTSOE_API_TOKEN,
        'documentType': 'A11',
        'in_Domain': in_domain,
        'out_Domain': out_domain,
        'periodStart': format_date(year_start),
        'periodEnd': format_date(year_end),
    }
    url = '{}?{}'.format(BASE_URL, urlencode(params))
    xml = rate_limited_request(url)
    data = parse_xml_to_dict(xml)

    # Check for "no data" response
    if 'Reason' in data or 'No matching data' in json.dumps(data):
        return None
    if 'TimeSeries' not in data:
        return None

    return data


def main():
    logger.info('ENTSOE Bilateral Flow Downloader - Bulgaria')
    logger.info('Years: {}-{}'.format(START_YEAR, END_YEAR))
    logger.info('Neighbors: {}'.format(', '.join(n['name'] for n in NEIGHBORS.values())))

    if not ENTSOE_API_TOKEN:
        logger.error('ENTSOE_API_TOKEN not set in .env')
        exit(1)

    output_dir = DATA_DIR / 'BG_BILATERAL'
    output_dir.mkdir(parents=True, exist_ok=True)

    for year in range(START_YEAR, END_YEAR + 1):
        output_file = output_dir / '{}.json'.format(year)
        if output_file.exists():
            size_kb = output_file.stat().st_size / 1024
            logger.info('  {}: already exists ({:.0f} KB), skipping'.format(year, size_kb))
            continue

        logger.info('  Downloading {}...'.format(year))
        year_data = {}

        for code, info in NEIGHBORS.items():
            neighbor_eic = info['eic']

            # BG -> Neighbor (export from BG)
            try:
                export_data = download_flow(BG_EIC, neighbor_eic, year)
                if export_data:
                    logger.info('    BG->{}: OK'.format(code.upper()))
                else:
                    logger.info('    BG->{}: no data'.format(code.upper()))
            except Exception as e:
                logger.warning('    BG->{}: FAILED - {}'.format(code.upper(), e))
                export_data = None

            # Neighbor -> BG (import to BG)
            try:
                import_data = download_flow(neighbor_eic, BG_EIC, year)
                if import_data:
                    logger.info('    {}->BG: OK'.format(code.upper()))
                else:
                    logger.info('    {}->BG: no data'.format(code.upper()))
            except Exception as e:
                logger.warning('    {}->BG: FAILED - {}'.format(code.upper(), e))
                import_data = None

            year_data[code] = {
                'name': info['name'],
                'export': export_data,
                'import': import_data,
            }

        with open(output_file, 'w') as f:
            json.dump(year_data, f, indent=2)

        size_kb = output_file.stat().st_size / 1024
        logger.info('  {}: saved ({:.0f} KB)'.format(year, size_kb))

    logger.info('Done!')


if __name__ == '__main__':
    main()
