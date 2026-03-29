---
name: grocery-deals
description: Build Mimi's weekly grocery-deals report using active flyers, image extraction, strict category filtering, QA gating, 30-day historical-low detection, and Notion publishing. Trigger this skill when the user asks to run grocery deals, compare flyers, find price-matchable items, identify stock-up opportunities, update the Weekly Grocery Deals page, or check flyer-only stores such as Ranch Fresh, Centra, Metro, or FreshCo.
---

# Grocery Deals

This skill follows a self-diagnosing execution pattern:
1. Trigger check
2. Execution plan
3. Deterministic run sequence
4. Validation and QA gates
5. Post-run self-diagnosis
6. Workflow memory write

---

## 0) Config Contract

Use these defaults unless the user overrides them.

- `postal_code`: `L4G 0H2`
- `notion_page_title`: `Weekly Grocery Deals (Live)`
- `notion_live_page_id`: `23f7a51c-1360-83b3-ba8f-8189dfaed375`
- `notion_history_page_id`: `9057a51c-1360-8233-950e-0153de582489`
- `mimi_space_page_id`: `7b57a51c-1360-831c-9cd2-01f43afd0e1c`
- `history_db_id`: `9897a51c-1360-822c-af6b-81f1c14f4ae1`
- `history_db_collection_id`: `collection://a187a51c-1360-82bd-a39f-077063c6e32a`

---

## 1) Skill Trigger Check (MANDATORY before any action)

Before using any tool, explicitly perform this decision block internally.

### 1.1 User Intent Check
Determine whether the request is asking for one or more of the following:
- Weekly grocery-deals run
- Flyer comparison across stores
- RCSS matchable deal identification
- Stock-up opportunity detection
- Live page refresh / Notion publish
- Review of image-only flyers
- Historical-low comparison using the deal database

### 1.2 Trigger Rules
Trigger this skill when the request includes any of these patterns:
- “run grocery deals”
- “check flyers”
- “compare grocery flyers”
- “find grocery deals this week”
- “price match”
- “stock up”
- “update Weekly Grocery Deals”
- “check Ranch Fresh / Centra / Metro / FreshCo flyer”

Do **not** trigger this skill when the user only wants:
- General meal ideas
- Nutrition guidance unrelated to current flyer pricing
- A single-store factual question not requiring the workflow
- A shopping list without flyer/deal analysis

### 1.3 Trigger Decision Output
Internally resolve:
- `skill_triggered`: YES / NO
- `trigger_reason`: one sentence
- `scope`: full run / store-specific / chat-only / publish

If `skill_triggered = NO`, do not use this skill.

---

## 2) Pre-Execution Self-Check

Before Step 3, confirm the run can be executed.

### 2.1 Required Inputs
Minimum required inputs:
- Store registry
- Category filter
- QA checklist
- Report template
- Vision prompt
- Image discovery script
- Normalization script

### 2.2 Optional Intake Gate
Check whether the user specified:
1. Full run or specific stores only
2. Publish to Notion or chat-only output
3. Force-refresh History DB

If not specified, proceed with:
- Full run
- Notion publish
- Normal DB query

### 2.3 Execution Readiness Test
Confirm:
- References are loadable
- Needed tools are available
- Store scope is known
- Output target is known

If any required reference is unavailable, stop and report which dependency blocked execution.

### 2.4 Memory Readiness Test
Before execution, determine which persistence target is available for workflow memory:
- Notion workflow-memory DB
- Local JSONL log
- Vector memory store

If none are available, continue the run but return the self-diagnosis in chat only and mark memory persistence as unavailable.

---

## 3) Tool Selection Rules

Use tools only for the purpose below.

| Need | Tool / Resource | Rule |
|---|---|---|
| Store/source definitions | `references/store-registry.md` | Always load first |
| Inclusion/exclusion rules | `references/category-filter.md` | Apply during extraction and QA |
| QA logic | `references/qa-checklist.md` | Apply before ranking/publish |
| Output format | `assets/report-template.md` | Use for final report formatting |
| Vision extraction prompt | `assets/vision-system-prompt.txt` | Use verbatim, do not paraphrase |
| Flyer image discovery | `scripts/discover-flyer-images.py` | Use for image-based flyer stores |
| Key normalization | `scripts/normalize-item.py` | Use for history keys and dedupe keys |
| Agent prompt fragments | `references/prompt-pack.md` | Load before subagent dispatch |
| Flyer text pages | web search/fetch tools | Use for text-based flyer scraping |
| Historical record query | Notion fetch/search | Use only for the history DB and live page |
| Publish/update | Notion create/replace tools | Only after QA gate passes |

### Tool Safety Rules
- Never publish before QA gate passes.
- Never write to history DB before publish succeeds.
- Never bypass normalization for history or dedupe comparison.
- Never inline or rewrite the canonical vision system prompt.
- Never treat an unverified flyer extraction as ready-to-publish proof.

---

## 4) Execution Plan Template

Internally create this plan before running:

### 4.1 Inputs
- Store scope
- Publish mode
- History query mode
- Required references and scripts

