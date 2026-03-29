---
name: "family-finance-ledger"
description: "Family finance tracking skill for Mimi. Processes receipt images, bank statement PDFs, credit card statements, and Gmail purchase confirmation emails into a structured Notion ledger with accrual vs cash separation, credit card reconciliation, and monthly cashflow forecasting. Use this skill aggressively — trigger whenever Mimi: uploads any receipt image or PDF; mentions 'log my spending', 'process my receipts', 'update my ledger', 'bank statement', 'how much did we spend', 'reconcile', 'monthly summary', 'cashflow forecast', 'finance update'; or uploads any file that looks like a bank or credit card statement. Also trigger when scanning Gmail if the user mentions purchases, invoices, or order confirmations."
version: "2.0.0"
---

# Family Finance Ledger

Process Mimi's family finances: receipts, bank statements, Gmail purchase emails → Notion ledger with accrual/cash separation, reconciliation, and forecasting.

---

## Pre-Run Intake (Quick gate — ask only if ambiguous)

Before starting, confirm what's being processed if not obvious from context:
1. What's being uploaded or requested? (receipt / bank statement / credit card statement / Gmail scan / monthly summary / forecast)
2. Which month/period? (default: current month)
3. Notion output, chat summary, or both? (default: both)

If the user has already made this clear, skip and proceed directly.

---

## References Index — Load Before Acting

| File | Load When |
|------|-----------|
| `references/merchant-rules.md` | Before classifying ANY transaction |
| `references/notion-config.md` | Before writing to ANY Notion database |
| `references/qa-checklist.md` | Before writing any batch of records |
| `references/forecast-config.md` | When running cashflow forecast |
| `assets/summary-template.md` | When generating any summary or report |

---

## Core Accounting Rules (always enforced)

**Accrual basis** = spending reports use receipt/purchase date
**Cash basis** = cashflow reports use bank posted date

These may differ due to credit card timing — never conflate them.

**Credit card payments = Transfer, always.** Never classify as expense.
**Investment transfers = Investment Contribution.** Never classify as expense.
**Mortgage payments = Mortgage Payment.** Never classify as expense.

Full merchant classification rules: `references/merchant-rules.md`

---

## Run Order by Task Type

### Task A: Receipt Intake (image or PDF upload)

1. Load `references/merchant-rules.md`
2. Extract from image/PDF: merchant, date, total, payment method
3. Classify using deterministic rules → LLM fallback
4. If confidence < 0.7 → `needs_review = true`
5. Run QA (`references/qa-checklist.md`)
6. Load `references/notion-config.md` → write to Receipts & Purchases
7. Confirm written records to user

---

### Task B: Gmail Purchase Email Scan

**Only run when user explicitly requests a ledger update or finance scan — not during general email triage.**

1. Load `references/merchant-rules.md`
2. Search Gmail: `in:inbox newer_than:3d (receipt OR invoice OR order confirmation OR purchase OR payment confirmation)`
3. For each match: extract merchant, order date, amount, currency, payment method, order ID, status
4. Classify using deterministic rules → LLM fallback
5. If amount not in email body → `needs_review = true`, note "Amount in attachment — manual update required"
6. Status mapping:
   - Order confirmed / in progress → Pending / Confirmed
   - Shipped → Confirmed
   - Delivered → Confirmed
7. Run QA (`references/qa-checklist.md`)
8. Load `references/notion-config.md` → write to Receipts & Purchases (ID: 68db5aa4-2caa-4bbc-9ae0-7f985bed99cc)
9. Never skip a matching email — log all found purchases

---

### Task C: Bank Statement Import (PDF)

1. Load `references/merchant-rules.md`
2. Extract from PDF: start_date, end_date, start_balance, end_balance, all transactions
3. Normalize amounts: positive = inflow, negative = outflow
4. Classify each transaction (deterministic first, LLM fallback)
5. **Validate:** `start_balance + net_transactions == end_balance` (tolerance ±$1)
   - If mismatch > $1 → flag statement incomplete; do not write
6. Check dedupe keys against existing Bank Ledger records
7. Run QA (`references/qa-checklist.md`)
8. Load `references/notion-config.md` → write new records to Bank Ledger
9. Report: X new records written, Y duplicates skipped, validation result

---

### Task D: Credit Card Reconciliation

```
opening_balance
+ receipt_purchases (accrual period)
- bank_transfers (CC payments from bank ledger)
= closing_balance

Tolerance: ±$1
```

If mismatch > $1 → flag period; list unmatched items for review.

---

### Task E: Monthly Summary & Forecast

1. Load `references/forecast-config.md`
2. Load `assets/summary-template.md`
3. Pull MTD data from Bank Ledger and Receipts & Purchases
4. Run monthly anchor validation:
   - `end_balance - start_balance == net_bank_transactions` (tolerance ±$1)
   - If mismatch → flag for review
5. Calculate forecast using formula in `references/forecast-config.md`
6. Populate `assets/summary-template.md` with actuals + forecast
7. Output to chat; optionally write to Notion Monthly Summary page

---

## QA Gate (apply before every Notion write)

Load `references/qa-checklist.md`. Resolve all ERROR-level issues before writing.
WARNING-level issues → write with `needs_review = true`.
Never double-count. Never write unresolved ERROR rows.

---

## Error Handling

| Situation | Action |
|-----------|--------|
| Merchant unrecognized | LLM fallback; if < 0.7 confidence → needs_review |
| Amount missing | needs_review = true; note reason |
| Bank validation fails | Do not write; report mismatch to user |
| Notion database ID unknown | Search by title using notion-config.md guidance |
| Duplicate transaction | Skip insert; log "duplicate skipped" |
| PDF unreadable | Report to user; request re-upload or manual entry |
