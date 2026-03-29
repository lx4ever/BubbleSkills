# Notion Database Configuration

Load this file at the start of any run that writes to Notion.

## Database IDs

| Database | Notion ID | Used For |
|----------|-----------|----------|
| Receipts & Purchases | 68db5aa4-2caa-4bbc-9ae0-7f985bed99cc | Receipt images, online purchase emails, manual entries |
| Bank Ledger | *(search by title if ID unknown)* | Bank statement transactions |
| Monthly Summary | *(search by title if ID unknown)* | Cashflow forecasts, monthly anchors |

> If a database ID is unknown: use `Notion:notion-search` with the database name to locate it. Update this file with the found ID.

---

## Field Schemas

### Receipts & Purchases
| Field | Type | Notes |
|-------|------|-------|
| Merchant | Title | Store or vendor name |
| Date | Date | Receipt/purchase date (accrual) |
| Amount | Number | Total charged |
| Category | Select | From approved category list |
| Payment Method | Select | Cash, Visa, Debit, etc. |
| Transaction Type | Select | Expense, Transfer, Investment, Mortgage |
| Source | Select | Receipt Image, Gmail, Manual |
| Order ID | Text | For online purchases |
| Needs Review | Checkbox | true if confidence < 0.7 or amount missing |
| Notes | Text | Extraction notes, review reasons |

### Bank Ledger
| Field | Type | Notes |
|-------|------|-------|
| Description | Title | Raw merchant string from bank |
| Posted Date | Date | Bank posted date (cash basis) |
| Amount | Number | Positive = inflow, negative = outflow |
| Category | Select | From approved category list |
| Transaction Type | Select | Expense, Transfer, Investment, Mortgage, Income |
| Statement Period | Text | YYYY-MM (e.g. 2026-03) |
| Needs Review | Checkbox | true if unclassified |
| Dedupe Key | Text | `posted_date|amount|description` |

---

## Dedupe Policy
Before inserting any record:
- Build `dedupe_key = posted_date + "|" + amount + "|" + normalize(description)`
- If same key already exists in database → skip insert, log "duplicate skipped"
- Never insert the same transaction twice across multiple statement imports
