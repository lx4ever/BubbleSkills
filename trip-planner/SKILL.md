---
name: trip-planner
description: >
  Tesla road trip planning skill for Mimi. Automatically builds and maintains a live trip plan
  whenever the user mentions a destination, dates, activities, hotels, restaurants, or any
  travel-related detail — even casually. Integrates with the travel-expense-tracker skill
  to share the same Notion page. Use this skill aggressively: if the user mentions a place
  they want to go, a date range, a thing they want to do on a trip, a game or event they
  want to attend, or asks about driving routes, charging stops, or overnight stops — trigger
  this skill immediately. Also trigger when the user says things like "we're going to X",
  "I want to visit Y", "add this to my trip", "update the trip", or sends any snippet of
  information that relates to an upcoming journey.
---

# Trip Planner Skill

Automatically builds, updates, and syncs a comprehensive road trip plan to Notion whenever
the user provides any trip information. Works in tandem with the **travel-expense-tracker**
skill — both write to the same Notion page under Travel Plans.

---

## User Defaults (always apply)

| Setting | Value |
|---|---|
| **Vehicle** | 2024 Tesla Model Y AWD Long Range |
| **Range** | ~530 km (EPA) · ~400–450 km real-world highway |
| **Departure charge** | Always 100% from home |
| **"Sleeping in car"** | = Overnight at truck stop — **Love's or Flying J preferred** |
| **Home base** | 261 Lewis Honey Dr, Aurora, ON |
| **Border crossing** | Peace Bridge (Fort Erie → Buffalo, NY) by default |

---

## Trigger Behaviours

React to **any** of these user inputs by updating the trip plan:

- Destination or city name ("we're going to Cleveland")
- Date or date range ("April 3–5")
- Activity, attraction, or event ("we want to see the Reformatory")
- Accommodation or overnight preference ("sleeping in car", "hotel in X")
- Sports game or event ("watch the Cavs game")
- Restaurant or dining mention
- "Add this to my trip" / "update the plan" / "also visiting X"
- Photo of a receipt, ticket, or itinerary (hand off to travel-expense-tracker)

---

## Step 1 — Extract & Enrich Trip Details

From the user's message(s), extract:
- **Destination(s)** and any stops along the way
- **Dates** — trip start/end, specific day activities
- **Activities / Attractions** — look up hours, admission, booking requirements
- **Events** — use `fetch_sports_data` tool for NBA/NHL/MLB/etc. to confirm game time + venue
- **Dining** — note any restaurants mentioned; add to Dining Log placeholder
- **Overnight stops** — find nearest Love's or Flying J on route

Then enrich with web searches as needed:
- Attraction hours, admission prices, booking links
- Supercharger locations along the route (space stops every ~300 km)
- Love's / Flying J locations convenient to each overnight stop

---

## Step 2 — Plan the Route & Charging

### Supercharger Planning Rules
- Depart at 100% charge
- Plan Supercharger stops every **280–320 km** of highway driving
- Prefer stops with **Sheetz, food, or clean restrooms** nearby (check reviews)
- Avoid Superchargers with low ratings or safety concerns flagged in reviews
- Target arriving at each stop at **~20% battery** (conservative buffer)
- Before driving home: top up to **80–90%** at a well-rated Supercharger

### Overnight Truck Stop Rules
- Default to **Love's Travel Stop** or **Flying J**
- Find locations within ~15 min of the day's final destination or next morning's first stop
- Note amenities: showers, 24hr food, restrooms
- Flag if the location has overnight parking restrictions
- Tesla Camp Mode reminder: ~10–14% battery drain overnight in mild weather; turn off Sentry Mode

---

## Step 3 — Build / Update the Notion Page

### Finding the Right Page
1. Search under Travel Plans (`page_id: 32724f54-8181-80c0-a063-e312b5dafca3`) for an existing page matching the destination + month/year
2. If found → **update** it using `notion-update-page` (append / search-replace, never overwrite existing expense data or dining log entries)
3. If not found → **create** a new page with `notion-create-pages`

