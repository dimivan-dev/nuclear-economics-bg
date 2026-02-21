# Slow but Inevitable: The Economic Death of Nuclear in Bulgaria

## Introduction

A nuclear power plant is like a factory with enormous rent and almost no raw material costs. Whether Kozloduy NPP produces one megawatt-hour or sixteen billion of them, it still pays the same salaries to thousands of employees, the same maintenance bills, the same decommissioning contributions, and the same depreciation on its life-extension investments. The actual fuel — uranium — is surprisingly cheap, just a few euros per megawatt-hour.

This cost structure creates a simple but unforgiving economic rule: nuclear power only works if the plant runs **a lot**. The industry measures this as the **capacity factor (CF)** — what percentage of the theoretical maximum the plant actually produces. At 90% CF, the massive fixed costs are spread over a lot of electricity, making each unit affordable. At 50% CF, those same costs are spread over half the output, roughly doubling the price per unit. There's no way around this math.

For decades, Kozloduy's two 1,000 MW reactors ran at 92-95% capacity factor, producing 16+ TWh per year. Electricity was always needed, the plant ran flat out, and the economics were excellent.

That model is now breaking — and the force breaking it cannot be stopped.

## 1. The Solar Tsunami

Bulgaria's installed solar capacity has reached ~5.3 GW in 2024. ESO's (the Bulgarian Transmission System Operator) 10-year network development plan projects **14.8 GW of new solar** and **5.2 GW of battery storage** by 2034, based on investor intentions already in the pipeline:

> „С ускореното навлизане на ВЕИ и липса на значителен промишлен товар в страната, необходимостта от принудително ограничаване работната мощност на АЕЦ през определени периоди в годината тепърва ще се увеличава."
>
> — ЕСО, Десетгодишен план за развитие на преносната мрежа 2024-2033

*("With the accelerated entry of renewables and the lack of significant industrial load in the country, the need to forcibly limit the operating capacity of the NPP during certain periods of the year will only increase.")*

ESO themselves acknowledge what the data shows: forced curtailment of nuclear is coming.

Bulgaria's participation in the EU Recovery and Resilience Plan will further accelerate this timeline. The investment incentives and regulatory fast-tracking mean the country will likely hit significant solar and storage milestones well before 2034. The 5.2 GW of planned battery storage — measured in GWh, roughly 16+ GWh — may arrive sooner than anyone expects.

### What Solar Does to Nuclear

Solar energy produces for free once installed. When solar floods the grid at midday, it pushes prices toward zero — sometimes below. Nuclear, which cannot economically ramp down for a few hours, keeps producing into this oversupplied market. Every sunny hour is an hour where Kozloduy either sells at near-zero prices or must physically curtail its output.

Using 2024 hourly ENTSOE data, we can model the impact:

![Solar Growth vs Nuclear Capacity Factor](charts/solar_vs_nuclear_cf.png)

| Solar installed | Curtailment hours/year | Lost output (TWh) | Nuclear CF | Cost (EUR/MWh) |
|---|---:|---:|---:|---:|
| 5.3 GW (2024 actual) | 726 | 0.7 | 86% | 48 |
| 7.3 GW (+2 GW) | 1,421 | 1.5 | 82% | 51 |
| 10.3 GW (+5 GW) | 2,012 | 2.8 | 74% | 55 |
| **14.3 GW (ESO 2034)** | **2,411** | **3.7** | **69%** | **59** |
| 20.3 GW | 2,787 | 4.5 | 64% | 63 |

### Not Just Summer — April to October

The common assumption is that solar only threatens nuclear during the three summer months. The reality is much broader. With 14+ GW of solar, curtailment extends across the entire **April-to-October period** — roughly 7 months. Shoulder months like April, May, September, and October have moderate demand but increasingly strong solar output. At 14.3 GW installed, midday solar generation in these months routinely exceeds total national demand minus nuclear minimum output.

This isn't a clean seasonal shutdown. It's a messy pattern of forced curtailment, partial-load operation, and uneconomic running hours spanning more than half the year. Nuclear plants are not designed for this — cycling damages components, increases maintenance costs, and shortens fuel rod life. Each curtailment hour isn't just lost revenue; it adds operational wear.

