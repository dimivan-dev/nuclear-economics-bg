# Slow but Inevitable: The Economic Death of Nuclear in Bulgaria

## Introduction

Nuclear power plants are unusual machines. Unlike a gas turbine that can switch on and off cheaply, a nuclear reactor costs almost the same to own whether it runs or not. The staff, the maintenance crews, the decommissioning funds, the insurance — all of it gets paid regardless of how much electricity the plant produces. The fuel itself is surprisingly cheap — just a few euros per megawatt-hour.

This means nuclear economics depend almost entirely on one number: the **capacity factor** — what percentage of the theoretical maximum the plant actually produces. A nuclear plant running at 90% capacity factor spreads its massive fixed costs over a lot of electricity, making each unit cheap. At 50%, those same fixed costs are spread over half the electricity, roughly doubling the per-unit price.

Kozloduy NPP, Bulgaria's only nuclear plant, has two 1,000 MW reactors producing roughly 15-16 TWh per year. For decades, this baseload model worked: the plant ran flat out, electricity was always needed, and the math was simple.

That model is now breaking. Solar energy — which produces for free once installed — is eating into the hours when nuclear can sell its power. And unlike gas plants that can simply turn off when solar floods the market, nuclear can't flex. The result is a slow but mathematically inevitable squeeze on Kozloduy's economics.

## 1. The Solar Wave

Bulgaria's installed solar capacity has reached ~5.3 GW in 2024. ESO's (the Bulgarian TSO) 10-year network development plan projects **14.8 GW of new solar** and **5.2 GW of battery storage** by 2034, based on investor intentions already in the pipeline. ESO themselves state plainly what this means:

> „С ускореното навлизане на ВЕИ и липса на значителен промишлен товар в страната, необходимостта от принудително ограничаване работната мощност на АЕЦ през определени периоди в годината тепърва ще се увеличава."
>
> — ЕСО, Десетгодишен план за развитие на преносната мрежа 2024-2033

*("With the accelerated entry of renewables and the lack of significant industrial load in the country, the need to forcibly limit the operating capacity of the NPP during certain periods of the year will only increase.")*

Bulgaria's participation in the EU Recovery and Resilience Plan will further accelerate this timeline. The investment incentives and regulatory fast-tracking mean the country will likely reach significant solar and storage capacity well before 2034.

### What Solar Does to Nuclear

Using 2024 hourly ENTSOE data, we can model the impact. Nuclear must curtail whenever solar pushes total supply above demand (after accounting for ~300 MW of must-run gas CHP):

| Solar installed | Curtailment hours/year | Lost output (TWh) | Nuclear CF | Cost (EUR/MWh) |
|---|---:|---:|---:|---:|
| 5.3 GW (2024 actual) | 726 | 0.7 | 86% | 48 |
| 7.3 GW (+2 GW) | 1,421 | 1.5 | 82% | 51 |
| 10.3 GW (+5 GW) | 2,012 | 2.8 | 74% | 55 |
| **14.3 GW (ESO 2034)** | **2,411** | **3.7** | **69%** | **59** |
| 20.3 GW | 2,787 | 4.5 | 64% | 63 |

At ESO's projected 14.3 GW, nuclear loses 3.7 TWh of annual output and costs rise to 59 EUR/MWh — a 27% increase from today.

### Not Just Summer — April to October

The common assumption is that solar only threatens nuclear during the three summer months. The reality is much broader. With 14+ GW of solar, curtailment extends across the entire April-October period — roughly 7 months. Shoulder months like April, May, September, and October have moderate demand but increasingly strong solar output. At 14.3 GW installed, midday solar generation in these months routinely exceeds total national demand minus nuclear minimum output.

This isn't a clean 3-month shutdown. It's a messy pattern of forced curtailment, partial-load operation, and uneconomic running hours spanning more than half the year. Nuclear plants are not designed for this — cycling damages components, increases maintenance costs, and shortens fuel rod life. Each curtailment hour isn't just lost revenue; it adds operational wear.