### 4.2 Steps
1. Load references
2. Query 30-day history
3. Scrape text-based flyers
4. Extract image-based flyers
5. Compute historical-low flags
6. Run QA and drop/fix invalid items
7. Rank deals
8. Publish to Notion or prepare chat output
9. Write accepted items to history DB

### 4.3 Success Condition
A successful run means:
- Required references loaded
- All in-scope flyer sources attempted
- QA completed
- At least 5 ready deals remain
- Output generated successfully
- History write completed only after publish success

### 4.4 Failure Conditions
Common failure cases:
- No text stores returned data
- Image discovery failed for image-only stores
- Vision extraction returned unusable JSON
- History DB unavailable
- Ready deals fewer than 5 after QA
- Notion publish failed

### 4.5 Fallback Rules
- If history DB is unreachable, continue and mark all lows as `🆕 First tracked`
- If an image-based store fails, log it and continue with other stores
- If publish fails, do not write history DB
- If total ready deals < 5, return a failed-run summary instead of publishing

---

## 5) Deterministic Run Order (STRICT)

Run in this exact sequence.

1. Load references
2. Query History DB
3. Scrape text-based flyers
4. Extract image-based flyers
5. Historical lows detection
6. QA / verify
7. Rank
8. Publish to Notion or format chat output
9. Write to History DB

### Gate Conditions
- Step 3 → Step 4: proceed only if at least one text store returned data
- Step 4 → Step 5: proceed only after all image stores were attempted, whether successful or failed
- Step 6 → Step 8: do not publish if ready deals < 5
- Step 8 → Step 9: write history only after publish confirms success

---

## 6) Step-by-Step Execution Specification

### Step 1 — Load References (MANDATORY)
Load all of the following before any scraping or publishing:
- `references/store-registry.md`
- `references/category-filter.md`
- `references/qa-checklist.md`
- `assets/report-template.md`
- `assets/vision-system-prompt.txt`
- `scripts/discover-flyer-images.py`
- `scripts/normalize-item.py`
- `references/prompt-pack.md` before dispatching subagents
- `references/workflow-memory-schema.md` before final memory write

If any required file is missing, stop and report the missing dependency.

### Step 2 — Historical Lows Pre-Query
Query `collection://a187a51c-1360-82bd-a39f-077063c6e32a` for records from the last 30 days.

Build lookup table using `scripts/normalize-item.py`:
```text
key   = history_key(store, item)
value = min(unit_price) seen in last 30 days
```

Apply `normalize_unit()` during comparison.

If unreachable:
- log warning
- mark all lows as `🆕 First tracked`
- continue run

### Step 3 — Text-Based Flyer Scraping
Use store URLs from `references/store-registry.md`.
Use web search/fetch on text-extractable sources such as Flyerseek, Flyers Online, and Cocoeast where applicable.

Apply category hard-filter from `references/category-filter.md` during extraction.

### Step 4 — Image-Based Flyer Extraction
Target image-based stores including Metro, FreshCo, Ranch Fresh, and Centra.

#### 4a. Discover Image URLs
Run:
```bash
python3 scripts/discover-flyer-images.py --store all --json
```

Or per store:
```bash
python3 scripts/discover-flyer-images.py --store "Ranch Fresh" --json
```

If listing-page fetch returns no images:
- retry by locating the current flyer URL via web search
- rerun discovery with the discovered URL

#### 4b. Vision API Call
Use `assets/vision-system-prompt.txt` verbatim as the system prompt.
Do not paraphrase it.

Expected request form:
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

#### 4c. Failure Handling
- Image URL not found → try fallback source from store registry
- API returns non-JSON → retry once; if still invalid, mark missing proof
- Image URL 403/404 → log missing proof and add to watchlist
- Flyer period expired → mark expired and watchlist only
- All pages fail for a store → note that the image-only flyer was inaccessible this run

### Step 5 — Historical Lows Detection
For each candidate from Steps 3 and 4:
1. Build history key using `scripts/normalize-item.py`
2. Look up `prev_30d_low`
3. Apply badge logic

| Condition | `is_historical_low` | Badge | Stock-Up |
|---|---:|---|---:|
| `unit_price ≤ prev_30d_low` | true | `🏆 30d LOW` | true |
| No prior history | true | `🆕 First tracked` | true |
| `unit_price > prev_30d_low` | false | — | unchanged |

4. Compute `delta_vs_30d_low = unit_price - prev_30d_low`
5. Add `+0.15` ranking bonus when `is_historical_low = true`

### Step 6 — QA / Verify
Load `references/qa-checklist.md` and apply all checks.

Severity handling:
- `ERROR` → fix or drop before publish
- `WARNING` → keep but flag
- `INFO` → log only

Gate rule:
- if ready deals < 5 after QA, do not publish
- instead return a failed-run diagnostic summary

### Step 7 — Ranking
Use:
```text
base_score  = 0.45×unit_price_rank + 0.25×freshness + 0.20×matchability + 0.10×practicality
final_score = base_score + (0.15 if is_historical_low else 0)
```