With April-October curtailment at ESO's projected solar levels:

| Solar installed | CF (with Apr-Oct curtailment) | Cost (EUR/MWh) | Annual output (TWh) |
|---|---:|---:|---:|
| 5.3 GW (2024) | 65% | 61 | 11.4 |
| 7.3 GW | 62% | 64 | 10.9 |
| 10.3 GW | 58% | 67 | 10.2 |
| **14.3 GW (ESO 2034)** | **55%** | **71** | **9.6** |
| 20.3 GW | 51% | 76 | 8.9 |

At ESO's 2034 projection with seasonal curtailment, Kozloduy's cost reaches **71 EUR/MWh** and output drops to 9.6 TWh — down from 15.6 TWh today.

### Batteries Make It Worse

ESO's plan includes 5.2 GW / ~16 GWh of battery storage. Batteries don't save nuclear — they deepen the problem. Batteries profit by charging when prices are low (solar midday) and discharging when prices are high (evening peak). This flattens the daily price curve: it slightly raises the midday floor but **crushes the evening peak** that nuclear relies on for its best revenue hours. With enough batteries, the lucrative evening spread disappears.

The Recovery and Resilience Plan creates strong investment incentives for storage. Bulgaria could reach multi-GWh battery capacity ahead of ESO's timeline, further accelerating the erosion of nuclear's evening price premium.

### You Cannot Stop the Tsunami

Even if Bulgaria were to freeze all domestic solar and wind construction tomorrow, the problem doesn't go away. Bulgaria, Romania, and Greece form a tightly coupled electricity market — prices typically track within 5 EUR/MWh across the region.

Greece is aggressively building wind farms. Romania is adding both wind and solar. Turkey's market is increasingly self-sufficient. Every GW of renewables installed by a neighbor suppresses the regional price that Bulgarian nuclear earns. The solar and wind tsunami is regional, not national. No amount of domestic policy can shield Kozloduy from the price effects of 50+ GW of renewables being built across the Balkans and Southeast Europe.

## 2. February 15, 2026: A Preview

On February 15, 2026, a Sunday, Bulgaria experienced near-zero electricity prices for almost the entire day — **in winter**.

![Feb 15, 2026: BG vs RO Prices](charts/feb15_2026_prices.png)

Bulgaria averaged **12.3 EUR/MWh** while Romania averaged **138.4 EUR/MWh** — a 126 EUR/MWh spread, with Bulgaria on the wrong side.

| Hour | Nuclear (MW) | Coal (MW) | Gas (MW) | Hydro (MW) | Wind (MW) | BG Price | RO Price |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 00:00 | 1,904 | 1,099 | 313 | 360 | 383 | 10.0 | 99.3 |
| 06:00 | 1,904 | 1,094 | 313 | 770 | 413 | 0.0 | 101.3 |
| 10:00 | 1,904 | 1,118 | 308 | 586 | 196 | 2.5 | 108.9 |
| 14:00 | 1,903 | 1,098 | 313 | 739 | 323 | 0.2 | 216.1 |
| 18:00 | 1,905 | 1,145 | 312 | 1,134 | 288 | 9.2 | 212.0 |
| 22:00 | 1,905 | 1,099 | 320 | 635 | 468 | 10.0 | 197.5 |

The cause: **3,200 MW of must-run generation** (nuclear 1,904 + lignite ~1,100 + gas CHP ~310) against ~3,800 MW demand, with 300-470 MW of wind on top. Interconnector capacity to Romania was saturated — Bulgaria couldn't export its surplus.

This happened with only **350 MW of wind**. The grid collapsed into surplus not because of massive renewable generation, but because of **nuclear and coal inflexibility**. Kozloduy's 1,904 MW runs 24/7 — it cannot reduce output for a single day. Neither can lignite plants with minimum stable generation requirements.

Compare with Greece on the same day: 3,400 MW of wind, yet prices stayed at 38-142 EUR/MWh. Greece has a flexible gas fleet that ramps down when renewables ramp up. Bulgaria doesn't.

### The Export Market Is Gone