### The Battery Accelerator

ESO's plan includes 5.2 GW of battery storage. Batteries don't save nuclear — they make its problem worse. Batteries profit by charging when prices are low (solar midday) and discharging when prices are high (evening peak). This flattens the price curve: it raises the floor slightly but crushes the evening peak that nuclear relies on for its best revenue hours. With enough batteries, the lucrative evening spread that makes nuclear profitable even on sunny days disappears.

The Recovery and Resilience Plan creates strong investment incentives for storage deployment. Bulgaria could reach multi-GWh battery capacity well ahead of ESO's 2034 timeline, accelerating the erosion of nuclear's evening price premium.

## 2. February 15, 2026: A Preview

On February 15, 2026, a Sunday, Bulgaria experienced near-zero electricity prices for almost the entire day — **in winter**. This is not a summer phenomenon.

| Hour | Nuclear (MW) | Coal (MW) | Gas (MW) | Hydro (MW) | Wind (MW) | BG Price | RO Price |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 00:00 | 1,904 | 1,099 | 313 | 360 | 383 | 10.0 | 99.3 |
| 06:00 | 1,904 | 1,094 | 313 | 770 | 413 | 0.0 | 101.3 |
| 10:00 | 1,904 | 1,118 | 308 | 586 | 196 | 2.5 | 108.9 |
| 14:00 | 1,903 | 1,098 | 313 | 739 | 323 | 0.2 | 216.1 |
| 18:00 | 1,905 | 1,145 | 312 | 1,134 | 288 | 9.2 | 212.0 |
| 22:00 | 1,905 | 1,099 | 320 | 635 | 468 | 10.0 | 197.5 |

Bulgaria averaged **12.3 EUR/MWh** while Romania averaged **138.4 EUR/MWh** — a 126 EUR/MWh spread, with Bulgaria on the wrong side.

The cause: **3,200 MW of must-run generation** (nuclear 1,904 + lignite ~1,100 + gas CHP ~310) against ~3,800 MW demand, with 300-470 MW of wind on top. Interconnector capacity to Romania was saturated. Bulgaria exported power at near-zero prices while Romania paid 100-216 EUR/MWh next door.

This happened with only 350 MW of wind. Bulgaria's grid collapsed into surplus not because of massive renewable generation, but because of **nuclear and coal inflexibility**. Kozloduy cannot economically reduce output for a single day. Neither can lignite plants with minimum stable generation.

Compare with Greece on the same day: 3,400 MW of wind, yet prices stayed at 38-142 EUR/MWh. Greece has a flexible gas fleet that ramps down when wind picks up. Bulgaria doesn't.

### No Export Market to Save the Day

In 2015-2017, Bulgaria could profitably export surplus baseload power to its neighbors. Those days are over. Romania is rapidly building its own solar fleet. Greece has massive wind development. Turkey's market is increasingly self-sufficient. The neighbors that once absorbed Bulgaria's excess generation are becoming competitors.

When Bulgaria had surplus power on Feb 15, 2026, it couldn't even sell it at cost — the interconnectors were full and the neighbors didn't need it at any price. As solar and wind grow across the entire Balkans region, these export-blocked, near-zero-price events will become routine.

## 3. Winter Under Threat

Nuclear's traditional stronghold is winter: solar is minimal, demand peaks, and prices are highest. But even this is eroding.

**Greek and Romanian wind** competes directly with Bulgarian nuclear during winter. Bulgaria, Romania, and Greece are tightly coupled electricity markets — prices typically track within 5 EUR/MWh. As Greece continues its aggressive wind buildout and Romania adds both wind and solar, winter prices across the region will face downward pressure from renewable oversupply during windy periods.

