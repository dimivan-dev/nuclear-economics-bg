# Analysis Data Tables

Supporting data for the nuclear economics article. All modeled on 2025 ENTSOE hourly data.

## Price Compression Model

Supply-demand balance model using 2025 actual market data:
- Solar generation scaled from 5.3 GW baseline
- Coal displaced first by extra solar before merit order compression
- Merit order slope: 0.018 EUR/MWh per MW (2025 regression, R²=0.29)
- Export capacity: ~2,800 MW total interconnector
- Battery effect: structural peak cap at coal full cost (88 EUR/MWh) for 16+ GWh

### Monthly Average Prices (EUR/MWh) by Scenario

| Scenario | Jan | Feb | Mar | Apr | May | Jun | Jul | Aug | Sep | Oct | Nov | Dec | Year |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 5.3 GW (today) | 134 | 150 | 95 | 73 | 78 | 68 | 83 | 64 | 81 | 81 | 90 | 89 | 90 |
| 5.3 GW + 16 GWh | 84 | 86 | 66 | 58 | 60 | 52 | 63 | 56 | 59 | 74 | 84 | 83 | 69 |
| 10 GW + 16 GWh | 78 | 79 | 59 | 50 | 50 | 39 | 46 | 44 | 49 | 65 | 78 | 76 | 59 |
| **14.3 GW + 16 GWh** | **73** | **72** | **49** | **37** | **38** | **19** | **20** | **27** | **33** | **55** | **72** | **70** | **47** |
| 16 GW + 16 GWh | 71 | 68 | 44 | 32 | 32 | 10 | 9 | 20 | 25 | 50 | 70 | 67 | 42 |
| 20 GW + 16 GWh | 65 | 60 | 31 | 18 | 18 | -13 | -17 | 2 | 7 | 39 | 63 | 60 | 28 |

### Hours Below Key Thresholds

| Scenario | Hours <0 EUR | Hours <7 EUR | Hours <46 EUR | Uneconomic months |
|---|---:|---:|---:|---|
| 5.3 GW (today) | 112 | 454 | 1,893 | — |
| 5.3 GW + 16 GWh | 14 | 179 | 1,399 | — |
| 10 GW + 16 GWh | 210 | 644 | 2,253 | Jun, Jul, Aug |
| **14.3 GW + 16 GWh** | **1,008** | **1,385** | **3,109** | **Apr–Sep** |
| 16 GW + 16 GWh | 1,270 | 1,623 | 3,376 | Mar–Sep |
| 20 GW + 16 GWh | 1,784 | 2,062 | 3,921 | Mar–Oct |

## Nuclear Annual P&L by Operating Strategy

Fixed cost: 617 M EUR/year. Variable cost: 6.8 EUR/MWh. Total OPEX: 723 M EUR/year (excl. SES fund).

### 14.3 GW Solar + 16 GWh Batteries (ESO 2034)

| Strategy | Revenue (M€) | Cost (M€) | Profit (M€) | CF | Rev/MWh |
|---|---:|---:|---:|---:|---:|
| 2×1000 MW all year | 816 | 735 | +82 | 99% | 47.2 |
| Reduced 1400 MW Jun-Aug | 774 | 730 | +44 | 90% | 49.4 |
| Reduced 1400 MW May-Sep | 747 | 727 | +20 | 85% | 50.4 |
| 1 reactor off Jun-Aug | 735 | 724 | +11 | 87% | 48.5 |
| 1 reactor off May-Sep | 691 | 719 | -28 | 79% | 50.2 |
| Combo (1 off Jun-Aug, reduced shoulder) | 718 | 723 | -5 | 84% | 49.0 |

### 16 GW Solar + 16 GWh Batteries

| Strategy | Revenue (M€) | Cost (M€) | Profit (M€) | CF | Rev/MWh |
|---|---:|---:|---:|---:|---:|
| 2×1000 MW all year | 721 | 735 | -14 | 99% | 41.6 |
| Reduced 1400 MW Jun-Aug | 688 | 730 | -42 | 90% | 43.8 |
| 1 reactor off Jun-Aug | 660 | 724 | -64 | 87% | 43.6 |
| 1 reactor off May-Sep | 623 | 719 | -96 | 79% | 45.2 |

### 20 GW Solar + 16 GWh Batteries

| Strategy | Revenue (M€) | Cost (M€) | Profit (M€) | CF | Rev/MWh |
|---|---:|---:|---:|---:|---:|
| 2×1000 MW all year | 482 | 735 | -253 | 99% | 27.8 |
| 1 reactor off Jun-Aug | 502 | 720 | -218 | 87% | 33.1 |
| 1 reactor off Apr-Sep | 468 | 706 | -238 | 75% | 35.8 |

## Weekend Summer Day Profile (Jun-Aug average)

Average hourly price on weekend summer days (EUR/MWh):

| Hour | 5.3 GW | 10 GW | 14.3 GW | 20 GW |
|---:|---:|---:|---:|---:|
| 0 | 85 | 85 | 85 | 85 |
| 4 | 52 | 33 | 19 | 12 |
| 6 | 13 | -6 | -48 | -114 |
| 8 | 4 | -11 | -46 | -115 |
| 10 | 4 | -2 | -19 | -72 |
| 12 | 2 | 1 | -13 | -46 |
| 14 | 23 | 6 | -4 | -33 |
| 16 | 108 | 90 | 63 | 43 |
| 18 | 118 | 95 | 79 | 64 |
| 20 | 120 | 117 | 113 | 107 |
| 22 | 94 | 94 | 94 | 94 |

## Nuclear Daily P&L — Weekend Summer Day

Revenue per MW per day vs cost of 1,104 EUR/MW/day (= 46 EUR/MWh × 24h):

| Solar | Revenue | Profit/Loss | Profitable hours |
|---|---:|---:|---:|
| 5.3 GW (today) | 1,368 | +264 | 14/24 |
| 10 GW | 1,106 | +2 | 12/24 |
| 14.3 GW (no batteries) | 776 | -328 | 12/24 |
| 14.3 GW + peak cap | 724 | -380 | 12/24 |
| 20 GW | 180 | -924 | 11/24 |

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