In 2015-2017, Bulgaria could profitably export surplus baseload power to neighbors. Those days are over. Romania is building its own solar fleet. Greece has massive wind. The neighbors that once absorbed Bulgaria's excess generation are becoming competitors. When Bulgaria had surplus on Feb 15, 2026, it couldn't sell it at any price — the interconnectors were full and nobody needed it.

As solar and wind grow across the entire region, these export-blocked, near-zero-price events will become routine.

## 3. Winter Under Threat

Nuclear's traditional stronghold is winter: solar is minimal, demand peaks, prices are highest. But even this is eroding.

**Greek and Romanian wind** competes directly with Bulgarian nuclear during winter months. On windy winter days, regional prices face the same kind of oversupply pressure that solar creates in summer.

In 2024, 20 winter days already had solar peaks above 2 GW in Bulgaria. Some showed prices of 60-69 EUR/MWh — on sunny winter days, even today's modest solar fleet pushes prices uncomfortably low. As solar grows, these days become the norm. And on windy winter days, Greek and Romanian wind does the same job.

The result: nuclear's "safe" selling season is shrinking from both ends — solar eats the shoulder months and summer, regional wind eats into winter.

## 4. Unit 6 Reliability

Between December 2025 and February 2026, Unit 6 experienced multiple unplanned shutdowns. Each outage carries costs beyond lost generation: emergency response, inspection, regulatory delays on restart.

The declining capacity factor trend is already visible:

![Historical Capacity Factor](charts/historical_cf.png)

| Year | Output (TWh) | CF |
|---:|---:|---:|
| 2019 | 16.6 | 95% |
| 2020 | 16.7 | 95% |
| 2021 | 16.5 | 94% |
| 2022 | 16.5 | 94% |
| 2023 | 16.2 | 93% |
| **2024** | **15.6** | **89%** |
| **2025** | **14.8** | **84%** |

From 16.7 TWh in 2020 to 14.8 TWh in 2025 — a drop of 1.9 TWh (11%) in five years, and the decline is accelerating. Note that 2025 ENTSOE data is preliminary — the final numbers, once released, are expected to be worse. Less production from the same fixed cost base means the per-unit cost has already risen from ~44 EUR/MWh (at 2020's 95% CF) to ~49 EUR/MWh (at 2025's 84% CF) — a 10% increase with no change in expenses.

## 5. The Real Cost of Kozloduy

According to Kozloduy's 2024 annual report, operating expenses (excluding the SES fund regulatory levy) were **723 M EUR**:

![Cost Breakdown](charts/cost_breakdown.png)

| Category | EUR (M) |
|---|---:|
| Production (fuel, materials) | 79 |
| RAO/decommissioning funds | 161 |
| Grid access fees | 27 |
| O&M | 148 |
| Staff & social security | 200 |
| Depreciation | 107 |
| **Total OPEX** | **723** |

Of this, **617 M EUR is fixed** — paid whether the plant runs or not. Only fuel and grid access (~6.8 EUR/MWh) scale with output. This is what makes the capacity factor so critical: same bills, fewer megawatt-hours to divide them by.

![Cost vs Capacity Factor](charts/cost_vs_cf.png)

| CF | Output (TWh) | Cost (EUR/MWh) |
|---:|---:|---:|
| 92% | 16.1 | 45 |
| **89% (2024)** | **15.6** | **46** |
| 85% | 14.9 | 48 |
| 75% | 13.1 | 54 |
| 69% (ESO 2034) | 12.1 | 59 |
| 55% (+ Apr-Oct curtailment) | 9.6 | 71 |
| 50% | 8.8 | 77 |
| 40% | 7.0 | 95 |
| **31% (gas parity)** | **5.5** | **120** |

Gas parity — where buying gas-generated electricity becomes cheaper than running Kozloduy — arrives at CF 31%. But the real danger isn't reaching that absolute line. It's the squeeze from both sides: rising costs (from falling CF) meeting falling revenue (from price suppression by solar, batteries, and regional wind). At some point, the gap between what it costs to produce nuclear electricity and what the market will pay for it becomes too small to justify the operational and safety burden of running a nuclear facility.

