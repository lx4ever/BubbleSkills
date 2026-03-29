---
name: grocery-deals
description: Build a weekly grocery-deals report for Mimi using active flyers (text AND image-based), strict category filtering, 30-day historical lows detection, and automatic flyer image extraction via Claude vision API. Publishes to Notion/chat in RCSS price-match + Chinese stores + Costco sections. Use when asked to run grocery deals, compare flyers, produce proof-backed match items, update `Weekly Grocery Deals (Live)`, identify stock-up opportunities, or follow the L4G 0H2 grocery blueprint. Also use when asked to check Ranch Fresh, Centra, or any image-only flyer store.
---

# Grocery Deals

Run Mimi's weekly grocery workflow: deterministic filtering, ranking, proof gating, image-based flyer extraction, historical lows detection, and Notion publishing.

## Config Contract

Use these defaults unless the user overrides:
- `postal_code`: `L4G 0H2`
- `notion_page_title`: `Weekly Grocery Deals (Live)`
- `notion_live_page_id`: `23f7a51c-1360-83b3-ba8f-8189dfaed375`
- `notion_history_page_id`: `9057a51c-1360-8233-950e-0153de582489`
- `mimi_space_page_id`: `7b57a51c-1360-831c-9cd2-01f43afd0e1c`
- `history_db_id`: `9897a51c-1360-822c-af6b-81f1c14f4ae1`
- `history_db_collection_id`: `collection://a187a51c-1360-82bd-a39f-077063c6e32a`

---

## Pre-Run Intake (Optional — 10s gate)

Before starting, check if the user has specified any of the following. If not, proceed with all defaults:
1. Full run or specific stores only?
2. Publish to Notion, or chat output only?
3. Force-refresh History DB?

If no response, proceed with full run + Notion publish + normal DB query.

---

## Run Order (strictly follow this sequence)

**Step 1 → Load References**
**Step 2 → Query History DB**
**Step 3 → Scrape text-based flyers**
**Step 4 → Extract image-based flyers**
**Step 5 → Historical Lows Detection**
**Step 6 → QA / Verify**
**Step 7 → Rank**
**Step 8 → Publish to Notion**
**Step 9 → Write to History DB**

Gate conditions (DO NOT skip):
- Step 3 → Step 4: Proceed only if ≥1 text store returned data
- Step 4 → Step 5: Proceed only if all image agents attempted (success or logged failure)
- Step 6 → Step 8: **DO NOT publish** if total ready deals < 5 — report failure to user instead
- Step 8 → Step 9: Write to DB only after Notion publish confirms success

---

## Step 1: Load References (MANDATORY before any other step)

Load these files now. They are required for all downstream steps:

| File | Used in |
|------|---------|
| `references/store-registry.md` | Steps 3–4: store URLs, source types, image patterns |
| `references/category-filter.md` | Steps 3–4: what to extract; Step 6: what to reject |
| `references/qa-checklist.md` | Step 6: severity-graded QA rules |
| `assets/report-template.md` | Step 8: Notion page structure and line formats |
| `assets/vision-system-prompt.txt` | Step 4: canonical vision API system prompt |
| `scripts/discover-flyer-images.py` | Step 4: image URL discovery for all image-based stores |
| `scripts/normalize-item.py` | Steps 2, 5, 9: canonical item/unit/store normalization |

For agent prompts, load `references/prompt-pack.md` before dispatching subagents.

---

## Step 2: Historical Lows Pre-Query

Query `collection://a187a51c-1360-82bd-a39f-077063c6e32a` via `Notion:notion-fetch`. Pull all records from the last 30 days.

Build lookup table using `scripts/normalize-item.py`:
```
key   = history_key(store, item)   # → normalize_store(store) + "|" + normalize_item(item)
value = min(unit_price) seen in last 30 days
```

Apply unit normalization via `normalize_unit()` from `scripts/normalize-item.py`.

If unreachable: log warning, mark all lows as `🆕 First tracked`, continue.

---

## Step 3: Text-Based Flyer Scraping

Use store URLs from `references/store-registry.md`. Use `web_search` + `web_fetch` on flyerseek.com, flyers-on-line.com, cocoeast.ca for text-extractable stores.

Apply category hard-filter from `references/category-filter.md` during extraction.

---

## Step 4: Image-Based Flyer Extraction

For Metro, FreshCo, Ranch Fresh, and Centra.

### 4a. Discover Image URLs

Use `scripts/discover-flyer-images.py` to fetch listing pages and extract ordered image URLs for all image-based stores. This script handles:
- Primary and fallback URL chains per store
- SmartCanucks sub-link following for Ranch Fresh
- URL filter rules (include/exclude keywords, extensions)
- Page-number ordering
- web_fetch fallback if initial fetch returns no images

Run:
```
python3 scripts/discover-flyer-images.py --store all --json
```

Or per-store:
```
python3 scripts/discover-flyer-images.py --store "Ranch Fresh" --json
```

If `web_fetch` returns empty or no images for a store, retry that store's listing page using `web_search` to locate the current flyer URL, then re-run discovery with the found URL.

### 4b. Vision API Call (per image page)

Load `assets/vision-system-prompt.txt` as the system prompt (verbatim). Do not inline or paraphrase it.

