# Slow but Inevitable: The Economic Death of Nuclear in Bulgaria

A nuclear power plant is like a factory with enormous rent and almost no raw material costs. Whether Kozloduy NPP produces one megawatt-hour or sixteen billion of them, it still pays the same salaries to thousands of employees, the same maintenance bills, the same decommissioning contributions, and the same depreciation on its life-extension investments. The actual fuel — uranium — is surprisingly cheap, just a few euros per megawatt-hour.

This cost structure creates a simple but unforgiving economic rule: nuclear power only works if the plant runs **a lot**. The industry measures this as the **capacity factor (CF)** — what percentage of the theoretical maximum the plant actually produces. At 90% CF, the massive fixed costs are spread over a lot of electricity, making each unit affordable. At 50% CF, those same costs are spread over half the output, roughly doubling the price per unit. There's no way around this math.

For decades, Kozloduy's two 1,000 MW reactors ran at 92-95% capacity factor, producing 16+ TWh per year. Electricity was always needed, the plant ran flat out, and the economics were excellent.

That model is now breaking — and the force breaking it cannot be stopped.

**Bulgaria's installed solar capacity has reached 5.3 GW. ESO projects 14.8 GW of new solar and 16 GWh of battery storage by 2034.**

ESO's (the Bulgarian Transmission System Operator) 10-year network development plan lays it out plainly, based on investor intentions already in the pipeline:

> „С ускореното навлизане на ВЕИ и липса на значителен промишлен товар в страната, необходимостта от принудително ограничаване работната мощност на АЕЦ през определени периоди в годината тепърва ще се увеличава."
>
> — ЕСО, Десетгодишен план за развитие на преносната мрежа 2024-2033

*("With the accelerated entry of renewables and the lack of significant industrial load in the country, the need to forcibly limit the operating capacity of the NPP during certain periods of the year will only increase.")*

Bulgaria's participation in the EU Recovery and Resilience Plan will further accelerate this timeline. The investment incentives and regulatory fast-tracking mean the country will likely reach 16 GWh of battery storage and significant solar milestones well before 2034.

**Solar produces for free. When it floods the grid, it pushes prices toward zero — and nuclear has nowhere to hide.**

Nuclear doesn't get physically curtailed by solar — it could keep running. The problem is economic: when solar pushes prices below nuclear's operating cost, every hour the plant runs is an hour it loses money.

Until now, Kozloduy has been partly shielded by the daily price cycle. Even on sunny days, the evening peak (when solar fades but demand stays high) kept average daily prices above nuclear's cost. Nuclear sold cheaply at midday but recovered on the evening peak. With no significant battery storage deployed yet in Bulgaria, this peak-night spread has been nuclear's lifeline.

**That lifeline is about to be cut.**

With 16 GWh of batteries planned (and accelerated by the Recovery and Resilience Plan), batteries will charge during solar midday and discharge into the evening peak — eliminating exactly the price spread that keeps nuclear profitable on sunny days. Once batteries flatten the evening peak, nuclear has nowhere to recover its midday losses.

**In summer 2025, solar already accounts for 25-30% of Bulgaria's electricity generation — and is set to triple.**

Using 2025 actual market data, we model electricity prices as solar capacity grows toward ESO's 2034 projections. The model accounts for coal displacement (extra solar first pushes coal off the grid before compressing prices further) and battery peak erosion (large-scale storage structurally caps evening peak prices at coal's full cost of ~88 EUR/MWh).

An important caveat: the 2025 baseline already understates the problem. During May-August 2025, Unit 6 was offline or running at half capacity for extended periods, reducing nuclear output by 500-900 MW. This lower supply kept prices higher than they would have been with both reactors running. The numbers below are therefore conservative.

![Monthly Price Heatmap](charts/price_heatmap.png)

At ESO's projected 14.3 GW of solar with 16 GWh of batteries, six months of the year (April through September) have average prices below nuclear's operating cost. June and July drop to 19-20 EUR/MWh. By 20 GW, June and July have **negative average prices**, and only January-February remain safely profitable.

**This is what a typical weekend summer day looks like as solar grows.**

![Weekend Summer Day Profile](charts/weekend_summer_profile.png)

At today's 5.3 GW, prices dip to near zero at midday but recover strongly in the evening — nuclear earns +264 EUR/MW/day on a summer weekend. At 10 GW, the midday trough deepens and the daily profit vanishes to near zero. At 14.3 GW, prices are negative from 5am to 3pm, reaching -60 to -80 EUR/MWh, and only 5 evening hours remain above nuclear's cost. The daily loss reaches -328 EUR/MW.