### Page Title Format
```
[flag emoji] [Destination] · [Month Year]
```
Examples: `🇺🇸 Cleveland, Ohio · April 2026` / `🇲🇽 Mexico City · June 2026`

### Standard Page Structure

Refer to `references/notion-page-template.md` for the full Notion page content template.

Sections (in order):
1. 🗺️ **Trip Overview** — destination, dates, vehicle, departure charge, route summary
2. ⚡ **Supercharger Plan** — table of all charging stops with location, kW, amenities, rating
3. 🛻 **Overnight Truck Stops** — night-by-night table with Love's/Flying J location + amenities
4. 📅 **Day-by-Day Itinerary** — one section per day with time, activity, notes
5. 🏛️ **Attractions Detail** — expanded info for each major stop (hours, booking, tips)
6. 🚗 **Camp Mode Reference** — Tesla overnight tips (always include)
7. 📊 **Expense Tracker** — stub table ready for travel-expense-tracker to populate
8. 🍽️ **Dining Log** — stub ready for travel-expense-tracker to populate
9. ⚠️ **To-Do Before Trip** — checklist of action items

### Update Rules
- **Never overwrite** Expense Tracker or Dining Log sections if they have real data
- **Append** new activities to existing itinerary days rather than replacing
- **Search-replace** specific cells/rows when correcting data (e.g., wrong year)
- After every update, confirm the Notion page URL to the user

---

## Step 4 — Handoff to travel-expense-tracker

When the user provides receipts, cost estimates, or dining details:
- Flag that this belongs in the **travel-expense-tracker** workflow
- Both skills share the same Notion page — expense data goes into the 📊 and 🍽️ sections
- Do not duplicate expense processing here; defer to the expense tracker skill

---

## Step 5 — Confirm & Summarise

After updating Notion, always tell the user:
1. What was added or changed (bullet summary)
2. Any **action items** (e.g., "Book OSR tour", "Buy game tickets")
3. Any **flags or warnings** (e.g., "Game ends at 9pm — tight drive home", "Supercharger reviews flag safety concern at night")
4. The Notion page link

---

## Important Flags to Always Surface

- ⚠️ **Attractions that require advance booking** — mention prominently
- ⚠️ **Post-game drive timing** — if a game ends late + drive home is long, suggest truck stop option
- ⚠️ **Supercharger safety** — if reviews mention rough area, flag for daytime-only use
- ⚠️ **Attraction closure days** — cross-check hours against planned visit day
- ⚡ **Range anxiety check** — if any leg exceeds 350 km without a charger stop, flag it

---

## Tools to Use

| Task | Tool |
|---|---|
| Sports game lookup | `fetch_sports_data` |
| Attraction / charger locations | `places_search` |
| Hours, admission, booking info | `web_search` + `web_fetch` |
| Map display | `places_map_display_v0` |
| Create Notion page | `notion-create-pages` |
| Update Notion page | `notion-update-page` |
| Search for existing page | `notion-search` |

---

## Integration with travel-expense-tracker

Both skills write to the **same Notion page** under Travel Plans:

```
Travel Plans (page_id: 32724f54-8181-80c0-a063-e312b5dafca3)
└── 🇺🇸 Cleveland, Ohio · April 2026   ← shared page
    ├── 🗺️ Trip Overview          ← trip-planner owns this
    ├── ⚡ Supercharger Plan       ← trip-planner owns this
    ├── 🛻 Overnight Stops         ← trip-planner owns this
    ├── 📅 Day-by-Day Itinerary    ← trip-planner owns this
    ├── 🏛️ Attractions Detail      ← trip-planner owns this
    ├── 📊 Expense Tracker         ← travel-expense-tracker owns this
    ├── 🍽️ Dining Log              ← travel-expense-tracker owns this
    └── ⚠️ To-Do Before Trip       ← both skills contribute
```

When both skills are active in the same session:
- trip-planner creates the page first (if new trip)
- travel-expense-tracker appends to the expense and dining sections
- Neither skill overwrites the other's sections
