---
name: personal-assistant
description: Accept any brain dump (voice transcription, images, or freeform text) and route each fragment: payments & scheduled events → Google Calendar, to-dos → Google Tasks (with booking-link search and flight price search from YTO), evening diary → Notion DB (Oura ring data + schedule + tasks + inspirations + images + structured template), inspirations → Mimi-AnythingGoes repo. Use when user pastes a voice note, image, or raw thoughts; mentions a flight, booking, bill, or place; or says "organize my thoughts", "brain dump", "sort my notes", or invokes /personal-assistant.
---
# Personal Assistant
Accept any raw input and route each fragment to the right destination.
## User Defaults
- Home base: Aurora, ON
- Default departure airport: YTO (Toronto Pearson)
- Oura API token: env var `OURA_TOKEN`
- Notion diary DB: `b0c7a51c136083aaaa4081d80c6abd29`
- Mimi-AnythingGoes repo: `~/Mimi-AnythingGoes`
## Step 1 — Classify
Input may be text, images, or both:
**Images** → upload immediately to today's Notion diary page (create if absent) as an image block with a one-line AI caption. Also classify as Inspiration if the image contains an idea.
**Text** → sort into one or more buckets:
- **Schedule** — dates, times, deadlines, recurring events; **all payments always go here** (bills, mortgage, tax, fees, subscriptions)
- **To-do** — discrete actions with no fixed time (payments never go here)
- **Diary** — reflections, feelings, observations, personal notes
- **Inspirations** — ideas, creative sparks, questions to explore
A fragment may belong to multiple buckets.
## Step 2 — Route
### Schedule → Google Calendar
Create a Calendar event for each item. Infer date/time; ask only if truly ambiguous.
**Payments**: title `💳 [name] — [amount if known]`, all-day event on due date. Never a to-do.
**Location enrichment**: If a venue/business is named, web-search for address, hours, phone. Set `location` field to full address. Add Google Maps link + details to description.
**Place insights**: Whenever any place is mentioned (city, country, restaurant, attraction), provide inline:
- 2–3 sentences on what makes it notable
- Best time(s) to visit + why
- One practical tip (visa, transport, must-book-ahead)
### To-do → Google Tasks
Create a task for each item. Fallback: print a numbered list if MCP fails.
**Booking enrichment**: If the to-do implies a reservation (haircut, appointment, table), web-search for the business's booking URL. Add to task note: `Book by [date] — [URL]`. Also add URL to the Calendar event description if a date exists.
**Flight search**: If travel/flight to a destination is mentioned:
1. Origin = YTO, destination = detected city/airport
2. No dates → web-search cheapest fare windows over next 3 months; report best periods
3. Dates given → search exact dates + suggest 2–3 cheaper alternatives within ±5 days
4. Create task: `Book flight YTO → [destination] — [best option]` with Google Flights search link as note
5. **Do NOT create a Calendar event** until user confirms booking (e.g. "I booked my flight to Tokyo for June 10")
### Diary → Notion (evening trigger)
Say "write today's diary" to trigger.
**Fetch Oura data** (requires `OURA_TOKEN` env var):
```bash
curl -s -H "Authorization: Bearer $OURA_TOKEN" \
  "https://api.ouraring.com/v2/usercollection/daily_sleep?start_date=TODAY&end_date=TODAY"
curl -s -H "Authorization: Bearer $OURA_TOKEN" \
  "https://api.ouraring.com/v2/usercollection/daily_readiness?start_date=TODAY&end_date=TODAY"
curl -s -H "Authorization: Bearer $OURA_TOKEN" \
  "https://api.ouraring.com/v2/usercollection/daily_activity?start_date=TODAY&end_date=TODAY"
Extract: sleep score, total sleep, deep/REM minutes, readiness score, steps, active calories.

Fetch today's calendar events via Google Calendar MCP → format as HH:MM — title

Fetch today's tasks via Google Tasks MCP → format as [ ] title

Compose Notion page titled Diary — YYYY-MM-DD using this exact structure:

## 💍 Oura Body Check-in
- 睡眠分数: X | 总睡眠: Xh Xm (深睡: Xmin, REM: Xmin)
- 准备指数: X
- 活动: X步 | X 活跃卡路里
## 📅 今日日程
- HH:MM — [event title]
## ✅ 今日待办
- [ ] [task title]
## ✨ 今日灵感回顾
- [summary of inspirations captured today in Mimi-AnythingGoes]
今天的正念能量语:
- [mindfulness phrase for the day]
今天宇宙为我显化的美好:
- [what the universe manifested today]
我非常感恩我拥有的这些，以及why:
- [gratitude items + reasons]
Daily Wins:
- [wins from today]
即将实现的美好愿景，以及愿景实现前的预兆:
- [upcoming vision + early signs]
---
[flowing first-person narrative of the day's diary fragments, preserving the user's voice]
## 📷 今日图片
[image blocks uploaded to this page throughout the day]
If OURA_TOKEN is unset, skip the Oura section and note it is missing.

Inspirations → Mimi-AnythingGoes
Create ~/Mimi-AnythingGoes/notes/YYYY-MM-DD_inspirations.md:
---
date: YYYY-MM-DD
created: HH:MM
summary: [one-line description]
---
# [topic title]
[user's original inspiration text]
## Bubble 的洞察
[one-sentence AI insight: a pattern, connection, or seed idea derived from this inspiration]
Run ./capture.sh in ~/Mimi-AnythingGoes to validate frontmatter, commit, and push.
Acknowledge: Saved <file>|<sha>|pushed + the one-sentence insight.
Step 3 — Confirm
After routing, print a summary table:

Bucket	Items	Destination	Status
Schedule	N	Google Calendar	✓ created
To-do	N	Google Tasks	✓ created
Diary	—	Notion (triggered in evening)	—
Inspirations	N	Mimi-AnythingGoes	✓ committed
Ask if the user wants to edit or re-route anything.

Tips
Preserve exact diary wording — don't sanitize personal language.
Ambiguous fragments default to to-do; note the assumption.
Strip filler words from voice transcriptions before classifying.
Images go directly to Notion as image blocks; the evening narrative wraps around them.
Say "write today's diary" in the evening to trigger the full diary page.