In 2024, 20 winter days already had solar peaks above 2 GW in Bulgaria. Some showed dramatic price pressure — February 22-23 averaged just 60-69 EUR/MWh, with minimums hitting 10 EUR/MWh. These are sunny winter days where even today's modest solar fleet pushes prices below nuclear's comfortable zone. And on windy winter days, Greek and Romanian wind does the same job that solar does in summer.

The result: nuclear's "safe" selling season is shrinking from both ends — solar eats the shoulder months and summer, while regional wind eats into winter margins.

## 4. Unit 6 Reliability

The economic analysis above assumes Kozloduy operates reliably when it's running. Recent events at Unit 6 challenge this assumption.

Between December 2025 and February 2026, Unit 6 experienced multiple unplanned shutdowns — events that not only cut output but demonstrate the operational risks of an aging reactor. Each unplanned outage carries costs beyond lost generation: emergency response, inspection requirements, potential regulatory constraints on restart timing.

Unit 6 reliability issues compound the solar squeeze: every unplanned shutdown day in winter — when prices are highest — is a day of lost revenue that cannot be recovered. And as the economic margin narrows, the cost-benefit calculation for maintenance investment tilts further against the plant.

The declining capacity factor trend is already visible in the data:

| Year | Output (TWh) | CF |
|---:|---:|---:|
| 2018 | 16.2 | 92% |
| 2019 | 16.6 | 95% |
| 2020 | 16.7 | 95% |
| 2021 | 16.5 | 94% |
| 2022 | 16.5 | 94% |
| 2023 | 16.2 | 93% |
| **2024** | **15.6** | **89%** |
| **2025** | **14.8** | **84%** |

From 16.7 TWh in 2020 to 14.8 TWh in 2025 — a drop of 1.9 TWh (11%) in five years, and the decline is accelerating.

## 5. The Real Cost of Kozloduy

According to Kozloduy's 2024 annual report, total annual expenses were **1,842,450 thousand BGN (942 M EUR)**. The full breakdown:

| Category | BGN (хил.) | EUR (M) | Share |
|---|---:|---:|---:|
| **Annual expenses** | **1,842,450** | **942** | **100%** |
| Operating expenses | 1,803,416 | 922 | 98% |
| — Production (fuel, materials) | 154,617 | 79 | 8% |
| — RAO/decommissioning funds | 315,251 | 161 | 17% |
| — Grid access fees | 53,341 | 27 | 3% |
| — O&M | 289,881 | 148 | 16% |
| — Staff & social security | 391,944 | 200 | 21% |
| — Depreciation | 209,417 | 107 | 11% |
| — SES fund contributions | 388,964 | 199 | 21% |

The SES fund contribution (199 M EUR) is a regulatory levy to the Energy Security Fund — not an operational cost of running the plant. Excluding it, the real operating cost is **723 M EUR**.

Of this, **617 M EUR is fixed** — it gets paid whether the plant runs or not. Only fuel and grid access (~6.8 EUR/MWh) scale with output.

This is what makes the capacity factor so critical. At 89% CF (2024), the cost is 46.5 EUR/MWh. At 55% CF, it's 71 EUR/MWh. Same plant, same staff, same maintenance — just fewer megawatt-hours to divide the bill by.

| CF | Output (TWh) | Cost (EUR/MWh) | Breakeven price |
|---:|---:|---:|---:|
| 92% | 16.1 | 45 | 45 |
| **89%** | **15.6** | **46 (2024)** | **46** |
| 85% | 14.9 | 48 | 48 |
| 75% | 13.1 | 54 | 54 |
| 69% (ESO 2034) | 12.1 | 58 | 58 |
| 55% (+ summer curtailment) | 9.6 | 71 | 71 |
| 50% | 8.8 | 77 | 77 |
| 40% | 7.0 | 95 | 95 |
| **31%** | **5.5** | **120 (gas parity)** | **120** |

Gas parity — the point where buying gas electricity is cheaper than running nuclear — arrives at CF 31%. But the real danger is not reaching that line. It's the profit erosion along the way.

