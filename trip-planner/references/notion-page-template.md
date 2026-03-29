# Notion Page Template — Trip Planner

Use this as the content template when creating a new trip page via `notion-create-pages`.
Replace all `[PLACEHOLDER]` values with real data before writing to Notion.

---

```markdown
# 🗺️ Trip Overview

| | |
|---|---|
| **Destination** | [CITY, STATE/COUNTRY] |
| **Dates** | [Month D–D, YYYY] ([N] days / [N] nights) |
| **From** | 261 Lewis Honey Dr, Aurora, ON |
| **Vehicle** | 2024 Tesla Model Y AWD Long Range |
| **Start Charge** | 100% (charged overnight before departure) |
| **Sleeping** | Overnight at truck stops (Love's / Flying J) |
| **Border Crossing** | [e.g. Peace Bridge — Fort Erie → Buffalo, NY] |
| **Route** | [e.g. QEW → Hwy 420 → I-90 W] |
| **Distance** | ~[N] km each way |
| **Drive Time** | ~[N] hrs (before border wait) |

---

# ⚡ Supercharger Plan

| Stop | Location | Distance from Aurora | kW | Amenities | Rating |
|---|---|---|---|---|---|
| **Stop 1 (outbound)** | [Name, Address] | ~[N] km | [N]kW | [food/restrooms/etc] | ⭐[N] |
| **Stop 2 (optional)** | [Name, Address] | [context] | [N]kW | [food/restrooms/etc] | ⭐[N] |
| **In-city** | [Name, Address] | [context] | [N]kW | [notes] | ⭐[N] |
| **Return stop** | [Name, Address] | [context] | [N]kW | [notes] | ⭐[N] |

> ⚠️ [Any safety or range warnings]

---

# 🛻 Overnight Truck Stops

| Night | Planned Stop | Address | Amenities |
|---|---|---|---|
| **Night 1** ([Date]) | [Love's / Flying J — Location] | [Address] | [24hr · showers · food] |
| **Night 2** ([Date]) | [Love's / Flying J — Location] | [Address] | [notes] |

---

# 📅 Day-by-Day Itinerary

## Day 1 — [Weekday, Month D, YYYY] · [Theme]

| Time | Activity | Notes |
|---|---|---|
| [7:00 AM] | 🏠 Depart Aurora | Full 100% charge. [Route details] |
| [8:30 AM] | 🛂 [Border Crossing] | [crossing notes] |
| [11:00 AM] | ⚡ Supercharger — [Location] | [address · kW · duration · food notes] |
| [1:30 PM] | 🎯 [Activity] | [hours · cost · tips] |
| [6:00 PM] | 🍺 Dinner — [Area] | [restaurant suggestions] |
| [9:00 PM] | 🛻 Sleep — [Truck Stop] | Tesla Camp Mode · ~10–14% battery overnight |

## Day 2 — [Weekday, Month D, YYYY] · [Theme]

| Time | Activity | Notes |
|---|---|---|
| [8:00 AM] | 🌅 Morning at [Truck Stop] | Freshen up, coffee, breakfast |
| ... | ... | ... |

## Day [N] — [Weekday, Month D, YYYY] · [Theme]

| Time | Activity | Notes |
|---|---|---|
| ... | ... | ... |
| [Time] | 🛣️ Drive Home | [Route] · ~[N] hr drive · border wait |

> 💡 **[Any timing notes, e.g. game-night drive warning]**

---

# 🏛️ Attractions Detail

## [Attraction Name] ⭐ [Book Ahead / Free / etc.]
- **Address:** [full address]
- **Hours:** [days and times, noting any closures]
- **Phone:** [number]
- **Website:** [url]
- **Admission:** [price or Free]
- **Tours / Options:** [self-guided, guided, etc.]
- **Tip:** [insider tip]
- **Budget:** ~[N] hrs

## [Next Attraction]
...

---

# 🚗 Camp Mode Reference

| Setting | Value |
|---|---|
| Battery drain overnight (mild weather) | ~10–14% |
| Activate | Climate Control → fan icon → "Camp" |
| Sentry Mode | **Turn OFF overnight** (drains battery fast) |
| Doors | Lock manually from touchscreen |
| Don't open Tesla app while sleeping | Wakes car, increases drain |
| Temperature | Set 18–20°C for efficiency |

---

# 📊 Expense Tracker

*To be filled in as receipts arrive (managed by travel-expense-tracker skill).*

| Date | Category | Merchant | Amount (CAD) | Notes |
|---|---|---|---|---|
| [Date] | 🚗 Transport | Supercharger — [location] | TBD | |
| [Date] | 🏛️ Attraction | [name] | [Free / TBD] | |

---

# 🍽️ Dining Log

*To be filled in during/after trip (managed by travel-expense-tracker skill).*

---

# ⚠️ To-Do Before Trip

- [ ] [Book attraction that requires advance reservation]
- [ ] [Buy event tickets]
- [ ] Charge Tesla to 100% night of [Date]
- [ ] Check Peace Bridge border wait times morning of departure
- [ ] Confirm Love's / Flying J overnight parking policy
- [ ] Download Love's app for overnight spot finder
- [ ] Download PlugShare as backup charger app
```
