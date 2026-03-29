# Merchant Classification Rules

Load this file before classifying ANY transaction. Apply deterministic rules first. Use LLM fallback only if no rule matches.

## Rule Priority
1. Deterministic rules below (exact match, case-insensitive)
2. LLM category inference
3. If LLM confidence < 0.7 → set `needs_review = true`

---

## Deterministic Rules

### Investments → Transaction Type: Investment Contribution
| Merchant Pattern | Category |
|-----------------|----------|
| WEALTHSIMPLE | Investment Contribution |
| QUESTRADE | Investment Contribution |

### Mortgage → Transaction Type: Mortgage Payment
| Merchant Pattern | Category |
|-----------------|----------|
| CIBC MORTGAGE | Mortgage Payment |
| TD MORTGAGE | Mortgage Payment |
| INTERAC E-TRANSFER LONGMA369@HOTMAIL.COM | Mortgage Payment |
| EMT LONGMA369 | Mortgage Payment |

> Mortgage is paid bi-weekly at $1,165/payment ($1,050 amortization + $115 principal accelerator).
> Classify the full $1,165 as a single Mortgage Payment — do not split the $115 into a separate entry.
> Never classify any mortgage payment as an expense.

### Credit Card Payments → Transaction Type: Transfer
| Merchant Pattern | Category |
|-----------------|----------|
| VISA PAYMENT | Transfer |
| TD VISA PMT | Transfer |
| CREDIT CARD PAYMENT | Transfer |

**⚠️ Critical rule: Credit card payments are NEVER expenses. Always classify as Transfer.**

---

## LLM Fallback Category List
Use these category names only (do not invent new ones):

- Groceries
- Dining & Restaurants
- Gas & Fuel
- Transportation
- Shopping & Retail
- Entertainment
- Health & Pharmacy
- Utilities
- Subscriptions
- Investment Contribution
- Mortgage Payment
- Transfer
- Income
- Other

---

## Double-Count Prevention Rules
- A credit card payment appearing in BOTH the bank ledger AND credit card statement = Transfer only; never count as expense
- An investment transfer appearing in bank = Investment Contribution; never count as expense
- Mortgage payment = Mortgage Payment; never count as expense
- Refunds = negative expense in original category (do not create income entry)