Hard filters:
- current only
- RCSS eligible where required
- drop vague or insufficiently proven items

### Step 8 — Publish to Notion
Load `assets/report-template.md` and populate sections in the specified order.

Publish procedure:
1. Search for `Weekly Grocery Deals (Live)` at start of run
2. If active, replace page content
3. If archived or missing, create a new page under Mimi's Space and update stored page reference

All proof and source links must remain clickable.

### Step 9 — History DB Write
Write only after publish succeeds.

Build dedupe key using:
```bash
python3 scripts/normalize-item.py --dedupe-key --store "<store>" --item "<item>" --unit "<unit>" --date "<YYYY-MM-DD>"
```

Populate all required fields:
- `30d Low`
- `Delta vs 30d Low`
- `Stock-Up`
- `Is Current`
- `Dedupe Key`
- `Source URL`

Rules:
- `Stock-Up = YES` if `is_historical_low = true`
- skip insert if the same dedupe key already exists for the current week

---

## 7) Validation Checklist Before Final Output

Before returning results, verify all of the following:
- Correct skill was triggered
- Scope matched user request
- All mandatory references were loaded
- All in-scope stores were attempted
- Category filter was applied
- History normalization was applied
- QA completed
- No publish occurred with fewer than 5 ready deals
- No history DB writes occurred before publish success
- Final report links are clickable

---

## 8) Post-Execution Self-Diagnosis (MANDATORY)

After every run, internally evaluate:

### 8.1 Trigger Accuracy
- Was this the right skill?
- Was the scope correct?
- Was a full run used when store-specific would have been better?

### 8.2 Execution Outcome
- `run_status`: success / partial / failed
- Which step failed, if any?
- Was failure due to source access, parsing, QA, publish, or DB write?

### 8.3 Tool Performance Review
For each major tool or dependency, note:
- worked as expected
- worked with fallback
- failed and was bypassed
- failed and blocked run

### 8.4 Improvement Note
Record one concise lesson such as:
- “Ranch Fresh flyer URL changed; web search recovery path worked.”
- “Vision extraction for Centra returned non-JSON twice; needs stricter repair step.”
- “History DB unavailable; fallback first-tracked mode preserved workflow.”

---

## 9) Workflow Memory Write

At the end of the run, save or update a compact execution memory containing:
- Trigger pattern
- Scope used
- Stores attempted
- Failure points
- Fallbacks that worked
- Whether publish succeeded
- One improvement note for the next run

Load `references/workflow-memory-schema.md` before writing memory.

### Preferred Backends
Use these backends in this order:
1. Notion workflow-memory database if configured
2. Local JSONL append log via `scripts/log-workflow-memory.py`
3. Vector memory store using the canonical fields from `references/workflow-memory-schema.md`

### Memory Format
Use this compact structure:
```yaml
skill: grocery-deals
trigger_pattern: "weekly grocery flyer run"
scope: "full run + notion publish"
status: "success | partial | failed"
stores_attempted:
  - RCSS
  - No Frills
  - Ranch Fresh
history_mode: "normal | fallback-first-tracked"
blocking_step: "none | step number"
fallbacks_used:
  - "web search recovery for flyer URL"
  - "history DB fallback"
publish_succeeded: true
next_run_note: "Concise lesson learned"
```

### Write Procedure
1. Build canonical payload using the schema reference.
2. Prefer a Notion insert/update when a workflow-memory database is available.
3. If Notion memory is unavailable, append locally:
```bash
python3 scripts/log-workflow-memory.py   --payload '{"skill":"grocery-deals","trigger_pattern":"weekly grocery flyer run","scope":"full run + notion publish","status":"partial","stores_attempted":["RCSS","Metro"],"history_mode":"normal","blocking_step":"4","fallbacks_used":["web search recovery for flyer URL"],"publish_succeeded":false,"next_run_note":"Metro image extraction needs stricter JSON repair."}'
```
4. If a vector memory store exists, upsert the same canonical payload rather than free-form notes.

### Memory Safety Rules
- Do not store full user transcript text.
- Do not store raw flyer page dumps.
- Do not store duplicate memories for the same run unless status changed materially.
- Store operational lessons only.

---

## 10) Quick Failure Response Template

If the run cannot complete, respond with:
- what was attempted
- what failed
- what was still recovered
- whether publish was skipped
- what should be retried next run

Example structure:
```text
Grocery deals run was partially completed.
Completed: references, history query, text flyer scrape.
Failed: Centra and Ranch Fresh image extraction due to inaccessible flyer pages.
Recovered: ranked 8 verified deals from text-based stores.
Publish: skipped because only 4 ready deals passed QA.
Next retry focus: recover current image flyer URLs for Centra and Ranch Fresh.
```

---

## 11) Success Standard

This skill is considered well executed only when it:
- triggers for the right requests
- uses the correct tools in the correct order
- preserves proof and QA integrity
- publishes only valid output
- writes history only after publish success
- captures one reusable lesson for the next run
