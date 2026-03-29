# Flyer Store Registry

Load this file at the start of any scraping step to resolve store URLs, source types, and fallback URLs.

## Postal Code / Region
- `L4G 0H2` — Aurora, Ontario

## Store Groups

| Group | Stores |
|-------|--------|
| `rcss_group` | Giant Tiger, Food Basics, FreshCo, Walmart, Longo's, No Frills, Metro, Sobeys, Farm Boy, Loblaws, Shoppers Drug Mart, T&T |
| `chinese_group` | Ranch Fresh, Centra, T&T |
| `costco_group` | Costco |

## Flyer Sources

| Store | Primary URL | Source Type | Fallback URL |
|-------|------------|-------------|--------------|
| No Frills | flyerseek.com/no-frills-weekly-flyer-on | text | — |
| Food Basics | flyerseek.com/food-basics-flyer | text | — |
| Walmart | flyerseek.com/walmart-flyer | text | — |
| T&T Supermarket | flyers-on-line.com/t-t-supermarket/ontario | text | — |
| Metro | flyerseek.com/metro-weekly-flyer | image-only | SmartCanucks |
| FreshCo | flyerseek.com/freshco-weekly-flyer-on | image-only | SmartCanucks |
| Ranch Fresh | flyers.smartcanucks.ca/ranch-fresh-supermarket-canada | image | ranchfresh.ca/index1.html |
| Centra Food Market | flyers-on-line.com/centra-food-market/aurora | image | centrafoods.ca/pages/weekly-deals |
| Costco | cocoeast.ca | text | — |

## Image URL Extraction Patterns

**Ranch Fresh** — fetch `https://flyers.smartcanucks.ca/ranch-fresh-supermarket-canada`
- Find current week's flyer link (most recent, non-expired)
- Fetch that flyer page (e.g. `/canada/ranch-fresh-supermarket-flyer-march-13-to-191`)
- Extract `.jpg` URLs from `<img>` tags
- Pattern: `https://flyers.smartcanucks.ca/uploads/pages/[ID]/[name]-[N].jpg`
- Fallback: `https://www.ranchfresh.ca/index1.html` → `static/image/flyer*.jpeg`

**Centra Food Market Aurora** — fetch `https://www.flyers-on-line.com/centra-food-market/aurora`
- Extract image URLs from page
- Fallback: `https://centrafoods.ca/pages/weekly-deals`

**Metro / FreshCo** — fetch respective flyerseek.com pages
- Extract `.webp` or `.jpg` flyer page image URLs

## Image URL Filter (apply to all image stores)
```
include if: any(['flyer','page','weekly','upload','static/image'] in url)
           AND url ends with (.jpg, .jpeg, .png, .webp)
           AND 'logo' not in url
           AND 'thumb' not in url
make relative URLs absolute using base domain
```
