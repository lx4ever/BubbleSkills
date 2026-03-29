# QA / Verifier Checklist

Load this file during Step 5 (QA/Verify). Apply all rules by severity. Fix ERRORs before publishing. Flag WARNINGs in output. Log INFOs silently.

## ERROR — Must Fix Before Publishing
| Rule | Action |
|------|--------|
| RCSS-eligible item has no `proof_url` | Set `status = Missing-proof`; exclude from A section |
| `flyer_end` < today | Move to Watchlist only; do not rank |
| `unit_price` is null or 0 | Drop row |
| `store` or `item` is blank | Drop row |
| `category` not in approved list | Drop row |
| Duplicate `dedupe_key` already in History DB this week | Skip insert |

## WARNING — Flag in Output
| Rule | Action |
|------|--------|
| `unit_basis` mismatch in comparison (e.g. /lb vs /kg) | Add note "⚠️ unit basis mismatch — verify" |
| Image extraction returned < 3 items for a store | Add note "⚠️ low confidence extraction" |
| `flyer_start` > today (preview flyer) | Move to Watchlist; mark as preview |
| `source_type = image` with no page URL as proof | Note "image-sourced, page URL as proof" |

## INFO — Log Only
| Rule | Action |
|------|--------|
| Vision API returned non-JSON on first attempt | Log "re-extracting [store] page [N]" |
| History DB unreachable | Mark all lows as `🆕 First tracked`; continue |
| Store returned no usable items | Note "[Store]: No current data surfaced" |

## Minimum Publish Threshold
- If total ranked ready deals < 5 after QA: **do not publish to Notion**
- Report failure to user: "Only [N] deals passed QA this run — check sources"

## Schema Completeness Check
All published rows must have:
- `store`, `item`, `category`, `price`, `unit_price`, `unit_basis`
- `flyer_start`, `flyer_end`, `is_current = true`
- `proof_url` (RCSS-eligible rows only — mandatory)
- `source_type`, `status`, `low_badge`