### Profit Erosion

At 2024's average Bulgarian day-ahead price of 103.5 EUR/MWh:

| Scenario | CF | Output (TWh) | Revenue (M EUR) | OPEX (M EUR) | Profit (M EUR) |
|---|---:|---:|---:|---:|---:|
| 2024 actual | 89% | 15.6 | 1,614 | 723 | +891 |
| Moderate solar growth | 75% | 13.1 | 1,360 | 707 | +654 |
| ESO 2034 | 69% | 12.1 | 1,248 | 700 | +548 |
| ESO 2034 + curtailment Apr-Oct | 55% | 9.6 | 997 | 683 | +315 |
| Aggressive solar + batteries | 50% | 8.8 | 907 | 677 | +230 |

At today's prices, Kozloduy remains profitable even at CF 50%. But 2024 prices (103.5 EUR/MWh average) are historically elevated — a legacy of the energy crisis. As solar and batteries suppress daytime and evening prices across the region, the average price nuclear can capture will fall. If average prices drop to 80 EUR/MWh (plausible with 14 GW of solar):

| Scenario | CF | Revenue at 80 EUR/MWh | OPEX | Profit |
|---|---:|---:|---:|---:|
| ESO 2034 | 69% | 965 M | 700 M | +265 M |
| ESO 2034 + curtailment | 55% | 768 M | 683 M | +85 M |
| + price compression | 50% | 700 M | 677 M | +23 M |

At 80 EUR/MWh and CF 55%, profit is just 85 M EUR — down 91% from today. And the squeeze works from both sides: costs rise (lower CF) while revenue falls (lower prices). This is the death spiral.

## 6. The Death Spiral

Nuclear power plants in markets with growing renewable penetration face a well-documented pattern:

1. **Solar grows** → nuclear must curtail during sunny hours (April-October)
2. **Output drops** → fixed costs spread over fewer MWh → cost per MWh rises
3. **Revenue falls** → solar and batteries suppress prices during nuclear selling hours
4. **Curtailment extends** from summer to shoulder months → CF drops further
5. **Regional wind** (Greece, Romania) erodes winter margins — the last profitable season
6. **Export markets close** → neighbors build their own renewables, no longer buy Bulgarian surplus
7. **Reliability degrades** → aging plant, deferred maintenance, unplanned outages
8. **Political choice** → subsidize, or close

Bulgaria is at stages 1-3 today. ESO's own projections and the Recovery and Resilience Plan place the country at stages 4-6 well before 2034.

## 7. Conclusion

Kozloduy NPP is not in immediate danger of closure. At current capacity factors and prices, it generates 891 M EUR of annual profit. But the trajectory is clear and the math is unforgiving:

- **Today (5.3 GW solar, CF 89%)**: 46 EUR/MWh cost, highly profitable
- **~10 GW solar (CF 74%)**: 55 EUR/MWh, comfortable but declining
- **14.3 GW solar (ESO 2034, CF 69%)**: 59 EUR/MWh, margins narrowing
- **14.3 GW solar + Apr-Oct curtailment (CF 55%)**: 71 EUR/MWh, fragile
- **+ regional wind + batteries + price compression**: approaching breakeven

The CF has already declined from 95% to 84% in five years. The factors driving this decline — solar deployment, regional wind development, battery storage, export market saturation — are all accelerating. None of them are reversible.

The question facing Bulgarian energy policy is not whether this transition will happen, but whether the country plans for it proactively — investing in flexibility, storage, and grid modernization — or reactively, when Kozloduy's economics have already collapsed.

---

*Analysis based on ENTSOE hourly market data (2015-2026), Kozloduy NPP 2024 Annual Report, and ESO 10-year network development plan 2024-2033 ([eso.bg](https://www.eso.bg/fileObj.php?oid=5402)). All calculations use actual market prices and reported generation data.*
