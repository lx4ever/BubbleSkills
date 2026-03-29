# Category Filter Rules

Load this file before any deal extraction or QA step.

## Hard-Include Categories

| Category | Items |
|----------|-------|
| meat | beef, pork, ham, lamb, veal |
| poultry | chicken, turkey, duck |
| salmon/seafood | salmon, shrimp, tilapia, crab, lobster, fish fillets, scallops |
| fruits/vegetables | see extended list below |
| frozen food | frozen meat, seafood, dumplings, pizza, meals, vegetables |
| rice | all rice varieties |
| eggs | all egg products |

## Extended Produce Scan List
potatoes, mushrooms, onions, ginger root, lettuce, eggplant, cucumber, yam, sweet potato, pumpkin, grapes, cherry, orange, avocado, lotus root, yu choy, bok choy sprout, bean sprout, spinach, cauliflower, flat cabbage, broccoli, kale, beet, green onion, strawberries, cantaloupe, blackberries, apples, pears, mangoes

## Hard-Exclude
bakery, snacks, beverages, cleaning supplies, non-food items, personal care, household goods

## Bundle Deal Normalization
- "3 for $10" → `price = 3.33`, `notes = "3 for $10"`
- "2 for $5" → `price = 2.50`, `notes = "2 for $5"`

## Unit Normalization Rules
- Compare only same unit basis: `/lb` to `/lb`, `/kg` to `/kg`
- Do NOT cross-compare `/lb` vs `/kg` without converting
- Strip size suffixes before matching (e.g. "500g pkg" → normalize to per-unit price)
- Strip brand prefixes for generics

## Time-Window Policy
- Include: current active flyers only
- Watchlist only: preview flyers (not yet active)
- Exclude: expired flyers from ranking
