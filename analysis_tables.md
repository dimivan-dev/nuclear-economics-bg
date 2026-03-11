# Analysis Data Tables

Supporting data for the nuclear economics article. All modeled on 2025 ENTSOE hourly data.

## Price Compression Model

Merit-order model using 2025 actual market data:
- Solar generation scaled from 5.3 GW baseline
- Merit order slope: 0.018 EUR/MWh per MW (2025 regression, R²=0.29)
- Solar curtailment: prices floor at 0 EUR/MWh (operators curtail solar at negative prices)
- Battery effect: daily energy-balance dispatch — batteries charge from zero-price solar hours, discharge into highest-price hours. When battery energy covers the full non-solar gap, prices drop to battery cycling cost (~15 EUR/MWh). Remaining hours capped at coal full cost (88 EUR/MWh).
- Export capacity: ~2,800 MW total interconnector
- 2025 caveat: Unit 6 offline May-Aug → prices ~10% higher than normal. All numbers are conservative.

### Monthly Average Prices (EUR/MWh) by Scenario

| Scenario | Jan | Feb | Mar | Apr | May | Jun | Jul | Aug | Sep | Oct | Nov | Dec | Year |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 5.3 GW (today, no batt.) | 139 | 156 | 105 | 87 | 87 | 87 | 102 | 78 | 95 | 90 | 92 | 91 | 101 |
| 5.3 GW + 16 GWh | 86 | 87 | 71 | 57 | 60 | 58 | 76 | 57 | 63 | 82 | 85 | 85 | 72 |
| 10 GW + 16 GWh | 84 | 85 | 58 | 47 | 47 | 35 | 53 | 35 | 43 | 75 | 80 | 80 | 60 |
| **14.3 GW + 16 GWh** | **82** | **82** | **55** | **40** | **38** | **28** | **38** | **29** | **35** | **64** | **73** | **73** | **53** |
| 16 GW + 16 GWh | 80 | 80 | 53 | 38 | 36 | 27 | 36 | 27 | 33 | 58 | 70 | 71 | 51 |
| 20 GW + 16 GWh | 77 | 76 | 50 | 36 | 32 | 24 | 32 | 24 | 29 | 48 | 63 | 62 | 46 |
| 14.3 GW + 32 GWh | 81 | 81 | 49 | 31 | 33 | 15 | 23 | 16 | 26 | 64 | 73 | 73 | 47 |
| 20 GW + 32 GWh | 75 | 73 | 41 | 25 | 23 | 10 | 15 | 12 | 19 | 45 | 62 | 60 | 38 |

### Months Below Nuclear Average Cost (46 EUR/MWh)

| Scenario | Uneconomic months |
|---|---|
| 5.3 GW (today) | — |
| 5.3 GW + 16 GWh | — |
| 10 GW + 16 GWh | Jun, Aug |
| **14.3 GW + 16 GWh** | **Apr–Sep** |
| 16 GW + 16 GWh | Apr–Sep |
| 20 GW + 16 GWh | Apr–Sep |
| 14.3 GW + 32 GWh | Apr–Sep |
| 20 GW + 32 GWh | Mar–Sep |

## Nuclear Annual P&L by Operating Strategy

Fixed cost: 617 M EUR/year. Variable cost: 6.8 EUR/MWh. Total OPEX: 723 M EUR/year (excl. SES fund).

### 14.3 GW Solar + 16 GWh Batteries (ESO 2034)

| Strategy | Revenue (M€) | Cost (M€) | Profit (M€) | CF | Rev/MWh |
|---|---:|---:|---:|---:|---:|
| 2×1000 MW all year | 916 | 735 | +182 | 99% | 52.9 |
| Reduced 1400 MW Jun-Aug | 876 | 726 | +150 | 90% | 54.7 |
| Reduced 1400 MW May-Sep | 844 | 720 | +124 | 85% | 55.7 |
| 1 reactor off Jun-Aug | 848 | 720 | +128 | 87% | 56.0 |
| 1 reactor off May-Sep | 796 | 710 | +86 | 79% | 58.0 |
| Combo (1 off Jun-Aug, reduced shoulder) | 800 | 711 | +89 | 84% | 57.7 |

### 14.3 GW Solar + 32 GWh Batteries

| Strategy | Revenue (M€) | Cost (M€) | Profit (M€) | CF | Rev/MWh |
|---|---:|---:|---:|---:|---:|
| 2×1000 MW all year | 816 | 735 | +82 | 99% | 47.1 |
| Reduced 1400 MW Jun-Aug | 786 | 726 | +60 | 90% | 49.1 |
| 1 reactor off Jun-Aug | 767 | 720 | +47 | 87% | 50.6 |
| 1 reactor off May-Sep | 721 | 710 | +11 | 79% | 52.6 |

### 20 GW Solar + 16 GWh Batteries

| Strategy | Revenue (M€) | Cost (M€) | Profit (M€) | CF | Rev/MWh |
|---|---:|---:|---:|---:|---:|
| 2×1000 MW all year | 797 | 735 | +63 | 99% | 46.1 |
| Reduced 1400 MW Jun-Aug | 763 | 726 | +37 | 90% | 47.6 |
| 1 reactor off Jun-Aug | 740 | 720 | +20 | 87% | 48.8 |
| 1 reactor off May-Sep | 696 | 710 | -15 | 79% | 50.7 |

### 20 GW Solar + 32 GWh Batteries

| Strategy | Revenue (M€) | Cost (M€) | Profit (M€) | CF | Rev/MWh |
|---|---:|---:|---:|---:|---:|
| 2×1000 MW all year | 662 | 735 | -73 | 99% | 38.2 |
| Reduced 1400 MW Jun-Aug | 646 | 726 | -80 | 90% | 40.3 |
| 1 reactor off Jun-Aug | 635 | 720 | -85 | 87% | 41.9 |
| 1 reactor off May-Sep | 605 | 710 | -105 | 79% | 44.1 |

## Cost vs Capacity Factor

| CF | Output (TWh) | Cost (EUR/MWh) |
|---:|---:|---:|
| 99% | 17.3 | 42 |
| 92% | 16.1 | 45 |
| 89% (2024) | 15.6 | 46 |
| 87% (1 reactor off 3 months) | 15.2 | 48 |
| 85% | 14.9 | 48 |
| 79% (1 reactor off 5 months) | 13.8 | 52 |
| 75% (1 reactor off 6 months) | 13.1 | 54 |
| 50% | 8.8 | 77 |
| 31% (gas parity) | 5.5 | 120 |

## Historical Capacity Factor

| Year | Output (TWh) | CF |
|---:|---:|---:|
| 2019 | 16.6 | 95% |
| 2020 | 16.7 | 95% |
| 2021 | 16.5 | 94% |
| 2022 | 16.5 | 94% |
| 2023 | 16.2 | 93% |
| 2024 | 15.6 | 89% |
| 2025 | 14.8 | 84% |

## OPEX Breakdown (2024 Annual Report, excl. SES fund)

| Category | EUR (M) |
|---|---:|
| Production (fuel, materials) | 79 |
| RAO/decommissioning funds | 161 |
| Grid access fees | 27 |
| O&M | 148 |
| Staff & social security | 200 |
| Depreciation | 107 |
| **Total OPEX** | **723** |

Fixed: 617 M EUR. Variable: ~6.8 EUR/MWh.
