# QA Checklist — Family Finance Ledger

Load this file during the QA step of any intake or reconciliation run. Apply rules by severity before writing to Notion.

---

## ERROR — Block write, flag for review

| Rule | Action |
|------|--------|
| Credit card payment classified as Expense | Re-classify as Transfer; never write as Expense |
| Transaction appears in both bank ledger AND as receipt (same date, amount, merchant) | Keep bank entry only; mark receipt as reconciled |
| `amount` is null or 0 on a non-transfer row | Set `needs_review = true`; note "Amount missing" |
| Bank validation fails: `start_balance + net ≠ end_balance` (tolerance > $1) | Flag statement as incomplete; do not write partial data |
| Credit card reconciliation fails: tolerance > $1 | Flag period; do not mark reconciled |
| Duplicate dedupe key already exists in Notion | Skip insert; log "duplicate skipped" |

---

## WARNING — Write with flag

| Rule | Action |
|------|--------|
| LLM confidence < 0.7 on category | Set `needs_review = true`; write with best-guess category |
| Amount found only in PDF attachment (not email body) | Set `needs_review = true`; note "Amount in attachment — manual update required" |
| Merchant string is generic (e.g. "PURCHASE", "PAYMENT") | Set `needs_review = true`; note "Merchant unclear" |
| Receipt date differs from bank posted date by > 5 days | Note timing difference; keep both dates |
| Currency is not CAD | Flag for review; note original currency and amount |

---

## INFO — Log only

| Rule | Action |
|------|--------|
| Statement import found 0 new transactions (all duplicates) | Log "All transactions already imported for this period" |
| Gmail scan found 0 purchase emails in last 3 days | Log "No new purchase emails found" |
| Refund detected | Log as negative expense in original category |

---

## Never Do
- Never guess a merchant name if unclear
- Never treat an investment transfer as an expense
- Never treat a mortgage payment as an expense
- Never double-count a transaction across receipt and bank sources
- Never write to Notion if ERROR rules are unresolved
