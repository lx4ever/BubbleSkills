# Finance Summary Report Template

Load this file during the Report step. Populate each section with data from the current run. Do not omit section headers — use "No data this period" for empty sections.

---

## Header
```
📊 Family Finance Summary — [Month YYYY]
Generated: [YYYY-MM-DD]
Data through: [latest transaction date]
```

---

## 💳 Spending (Accrual Basis)
*Based on receipt/purchase dates — reflects when money was actually spent*

```
Total Spending:    $X,XXX.XX
Budget vs Actual:  [over/under] by $XXX.XX   ← omit if no budget set

Top Categories:
  1. [Category]    $X,XXX.XX   (XX%)
  2. [Category]    $X,XXX.XX   (XX%)
  3. [Category]    $X,XXX.XX   (XX%)

Needs Review:  X items — [brief description of flags]
```

---

## 🏦 Cashflow (Bank Basis)
*Based on bank posted dates — reflects actual money movement*

```
Income:            $X,XXX.XX
Outflow:           $X,XXX.XX
  → Expenses:      $X,XXX.XX
  → Transfers:     $X,XXX.XX   (CC payments, investments, mortgage)
Net:               $X,XXX.XX

Opening Balance:   $X,XXX.XX
Closing Balance:   $X,XXX.XX
Validation:        ✅ Balanced  |  ⚠️ Mismatch of $X.XX — review required
```

---

## 📈 Forecast
*Projected end-of-month position*

```
Current Balance:           $X,XXX.XX
Remaining Income:          $X,XXX.XX
Remaining Fixed (est.):   -$X,XXX.XX
Variable Run-Rate (est.): -$X,XXX.XX

Projected Month-End:       $X,XXX.XX
Confidence:                XX%

Assumptions:
- [e.g. Mortgage payment on DD expected]
- [e.g. Variable run-rate based on X days of data]
- [e.g. Fixed obligations not configured — variable only]
```

---

## ⚠️ Items Needing Review
```
X items flagged — review in Notion "Receipts & Purchases" filtered by Needs Review = true

Examples:
- [Merchant] [Date] $XX.XX — [reason]
```

*Omit this section if 0 items need review.*

---

## Footer
```
✅ [N] transactions written to Bank Ledger
✅ [N] receipts written to Receipts & Purchases
Last updated: [YYYY-MM-DD HH:MM]
```