Weekdays are even worse: higher solar output drives midday prices to -80 to -170 EUR/MWh at 14.3 GW. And this is before batteries eat the remaining evening peak.

**Batteries don't just shift energy — they permanently destroy the peak premium.**

![Battery Peak Erosion](charts/battery_peak_erosion.png)

Without batteries, nuclear still has 5 profitable evening hours on a summer weekend at 14.3 GW. With 16 GWh of batteries discharging into the evening peak, those hours get capped at coal's full cost (88 EUR/MWh) — the battery undercuts any price above that. With 32 GWh, even more peak hours are capped. The price spread transforms from time-of-day arbitrage (buy cheap midday, sell expensive evening) into technology arbitrage: batteries profit from the cost gap between solar (~55 EUR/MWh) and coal (~88 EUR/MWh), not from the daily demand shape. Nuclear, caught in between, can sell into neither side of this new spread.

**Nuclear's traditional stronghold is winter. Even that is eroding.**

Greek and Romanian wind competes directly with Bulgarian nuclear during winter months. On windy winter days, regional prices face the same oversupply pressure that solar creates in summer. Nuclear's "safe" selling season is shrinking from both ends — solar eats the shoulder months and summer, regional wind eats into winter.

**On February 15, 2026, Bulgaria experienced near-zero electricity prices for almost the entire day — in winter.**

![Feb 15, 2026: BG Prices](charts/feb15_2026_prices.png)

Bulgaria averaged 12.3 EUR/MWh for the day. Meanwhile, interconnector capacity to neighboring countries was fully saturated — Bulgaria couldn't export its surplus at any price. The cause: 3,200 MW of must-run generation (nuclear 1,904 + lignite ~1,100 + gas CHP ~310) against ~3,800 MW demand, with just 300-470 MW of wind on top.

This happened with minimal renewables. The grid collapsed into surplus because of nuclear and coal inflexibility. Compare with Greece on the same day: 3,400 MW of wind, yet prices stayed at 38-142 EUR/MWh. Greece has a flexible gas fleet that ramps down when renewables ramp up. Bulgaria doesn't.


**The export market that once absorbed Bulgaria's surplus is gone.**

In 2015-2017, Bulgaria could profitably export surplus baseload power to neighbors. Romania is now building its own solar fleet. Greece has massive wind. Even if Bulgaria were to freeze all domestic solar construction tomorrow, the problem doesn't go away. Bulgaria, Romania, and Greece form a tightly coupled electricity market — prices typically track within 5 EUR/MWh across the region. The solar and wind tsunami is regional, not national.

**Meanwhile, Unit 6 is making the problem worse from the other side.**

Between December 2025 and February 2026, Unit 6 experienced multiple unplanned shutdowns. In summer 2025, Unit 6 was offline or at half capacity for extended periods — May averaged just 1,064 MW of nuclear output (versus ~2,000 MW at full capacity). The declining capacity factor is already visible:

![Historical Capacity Factor](charts/historical_cf.png)

From 16.7 TWh in 2020 to 14.8 TWh in 2025 — a drop of 1.9 TWh (11%) in five years, driven by Unit 6 technical problems. Note that 2025 ENTSOE data is preliminary — the final numbers, once released, are expected to be worse.

**Kozloduy's real operating cost is 723 million EUR per year — and almost all of it is fixed.**

According to Kozloduy's 2024 annual report, operating expenses (excluding the SES fund regulatory levy) total 723 M EUR. Of this, 617 M EUR is fixed — paid whether the plant runs or not. Only fuel and grid access (~6.8 EUR/MWh) scale with output.

![Cost Breakdown](charts/cost_breakdown.png)

![Cost vs Capacity Factor](charts/cost_vs_cf.png)

**So when does Kozloduy actually have to start shutting reactors down?**

Kozloduy's two VVER-1000 reactors cannot modulate to follow hourly load — they are not designed for load-following operation. They can reduce output to roughly 70% (running both at ~700 MW each, or 1,400 MW total), or take one reactor completely offline (~1,000 MW). These are the only realistic curtailment options.

![Profit vs Solar Capacity](charts/profit_vs_solar.png)

