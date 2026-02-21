# Nuclear Economics in Bulgaria

Analysis of Kozloduy NPP's economic viability under growing solar penetration, based on ENTSOE market data and Kozloduy's actual expense reports.

## Article

**[Slow but Inevitable: The Economic Death of Nuclear in Bulgaria](nuclear_article.md)**

Key findings:
- Kozloduy's real OPEX is **723 M EUR/year** (excluding SES fund levy), with **617 M EUR fixed costs**
- At 2024 CF of 89%, cost is 46.5 EUR/MWh — but drops to 71 EUR/MWh at CF 55%
- ESO projects 14.8 GW new solar + 5.2 GW batteries by 2034
- Nuclear curtailment extends April-October, not just summer
- Gas parity (120 EUR/MWh) reached at CF 31%
- Feb 15, 2026: Bulgaria hit near-zero winter prices (avg 12.3 EUR/MWh) while Romania averaged 138 EUR/MWh

## Data

`data/` — Preprocessed hourly ENTSOE data (2015-2025) for Bulgaria: generation by source, prices, demand, cross-border flows.

## Scripts

- `preprocess.py` — Convert raw ENTSOE data to compact hourly JSON
- `bess_analysis.py` — Battery storage market impact analysis (merit order, LP arbitrage, saturation sweep)
- `nuclear_economics.py` — Nuclear cost modeling
- `download_entsoe.py` — ENTSOE API data downloader
- `download_demand.py` — Demand data downloader
- `download_bilateral_flows.py` — Cross-border flow downloader

## Sources

- [ENTSOE Transparency Platform](https://transparency.entsoe.eu/)
- [Kozloduy NPP 2024 Annual Report](screens/ksnip_20260220-221204.png) (expense table)
- [ESO 10-year Network Development Plan 2024-2033](https://www.eso.bg/fileObj.php?oid=5402)
