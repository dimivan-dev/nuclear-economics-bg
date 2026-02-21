#!/usr/bin/env python3
"""
Download Bulgaria actual total load (demand) data from ENTSOE.

Document type A65, process type A16.
Saves to data/BG_DEMAND/{year}.json
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
EIC = '10YCA-BULGARIA-R'
START_YEAR = 2015
END_YEAR = 2025

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


def parse_xml_to_dict(xml_str: str) -> dict:
    try:
        root = ET.fromstring(xml_str)
        for elem in root.iter():
            if '}' in elem.tag:
                elem.tag = elem.tag.split('}', 1)[1]
        return root_to_dict(root)
    except Exception as e:
        logger.warning(f"Failed to parse XML: {e}")
        return {}


def root_to_dict(element):
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


def format_date(dt: datetime) -> str:
    return dt.strftime('%Y%m%d%H%M')


def download_demand(year: int) -> dict:
    year_start = datetime(year, 1, 1)
    year_end = datetime(year, 12, 31, 23, 59)

    params = {
        'securityToken': ENTSOE_API_TOKEN,
        'documentType': 'A65',
        'processType': 'A16',
        'outBiddingZone_Domain': EIC,
        'periodStart': format_date(year_start),
        'periodEnd': format_date(year_end),
    }
    url = f"{BASE_URL}?{urlencode(params)}"
    xml = rate_limited_request(url)
    return parse_xml_to_dict(xml)


def main():
    logger.info("ENTSOE Demand Downloader - Bulgaria")
    logger.info(f"Years: {START_YEAR}-{END_YEAR}")

    if not ENTSOE_API_TOKEN:
        logger.error("ENTSOE_API_TOKEN not set in .env")
        exit(1)

    output_dir = DATA_DIR / 'BG_DEMAND'
    output_dir.mkdir(parents=True, exist_ok=True)

    for year in range(START_YEAR, END_YEAR + 1):
        output_file = output_dir / f'{year}.json'
        if output_file.exists():
            size_mb = output_file.stat().st_size / 1024 / 1024
            logger.info(f"  {year}: already exists ({size_mb:.1f} MB), skipping")
            continue

        logger.info(f"  Downloading {year}...")
        try:
            data = download_demand(year)
            with open(output_file, 'w') as f:
                json.dump(data, f, indent=2)
            size_mb = output_file.stat().st_size / 1024 / 1024
            logger.info(f"  {year}: saved ({size_mb:.1f} MB)")
        except Exception as e:
            logger.error(f"  {year}: FAILED - {e}")

    logger.info("Done!")


if __name__ == '__main__':
    main()