The picture is stark. Without batteries, Kozloduy remains profitable even at 20 GW of solar — barely, at +7 M EUR. But add 16 GWh of batteries (ESO's own projection, likely to arrive sooner), and the crossover point drops to **~16 GW of solar**. That's just 10 GW more than today, well within ESO's 2034 projection of 14.8 GW new capacity.

**At 14.3 GW + 16 GWh batteries, Kozloduy earns just 47 EUR/MWh against a cost of 46 EUR/MWh — an 82 M EUR annual profit on a 735 M EUR cost base.** One bad year, one extended outage, one price dip wipes it out. Taking a reactor offline for the summer doesn't help — it reduces revenue more than it saves in variable costs, because the marginal cost of running (7 EUR/MWh) is far below even the depressed summer prices.

![Strategy Comparison](charts/strategy_comparison.png)

At 16 GW + 16 GWh, nuclear enters permanent loss territory. No operating strategy — full power, reduced power, one reactor off — returns a profit. The loss only deepens from there. By 20 GW + 16 GWh, the annual loss exceeds 200 M EUR regardless of strategy.

**This is a death spiral — and Bulgaria is entering it now.**

The pattern is well-documented in every market where renewables have reached critical mass. Solar and wind grow, market prices drop. Revenue falls, but fixed costs stay the same. Prices go negative during more and more hours. The plant shuts down for longer periods. Output drops, costs per unit rise. Regional renewables erode even winter margins. Export markets close as neighbors build their own capacity. And then comes the political choice: subsidize, or close.

Reliability issues and the solar squeeze feed each other. Every unplanned outage pushes costs up, and every GW of solar pushes revenue down. The margin gets thinner from both sides.

**Against this backdrop, Bulgaria is pursuing plans to build two more reactors.**

The project would cost billions of euros with a construction timeline stretching into the mid-2030s. This is like entering a lame, blind horse into a race that it's already late for — and even if it arrived on time, it couldn't win.

**It's late.** New nuclear construction takes 10-15 years. By the time these reactors produce their first MWh, ESO projects 14.8 GW of solar and 16 GWh of batteries will already be on the grid. The market these reactors are designed for will have ceased to exist.

**It's lame.** Nuclear is inflexible. It can't ramp down for sunny afternoons or windy winter nights. In a market dominated by variable renewables, inflexibility is not a feature — it's a fatal flaw. Every hour the reactor can't flex is an hour it bleeds money.

**It's blind.** The project ignores every market signal. Capacity factors falling. Market prices compressing. Neighbors building their own renewables. Export markets saturating. The data is screaming that inflexible baseload has no future in Southeast Europe's integrating electricity market. The project sees none of this.

**It can't win.** Even if built on time and on budget (which no nuclear project in Europe has achieved this century), 4,000 MW of must-run nuclear competing with 14+ GW of near-zero-marginal-cost solar for a national demand that rarely exceeds 6,000 MW is arithmetic that doesn't work. The plant would be born into curtailment.

The billions earmarked for new reactors would yield far greater returns invested in grid flexibility, storage, and interconnection — the infrastructure Bulgaria actually needs.

**Kozloduy NPP is not in immediate danger. But the trajectory is unambiguous.**

Today, at 5.3 GW solar with no batteries, the average market price is 90 EUR/MWh and nuclear earns a comfortable 828 M EUR profit. Add 16 GWh of batteries alone — without any new solar — and that profit halves to 455 M EUR as batteries cap the evening peak. At 10 GW solar with batteries, profit drops to 291 M EUR. At ESO's projected 14.3 GW with 16 GWh of batteries, profit shrinks to just 82 M EUR — the plant barely breaks even. At 16 GW + 16 GWh, nuclear enters permanent loss.

The forces driving this — solar deployment, battery storage, regional wind, export market saturation — are all accelerating. None of them are reversible. And none of them can be stopped. Even if Bulgaria froze all domestic renewable construction tomorrow, Greek wind farms, Romanian solar parks, and Turkish capacity additions would continue suppressing regional electricity prices. The Balkans energy market is integrating. Bulgaria cannot wall itself off from the solar and wind tsunami sweeping Southeast Europe. The electricity will flow through the interconnectors, the prices will converge, and the economics of inflexible baseload generation will continue to deteriorate.

The question is not *whether* nuclear economics will collapse, but whether Bulgaria plans proactively — investing in flexibility, storage, and grid modernization — or stumbles into crisis with billions wasted on new reactors that the market doesn't need and physics won't allow to compete.

---

*Analysis based on ENTSOE hourly market data (2015-2026), Kozloduy NPP 2024 Annual Report, and ESO 10-year network development plan 2024-2033 ([eso.bg](https://www.eso.bg/fileObj.php?oid=5402)). Full data tables in [analysis_tables.md](analysis_tables.md). All data and scripts available at [github.com/dimivan-dev/nuclear-economics-bg](https://github.com/dimivan-dev/nuclear-economics-bg).*
