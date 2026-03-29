# Grocery Deals Blueprint (Mimi)

## Objective
Produce weekly grocery report for L4G 0H2:
1) Historical Lows callout (mandatory)
2) RCSS price-match-ready deals (with proof)
3) Chinese stores top deals (Ranch Fresh · Centra · T&T)
4) Costco highlights
5) Optional preview watchlist (non-ranked)

## Flyer Source Strategy

### Text-extractable stores (web_search + web_fetch):
- No Frills → flyerseek.com
- Food Basics → flyerseek.com
- Walmart → flyerseek.com
- T&T Supermarket → flyers-on-line.com
- Costco → cocoeast.ca

### Image-only stores (Image Extraction Agent required):
- **Ranch Fresh Supermarket** → flyers.smartcanucks.ca/ranch-fresh-supermarket-canada (primary) OR ranchfresh.ca/index1.html (fallback)
- **Centra Food Market Aurora** → flyers-on-line.com/centra-food-market/aurora (primary) OR centrafoods.ca/pages/weekly-deals (fallback)
- **Metro** → flyerseek.com (image) → SmartCanucks fallback
- **FreshCo** → flyerseek.com (image) → SmartCanucks fallback

### Image Extraction Agent workflow (for image-only stores):
1. Fetch flyer listing page HTML
2. Parse and extract all flyer image URLs (filter by: flyer/page/upload keywords, jpg/jpeg/png/webp extensions, exclude logos/icons)
3. For each image URL → call Anthropic vision API → get structured JSON deals
4. Validate flyer dates are current
5. Return deals in standard row schema

## Historical Lows Policy (mandatory every run)
- Query History DB (collection://9e41c425-a33e-4ab1-a4e3-5d77f8dc4f16) FIRST
- Build lookup: normalize(store)|normalize(item) → min(Unit Price) last 30 days
- Flag 🏆 30d LOW if current unit_price ≤ 30d low
- Flag 🆕 First tracked if no prior history
- +0.15 score bonus for historical lows
- Set Stock-Up=true; populate 30d Low + Delta vs 30d Low in DB

## Proof Policy
For RCSS candidates: direct flyer item URL OR screenshot+page tuple.
For image-sourced deals: use flyer listing page URL as proof link.

## Ranking
```
base_score = 0.45*unit_price_rank + 0.25*freshness + 0.20*matchability + 0.10*practicality
final_score = base_score + (0.15 if is_historical_low else 0)
```

## Dedupe Key
`store + normalized_item + normalized_size + flyer_window`

Tie-break: proof completeness → clearer unit price → newer timestamp

## Chat Section Order
1. Run time + Pricing valid until
2. 🏆 HISTORICAL LOWS THIS WEEK callout (omit if none)
3. A) RCSS PRICE-MATCH READY
4. B) CHINESE STORES (Ranch Fresh · Centra · T&T — text + image combined)
5. C) COSTCO HIGHLIGHTS
6. Optional Preview watchlist

## Line Format
- `Store • Item • Price 🏆 30d LOW • ✅ Match | [Proof: url]`
- `Store • Item • Price 🆕 First tracked • ✅ Match | [Proof: url]`
- `Store • Item • Price • ✅ Match | [Proof: url]`