```json
POST https://api.anthropic.com/v1/messages
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 2000,
  "system": "<contents of assets/vision-system-prompt.txt>",
  "messages": [{
    "role": "user",
    "content": [
      {"type": "image", "source": {"type": "url", "url": "<IMAGE_URL>"}},
      {"type": "text", "text": "Extract all grocery deals. Store: <STORE_NAME>. Return JSON array only."}
    ]
  }]
}
```

### 4c. Failure Handling

| Failure | Action |
|---------|--------|
| Image URL not found | Try fallback from `references/store-registry.md` |
| API returns non-JSON | Retry once; if still fails → Missing-proof |
| Image URL 403/404 | Log Missing-proof; add to Watchlist |
| Flyer period expired | Flag expired; Watchlist only |
| All pages fail | Note "image-only flyer not accessible this run" |

---

## Step 5: Historical Lows Detection

For each candidate from Steps 3 & 4:

1. Build lookup key using `scripts/normalize-item.py`:
   ```
   python3 scripts/normalize-item.py --history-key --store "<store>" --item "<item>"
   ```
2. Look up `prev_30d_low` from Step 2 table
3. Apply badge logic:

| Condition | `is_historical_low` | Badge | Stock-Up |
|-----------|--------------------|----|---|
| `unit_price ≤ prev_30d_low` | true | `🏆 30d LOW` | true |
| No prior history | true | `🆕 First tracked` | true |
| `unit_price > prev_30d_low` | false | — | unchanged |

4. `delta_vs_30d_low = unit_price - prev_30d_low`
5. Apply **+0.15 score bonus** for historical lows in Step 7 ranking

---

## Step 6: QA / Verify

Load `references/qa-checklist.md`. Apply all rules by severity:
- **ERROR**: fix or drop before publishing
- **WARNING**: flag in output
- **INFO**: log only

Gate: if total ready deals < 5 after QA → do not publish, report failure to user.

---

## Step 7: Ranking

```
base_score   = 0.45×unit_price_rank + 0.25×freshness + 0.20×matchability + 0.10×practicality
final_score  = base_score + (0.15 if is_historical_low else 0)
```

Hard filters: current only, RCSS eligibility, drop vague items.

---

## Step 8: Publish to Notion

Load `assets/report-template.md`. Populate each section with ranked results in the order specified.

1. Search `Notion:notion-search` for `Weekly Grocery Deals (Live)` at start of each run
2. If active → `replace_content` with new report
3. If archived/missing → create new page under Mimi's Space (`7b57a51c-1360-831c-9cd2-01f43afd0e1c`); update memory

All proof/source links must be clickable hyperlinks.

---

## Step 9: History DB Write

Collection: `collection://a187a51c-1360-82bd-a39f-077063c6e32a`

Build dedupe key using `scripts/normalize-item.py`:
```
python3 scripts/normalize-item.py --dedupe-key --store "<store>" --item "<item>" --unit "<unit>" --date "<YYYY-MM-DD>"
```

Populate all fields: `30d Low`, `Delta vs 30d Low`, `Stock-Up`, `Is Current`, `Dedupe Key`, `Source URL`.
- `Stock-Up = YES` if `is_historical_low = true`
- Skip insert if same `Dedupe Key` already exists this week

---

## Output Schema (row-level)

```json
{
  "store": "", "item": "", "category": "", "size": "",
  "price": 0.0, "unit_price": 0.0, "unit_basis": "/lb|/ea|/kg|/pkg",
  "flyer_start": "YYYY-MM-DD", "flyer_end": "YYYY-MM-DD",
  "is_current": true, "is_preview": false,
  "rcss_match_eligible": true, "proof_url": "",
  "source_type": "text|image", "status": "Ready|Missing-proof",
  "is_historical_low": false, "prev_30d_low": null,
  "delta_vs_30d_low": null, "low_badge": "🏆 30d LOW|🆕 First tracked|(none)",
  "notes": ""
}
```

---

## Subagent Framework

1. **Orchestrator** — load refs, run DB query, dispatch agents, merge/dedupe, rank, render
2. **RCSS Match Agent** — text flyers for RCSS-eligible stores + proof packaging
3. **Chinese Stores Agent** — Ranch Fresh + Centra + T&T (text + image)
4. **Costco Agent** — Costco Ontario highlights with validity windows
5. **Produce Deep-Scan Agent** — extended produce sweep + unit normalization
6. **Image Extraction Agent** — uses `scripts/discover-flyer-images.py` + vision API
7. **Historical Lows Agent** — uses `scripts/normalize-item.py` history_key(); compare vs 30d lookup, set badges
8. **QA/Verifier Agent** — applies `references/qa-checklist.md`, uses `normalize-item.py` dedupe_key() for duplicate checks

Full per-agent prompts: `references/prompt-pack.md`

---

## References Index

| File | Purpose |
|------|---------|
| `references/store-registry.md` | Store URLs, source types, image extraction patterns |
| `references/category-filter.md` | Hard-include categories, extended produce list, normalization rules |
| `references/qa-checklist.md` | Severity-graded QA checklist |
| `references/blueprint.md` | Workflow blueprint (background reference) |
| `references/prompt-pack.md` | Full per-agent prompts |
| `assets/report-template.md` | Notion page structure and line formats |
| `assets/vision-system-prompt.txt` | ⭐ Canonical vision API system prompt — single source of truth |
| `scripts/discover-flyer-images.py` | ⭐ Image URL discovery for Ranch Fresh, Centra, Metro, FreshCo |
| `scripts/normalize-item.py` | ⭐ Canonical item/unit/store normalization + dedupe/history key builders |
