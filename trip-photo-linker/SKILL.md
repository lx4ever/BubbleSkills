---
name: trip-photo-linker
description: Link exported travel photos to structured trip events from Notion, infer missing place context carefully, rank the best photos per event, and generate trip story records.
---

# Trip Photo Linker v2

## Trigger Phrases
Use any of the following to activate this skill:
- "Link my photos for [trip]"
- "Process my trip photos"
- "Organize photos from [destination]"
- "Match photos to my [destination] trip"
- "Run photo linker for [trip]"
- "Add photos to my trip"

## Purpose
This skill processes an exported photo folder or a selected set of travel photos and connects them to a structured trip record in Notion.

Compared with v1.1, this version adds:
- best photo ranking per event
- duplicate and near-duplicate suppression
- cover photo recommendation
- trip story generation
- stronger separation between confirmed facts and inferred narrative

## Scope
This skill does not parse receipts directly.
Receipt parsing is assumed to be handled by another skill that writes restaurant, dish, drink, and expense records into Notion.

## Inputs

### Required
- One Notion trip page or one trip database entry
- Related trip events stored in Notion
- One exported photo folder or one selected photo set

### Optional
- Receipt-derived structured data already present in Notion
- Reservation data
- Lodging data
- Manual itinerary notes
- Existing user preferences for favorite photo styles

## Outputs
- Photo records linked to trip events
- Confidence score and evidence breakdown
- Best-photo ranking per event
- Event cover photo recommendation
- Trip cover photo recommendation
- Trip story blocks or story records
- Review queue for ambiguous cases
- Unmatched queue for weak evidence

## Processing Stages
1. Normalize trip events from Notion
2. Extract photo metadata and scene evidence
3. Build moment clusters
4. Match photos and clusters to trip events
5. Rank photos within each event ← **load `references/photo-ranking-rubric.md` here**
6. Suppress duplicates and near-duplicates ← **rubric covers suppression rules**
7. Generate trip story outputs
8. Write structured records back to Notion

### Reference Files
| File | Load when |
|------|-----------|
| `references/photo-ranking-rubric.md` | Step 5 — before ranking any photos |

## Core Principles

### 1. Timeline-first matching
Match to trip events first.

### 2. Evidence hierarchy
Use:
- confirmed
- inferred
- unknown

### 3. No hallucination
Do not invent restaurants, attractions, or dish names.

### 4. Best-photo ranking happens after matching
Do not choose the best photo before the event match is established.

### 5. Story is grounded in facts
Trip story output may be narrative in style, but every factual statement must come from event data, image evidence, or a clearly labeled inference.

## Best Photo Ranking

**Load `references/photo-ranking-rubric.md` before executing this step.**

The rubric defines:
- Universal ranking criteria (clarity, composition, representativeness, uniqueness, etc.)
- Event-type-specific preferences (Restaurant, Transport, Hotel, Attraction, Truck Stop)
- Duplicate suppression rules and output labels (`top_pick`, `backup`, `duplicate_candidate`)
- Cover photo selection logic for both event-level and trip-level covers

To adapt ranking for a different trip style (e.g. foodie trip, architecture walk, family trip),
swap out `references/photo-ranking-rubric.md` — the core skill logic here stays unchanged.

After photos are matched to an event, follow the rubric to rank them and assign output labels.
Never select a cover photo before the event match is established (Core Principle #4).

## Story Generation
Generate story records only after matching and ranking are complete.

Possible outputs:
- one summary per event
- one trip timeline recap
- one short narrative album order

Story text must:
- separate confirmed facts from inferred context
- avoid overclaiming exact place names when confidence is low
- prefer grounded, descriptive language

## Output Types

### Type A — Confirmed event match
Example:
- Dinner at Marble Room

### Type B — Inferred place match
Example:
- Possible dinner at Marble Room

### Type C — Category only
Example:
- Restaurant meal in downtown Cleveland

## Review Rules
Set `review_required = true` when:
- confidence is moderate
- multiple event alternatives are plausible
- place is inferred rather than confirmed
- dish name is inferred
- top photo ranking is not clearly separated from backups

## Future Upgrade Path
Future versions may add:
- user-specific aesthetic preferences
- face-quality scoring
- social-share album formatting
- automatic caption variants
- trip map visualization
