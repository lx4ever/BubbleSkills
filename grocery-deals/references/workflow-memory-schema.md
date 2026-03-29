# Workflow Memory Schema

Use one of these persistence backends. Prefer them in this order unless the environment dictates otherwise:
1. Notion workflow-memory database
2. Local JSONL log file
3. Vector memory store with the same metadata

## Canonical fields

Required fields for every execution memory:
- `skill`
- `run_timestamp`
- `trigger_pattern`
- `scope`
- `status`
- `stores_attempted`
- `history_mode`
- `blocking_step`
- `fallbacks_used`
- `publish_succeeded`
- `next_run_note`

Optional fields:
- `user_request_excerpt`
- `deal_count_ready`
- `image_store_failures`
- `text_store_failures`
- `history_db_status`
- `publish_target`
- `dedupe_key`

## Canonical JSON shape

```json
{
  "skill": "grocery-deals",
  "run_timestamp": "2026-03-29T10:00:00-04:00",
  "trigger_pattern": "weekly grocery flyer run",
  "scope": "full run + notion publish",
  "status": "success",
  "stores_attempted": ["RCSS", "No Frills", "Metro", "FreshCo"],
  "history_mode": "normal",
  "blocking_step": "none",
  "fallbacks_used": ["web search recovery for flyer URL"],
  "publish_succeeded": true,
  "next_run_note": "Metro image discovery required fallback flyer URL search."
}
```

## Notion property mapping

Map canonical fields to these Notion properties:
- Title → `Run Title`
- Rich text → `Trigger Pattern`
- Select → `Scope`
- Select → `Status`
- Multi-select → `Stores Attempted`
- Select → `History Mode`
- Select → `Blocking Step`
- Multi-select → `Fallbacks Used`
- Checkbox → `Publish Succeeded`
- Rich text → `Next Run Note`
- Date → `Run Timestamp`
- Number → `Ready Deal Count`
- URL → `Publish Target`
- Rich text → `User Request Excerpt`

## Dedupe logic

Memory entries should dedupe on:
`skill + normalized trigger_pattern + scope + calendar_week`

If a matching memory already exists for the same week:
- update the existing entry if the new run has a clearer `next_run_note`
- otherwise append a new entry only when the status changed materially
