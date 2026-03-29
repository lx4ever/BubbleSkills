# Photo Ranking Rubric

This file defines how to score and rank photos within a matched trip event.
Load this file during Step 5 (Rank photos within each event).

To swap rubrics for a different trip type (e.g. "foodie trip", "architecture walk",
"family trip"), replace this file — the core skill logic stays unchanged.

---

## Universal Ranking Criteria

Apply these to every photo, regardless of event type. Score each signal independently,
then combine to produce a rank order. Do not require all signals to be present.

| Signal | Weight | Notes |
|--------|--------|-------|
| Clarity and sharpness | High | Blurry or dark photos rank low regardless of content |
| Composition quality | High | Rule of thirds, framing, avoiding clutter |
| Representativeness of the event | High | Does this photo clearly show what the event was? |
| Uniqueness | Medium | Penalise near-identical framing/content within the same event |
| Emotional or storytelling value | Medium | Does it convey mood, scale, or a moment? |
| Explicit connection to event data | Medium | Matches known venue name, dish, attraction, etc. |
| Low duplication score | Medium | Flag if nearly identical timestamp or framing to another photo |

---

## Event-Type Ranking Preferences

### Transport
Prefer:
- Strong road or route shot showing landscape or progress
- Border crossing, station, gas stop, or arrival cue
- Supercharger stop with identifiable context

Avoid:
- Repeated blurry dashboard shots
- Dark or featureless highway photos

---

### Restaurant / Dining
Prefer:
- Best plated food shot (well-lit, clear dish identity)
- Best interior or ambiance shot (captures atmosphere)
- Best people-at-table shot when available

Avoid:
- Dark duplicates
- Multiple near-identical shots of the same dish
- Menu photos when food shots exist (menu → backup_only)

---

### Hotel / Accommodation
Prefer:
- Best room shot (shows space and quality)
- Best view shot (window or balcony)
- Best exterior or lobby shot (establishes the property)

Avoid:
- Bathroom-only shots unless no other room photo exists
- Check-in desk photos (low storytelling value)

---

### Attraction / Landmark
Prefer:
- Clearest landmark shot (identifiable, sharp)
- Strongest scene-setting shot (shows scale or context)
- Best human-in-context shot (person in front of landmark)

Avoid:
- Duplicate angles of the same landmark
- Heavily backlit shots where subject is silhouette only

---

### Truck Stop / Overnight Stop
Prefer:
- Exterior shot showing the stop (Love's / Flying J signage if visible)
- Tesla at Supercharger if charging occurred
- Any shot that establishes the overnight location

Avoid:
- Interior restroom / vending shots
- Dark parking lot shots with no distinguishing features

---

## Duplicate Suppression Rules

Near-duplicates should not all survive as top-ranked records.

Signals of duplication:
- Nearly identical timestamps (< 30 seconds apart)
- Same framing or content labels from vision analysis
- Same location with minimal visual variation

Action:
- Keep one or two strongest representatives as `top_pick` or `backup`
- Mark the rest as `duplicate_candidate` or `backup_only`
- Never surface a `duplicate_candidate` as the event cover photo

---

## Cover Photo Selection

### Event cover photo
- Must be `top_pick` rank
- Must have `review_required = false` (or be the only option)
- Prefer the photo with the highest representativeness score for that event type

### Trip cover photo
- Select from all event cover photos
- Prefer: hero landmark shot, or best dining/atmosphere shot if no landmark exists
- Avoid: transport or truck stop photos as trip cover unless no alternative exists

---

## Output Labels

| Label | Meaning |
|-------|---------|
| `top_pick` | Best photo for this event; eligible for cover |
| `backup` | Good quality; surfaced if top_pick is unavailable |
| `backup_only` | Kept but not surfaced by default |
| `duplicate_candidate` | Near-duplicate; candidate for pruning |
