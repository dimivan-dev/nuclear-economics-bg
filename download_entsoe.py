#!/usr/bin/env python3
"""
Configurable ENTSOE downloader for any countries.

Easy to use - just modify COUNTRIES dict to specify which countries to download.

Example:
  COUNTRIES = {
      'BG': {'name': 'Bulgaria', 'eic': '10YCA-BULGARIA-R'},
      'FR': {'name': 'France', 'eic': '10YFR-RTE------C'},
      'DE': {'name': 'Germany', 'eic': '10YDE-RWENET---L'},
  }

This will create:
  data/BG/2015.json
  data/BG/2016.json
  ...
  data/FR/2015.json
  data/FR/2016.json
  ...
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

# Configuration
ENTSOE_API_TOKEN = os.getenv('ENTSOE_API_TOKEN')
DATA_DIR = Path(os.getenv('DATA_DIR', './data'))
START_YEAR = int(os.getenv('START_DATE', '2015-01-01').split('-')[0])
END_YEAR = int(os.getenv('END_DATE', '2025-12-31').split('-')[0])

BASE_URL = 'https://web-api.tp.entsoe.eu/api'
DELAY_MS = 300

# ============================================================================
# MODIFY THIS SECTION TO CHANGE WHICH COUNTRIES TO DOWNLOAD
# ============================================================================

COUNTRIES = {
    'BG': {'name': 'Bulgaria', 'eic': '10YCA-BULGARIA-R'},
    'RO': {'name': 'Romania', 'eic': '10YRO-TEL------P'},
    'RS': {'name': 'Serbia', 'eic': '10YCS-SERBIA---S'},
    'TR': {'name': 'Turkey', 'eic': '10YTR-TEIAS----W'},
    'GR': {'name': 'Greece', 'eic': '10YGR-HTSO-----Y'},
    'MK': {'name': 'North Macedonia', 'eic': '10YMK-MEPSO----J'},
    'AL': {'name': 'Albania', 'eic': '10YAL-KESH-----5'},
    'XK': {'name': 'Kosovo', 'eic': '10YXK-KESCO----J'},
}

# Define interconnections between countries (e.g., Bulgaria to neighbors)
# Format: 'FROM-TO': (from_eic, to_eic, 'Label')
# Leave empty dict {} to skip interconnections
INTERCONNECTIONS = {
    'BG-RO': ('10YCA-BULGARIA-R', '10YRO-TEL------P', 'Bulgaria-Romania'),
    'BG-RS': ('10YCA-BULGARIA-R', '10YCS-SERBIA---S', 'Bulgaria-Serbia'),
    'BG-TR': ('10YCA-BULGARIA-R', '10YTR-TEIAS----W', 'Bulgaria-Turkey'),
    'BG-GR': ('10YCA-BULGARIA-R', '10YGR-IPEX-----L', 'Bulgaria-Greece'),
    'BG-MK': ('10YCA-BULGARIA-R', '10YMK-MEPSO----J', 'Bulgaria-N.Macedonia'),
}

# ============================================================================

last_request_time = 0


def rate_limited_request(url: str) -> str:
    global last_request_time
    now = time.time() * 1000
    elapsed = now - last_request_time
    if elapsed < DELAY_MS:
        time.sleep((DELAY_MS - elapsed) / 1000)
    last_request_time = time.time() * 1000

    response = requests.get(url, timeout=120)
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text[:200]}")
    return response.text


def format_date(dt: datetime) -> str:
    return dt.strftime('%Y%m%d%H%M')


def parse_xml_to_dict(xml_str: str) -> dict:
    """Parse ENTSOE XML response to dictionary."""
    try:
        root = ET.fromstring(xml_str)
        for elem in root.iter():
            if '}' in elem.tag:
                elem.tag = elem.tag.split('}', 1)[1]
        return root_to_dict(root)
    except Exception as e:
        logger.warning(f"      Failed to parse XML: {e}")
        return {}


def root_to_dict(element):
    """Convert XML element to dictionary."""
    result = {}
    if element.text and element.text.strip():
        result['text'] = element.text.strip()
    if element.attrib:
        result.update({f'@{k}': v for k, v in element.attrib.items()})
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


def download_generation(country_code: str, year: int) -> dict:
    """Download actual generation."""
    year_start = datetime(year, 1, 1)
    year_end = datetime(year, 12, 31, 23, 59)
    eic = COUNTRIES[country_code]['eic']

    try:
        params = {
            'securityToken': ENTSOE_API_TOKEN,
            'documentType': 'A75',
            'processType': 'A16',
            'in_Domain': eic,
            'periodStart': format_date(year_start),
            'periodEnd': format_date(year_end),
        }
        url = f"{BASE_URL}?{urlencode(params)}"
        xml = rate_limited_request(url)
        return parse_xml_to_dict(xml)
    except Exception as e:
        logger.warning(f"      Generation error: {e}")
        return {}


def download_prices(country_code: str, year: int) -> dict:
    """Download day-ahead prices."""
    year_start = datetime(year, 1, 1)
    year_end = datetime(year, 12, 31, 23, 59)
    eic = COUNTRIES[country_code]['eic']

    try:
        params = {
            'securityToken': ENTSOE_API_TOKEN,
            'documentType': 'A44',
            'in_Domain': eic,
            'out_Domain': eic,
            'periodStart': format_date(year_start),
            'periodEnd': format_date(year_end),
        }
        url = f"{BASE_URL}?{urlencode(params)}"
        xml = rate_limited_request(url)
        return parse_xml_to_dict(xml)
    except Exception as e:
        logger.warning(f"      Prices error: {e}")
        return {}


def download_capacity(country_code: str, year: int) -> dict:
    """Download installed capacity."""
    year_start = datetime(year, 1, 1)
    year_end = datetime(year, 12, 31, 23, 59)
    eic = COUNTRIES[country_code]['eic']

    try:
        params = {
            'securityToken': ENTSOE_API_TOKEN,
            'documentType': 'A68',
            'processType': 'A33',
            'in_Domain': eic,
            'periodStart': format_date(year_start),
            'periodEnd': format_date(year_end),
        }
        url = f"{BASE_URL}?{urlencode(params)}"
        xml = rate_limited_request(url)
        return parse_xml_to_dict(xml)
    except Exception as e:
        logger.warning(f"      Capacity error: {e}")
        return {}


def download_water_storage(country_code: str, year: int) -> dict:
    """Download water reservoir levels."""
    year_start = datetime(year, 1, 1)
    year_end = datetime(year, 12, 31, 23, 59)
    eic = COUNTRIES[country_code]['eic']

    try:
        params = {
            'securityToken': ENTSOE_API_TOKEN,
            'documentType': 'A72',
            'processType': 'A16',
            'in_Domain': eic,
            'periodStart': format_date(year_start),
            'periodEnd': format_date(year_end),
        }
        url = f"{BASE_URL}?{urlencode(params)}"
        xml = rate_limited_request(url)
        return parse_xml_to_dict(xml)
    except Exception as e:
        logger.warning(f"      Water storage error: {e}")
        return {}


def download_crossborder_flows(year: int) -> dict:
    """Download cross-border flows defined in INTERCONNECTIONS."""
    year_start = datetime(year, 1, 1)
    year_end = datetime(year, 12, 31, 23, 59)
    all_flows = {}

    for flow_key, (from_eic, to_eic, label) in INTERCONNECTIONS.items():
        try:
            params = {
                'securityToken': ENTSOE_API_TOKEN,
                'documentType': 'A11',
                'in_Domain': from_eic,
                'out_Domain': to_eic,
                'periodStart': format_date(year_start),
                'periodEnd': format_date(year_end),
            }
            url = f"{BASE_URL}?{urlencode(params)}"
            xml = rate_limited_request(url)
            all_flows[label] = parse_xml_to_dict(xml)
        except Exception as e:
            logger.warning(f"      Flow {label} error: {e}")

    return all_flows


def download_year(year: int):
    """Download all data for all countries for one year."""
    logger.info(f"\n{'='*80}")
    logger.info(f"YEAR {year}")
    logger.info(f"{'='*80}")

    # Download for each country
    for country_code, country_info in COUNTRIES.items():
        logger.info(f"\n{country_info['name']}:")

        country_data = {
            'year': year,
            'country': country_code,
            'name': country_info['name'],
            'generation': download_generation(country_code, year),
            'prices': download_prices(country_code, year),
            'capacity': download_capacity(country_code, year),
            'water_storage': download_water_storage(country_code, year),
        }

        # Create country directory
        country_dir = DATA_DIR / country_code
        country_dir.mkdir(parents=True, exist_ok=True)

        # Save as data/COUNTRY/YEAR.json
        output_file = country_dir / f'{year}.json'
        with open(output_file, 'w') as f:
            json.dump(country_data, f, indent=2)

        size_mb = output_file.stat().st_size / 1024 / 1024
        logger.info(f"  ✓ Saved to {output_file.relative_to(DATA_DIR)} ({size_mb:.1f} MB)")

    # Download and save interconnections
    if INTERCONNECTIONS:
        logger.info(f"\nInterconnections:")
        flows = download_crossborder_flows(year)

        # Save to a special 'FLOWS' directory
        flows_dir = DATA_DIR / 'FLOWS'
        flows_dir.mkdir(parents=True, exist_ok=True)

        flows_file = flows_dir / f'{year}.json'
        with open(flows_file, 'w') as f:
            json.dump(flows, f, indent=2)

        size_mb = flows_file.stat().st_size / 1024 / 1024
        logger.info(f"  ✓ Saved to {flows_file.relative_to(DATA_DIR)} ({size_mb:.1f} MB)")


def main():
    logger.info("=" * 80)
    logger.info("ENTSOE Data Downloader")
    logger.info("=" * 80)
    logger.info(f"Countries: {', '.join([c['name'] for c in COUNTRIES.values()])}")
    logger.info(f"Years: {START_YEAR}-{END_YEAR}")
    logger.info(f"Data: Generation, Prices, Capacity, Water Storage")
    if INTERCONNECTIONS:
        logger.info(f"Interconnections: {len(INTERCONNECTIONS)} flows")

    if not ENTSOE_API_TOKEN:
        logger.error("ERROR: ENTSOE_API_TOKEN not set in .env")
        exit(1)

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Download year by year
    for year in range(START_YEAR, END_YEAR + 1):
        download_year(year)

    logger.info("\n" + "=" * 80)
    logger.info("✓ DOWNLOAD COMPLETE!")
    logger.info("=" * 80)

    # Summary
    logger.info(f"\nData structure:")
    logger.info(f"  data/")
    for country_code in COUNTRIES.keys():
        logger.info(f"    {country_code}/")
        logger.info(f"      2015.json, 2016.json, ..., {END_YEAR}.json")
    if INTERCONNECTIONS:
        logger.info(f"    FLOWS/")
        logger.info(f"      2015.json, 2016.json, ..., {END_YEAR}.json")


if __name__ == '__main__':
    main()