## 6. Building Two More Reactors: Economic Suicide

Against this backdrop, Bulgaria is pursuing plans to build two new reactors at Kozloduy — a project costing billions of euros with a construction timeline stretching into the mid-2030s.

By the time new reactors come online, the market they're built for will no longer exist. ESO's own projections show 14.8 GW of new solar and 5.2 GW of batteries by 2034. The Recovery and Resilience Plan will accelerate this further. Every year of construction is another year of solar and battery deployment eating into the hours when nuclear can sell power.

The existing two reactors already face a CF squeeze to 55-69% by 2034. Adding two more reactors — another 2,000 MW of inflexible baseload — into a market that can't absorb the current 2,000 MW is not an investment in energy security. It is doubling down on a stranded asset.

New nuclear at Kozloduy would need to run at high capacity factors for decades to recover its multi-billion-euro construction cost. The data shows the opposite trajectory: capacity factors falling, curtailment hours rising, market prices compressing. With four reactors instead of two, the curtailment problem doesn't just double — it gets exponentially worse, as 4,000 MW of must-run nuclear competes with 14+ GW of near-zero-marginal-cost solar for a national demand that rarely exceeds 6,000 MW.

No serious economic analysis supports this investment. The billions earmarked for new reactors would yield far greater returns invested in grid flexibility, storage, and interconnection — the infrastructure Bulgaria actually needs to manage its renewable-dominated future.

## 7. The Death Spiral

Nuclear power plants in markets with growing renewable penetration face a well-documented pattern:

1. **Solar grows** → nuclear must curtail during sunny hours (April-October)
2. **Output drops** → fixed costs spread over fewer MWh → cost per MWh rises
3. **Revenue falls** → solar and batteries suppress prices during nuclear selling hours
4. **Curtailment extends** from summer into shoulder months and winter
5. **Regional renewables** (Greek wind, Romanian solar) erode winter margins
6. **Export markets close** → neighbors build own renewables, stop buying Bulgarian surplus
7. **Reliability degrades** → aging plant, deferred maintenance, unplanned outages
8. **Political choice** → subsidize, or close

Bulgaria is at stages 1-3 today. ESO's own projections and the Recovery and Resilience Plan place the country well into stages 4-6 by 2034.

## 8. Conclusion

Kozloduy NPP is not in immediate danger. At current capacity factors and market prices, it remains viable. But the trajectory is unambiguous:

- **Today (5.3 GW solar, CF 89%)**: 46 EUR/MWh cost, comfortable
- **~10 GW solar (CF 74%)**: 55 EUR/MWh, margins narrowing
- **14.3 GW solar (ESO 2034, CF 69%)**: 59 EUR/MWh
- **14.3 GW + Apr-Oct curtailment (CF 55%)**: 71 EUR/MWh, fragile
- **+ regional wind + batteries + price compression**: approaching breakeven

The CF has already dropped from 95% to 84% in five years. The forces driving this decline — solar deployment, battery storage, regional wind development, export market saturation — are all accelerating. None of them are reversible.

**And none of them can be stopped.** Even if Bulgaria froze all domestic renewable construction tomorrow, Greek wind farms, Romanian solar parks, and Turkish capacity additions would continue suppressing regional electricity prices. The Balkans energy market is integrating. Bulgaria cannot wall itself off from the solar and wind tsunami sweeping Southeast Europe. The electricity will flow through the interconnectors, the prices will converge, and the economics of inflexible baseload generation will continue to deteriorate.

The question facing Bulgarian energy policy is not *whether* nuclear economics will collapse, but whether the country plans proactively — investing in flexibility, storage, and grid modernization — or stumbles into crisis with billions wasted on new reactors the market doesn't need.

---

*Analysis based on ENTSOE hourly market data (2015-2026), Kozloduy NPP 2024 Annual Report, and ESO 10-year network development plan 2024-2033 ([eso.bg](https://www.eso.bg/fileObj.php?oid=5402)). All data and scripts available at [github.com/dimivan-dev/nuclear-economics-bg](https://github.com/dimivan-dev/nuclear-economics-bg).*
