# Cashflow Forecast Configuration

Load this file when running a cashflow forecast. These are the fixed monthly inputs used in the forecast formula.

## Monthly Fixed Obligations

| Item | Amount (CAD) | Timing | Notes |
|------|-------------|--------|-------|
| Mortgage — Base | $1,050.00 | Bi-weekly | Regular amortization payment |
| Mortgage — Principal Accelerator | $115.00 | Bi-weekly | Additional principal paydown only; excluded from expense reporting |
| Mortgage — Total per payment | $1,165.00 | Bi-weekly | Combined amount transferred |
| Wealthsimple Contribution | Variable | Ad hoc | No fixed schedule — only when excess cash available |
| Questrade Contribution | Variable | Ad hoc | No fixed schedule — only when excess cash available |

> Mortgage payments should be classified as **Mortgage Payment (Transfer)** — never as an expense.
> The $115 principal accelerator is part of the same transfer; do not split into a separate category.
> Investment contributions: when they appear in the bank ledger, classify as **Investment Contribution (Transfer)** regardless of amount.

## Income Schedule

| Source | Amount (CAD) | Frequency | Notes |
|--------|-------------|-----------|-------|
| Employment Income | ~$7,585.50 | Twice monthly | ~$15,171/month after tax, paid in 2 instalments |

> Bi-monthly pay (not bi-weekly) — expect 2 income deposits per calendar month.
> Monthly total: ~$15,171 CAD after tax.

---

## Forecast Formula

```
Forecasted Month-End Balance =
  Current Balance
  + Remaining Expected Income         ← 2× per month at ~$7,585.50 each
  - Remaining Mortgage Payments       ← $1,165.00 per bi-weekly occurrence
  - Investment Contributions          ← variable / ad hoc only; use actuals if posted
  - Variable Spend Run-Rate

Variable Spend Run-Rate =
  (MTD variable expenses / days_passed) * remaining_days_in_month

Exclude anomalies > 2× typical monthly average from run-rate.
```

## Mortgage Bi-Weekly Occurrence Logic
A month typically contains 2 mortgage payments, occasionally 3 (when a month spans 3 bi-weekly periods).
- Standard month: 2 × $1,165 = $2,330 outflow
- 3-payment month: 3 × $1,165 = $3,495 outflow
- Check bank ledger for actual posted dates; use those to determine remaining payments in the month.

## Investment Contribution Logic
- Do NOT include a scheduled investment amount in the forecast.
- If Wealthsimple or Questrade transfers have already posted this month → include actuals.
- If none posted yet → do not project any; note "No investment contributions posted yet this month."

## Confidence Scoring
| Condition | Confidence |
|-----------|-----------|
| Income + mortgage configured, ≥15 days of MTD data | 85–95% |
| Income + mortgage configured, < 15 days MTD data | 60–75% |
| < 5 days MTD data | < 40% |

Always state assumptions and confidence % in forecast output.
