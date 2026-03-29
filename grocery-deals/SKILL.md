#!/usr/bin/env python3
"""
normalize-item.py
Canonical normalization for grocery item names, units, and store names.
Used in Step 5 (history lows lookup key) and Step 9 (dedupe key).

Usage as CLI:
    python3 normalize-item.py --item "Boneless Skinless Chicken Breast" --unit "/lb"
    python3 normalize-item.py --dedupe-key --store "No Frills" --item "Chicken Breast" --unit "/lb" --date 2026-03-23

Usage as module:
    from normalize_item import normalize_item, normalize_unit, normalize_store, dedupe_key
"""

import argparse
import re
import sys
from datetime import date

# ── Unit synonyms → canonical form ───────────────────────────────────────────

UNIT_MAP = {
    # per-pound variants
    "per lb": "/lb", "per pound": "/lb", "/pound": "/lb",
    "lb": "/lb", "lbs": "/lb",
    # per-kg variants
    "per kg": "/kg", "per kilogram": "/kg", "/kilogram": "/kg",
    "kg": "/kg",
    # per-each variants
    "per ea": "/ea", "each": "/ea", "per each": "/ea",
    "/each": "/ea", "ea": "/ea",
    # per-package variants
    "per pkg": "/pkg", "per pack": "/pkg", "per package": "/pkg",
    "/pack": "/pkg", "/package": "/pkg", "pkg": "/pkg",
    # per-bag variants
    "per bag": "/bag", "/bag": "/bag",
    # per-100g
    "per 100g": "/100g", "/100g": "/100g", "100g": "/100g",
}

def normalize_unit(unit: str) -> str:
    """Return canonical unit string e.g. '/lb', '/kg', '/ea', '/pkg', '/bag', '/100g'."""
    if not unit:
        return "/ea"
    u = unit.strip().lower()
    if u in UNIT_MAP:
        return UNIT_MAP[u]
    # Already in canonical form
    if u in {"/lb", "/kg", "/ea", "/pkg", "/bag", "/100g"}:
        return u
    # Fallback: strip leading slash variants
    for canonical in ("/lb", "/kg", "/ea", "/pkg", "/bag"):
        if canonical.lstrip("/") in u:
            return canonical
    return u  # Return as-is if unrecognized


# ── Store name normalization ──────────────────────────────────────────────────

STORE_MAP = {
    "no frills":                    "no_frills",
    "nofrills":                     "no_frills",
    "food basics":                  "food_basics",
    "foodbasics":                   "food_basics",
    "real canadian superstore":     "rcss",
    "rcss":                         "rcss",
    "superstore":                   "rcss",
    "walmart":                      "walmart",
    "t&t":                          "tnt",
    "t&t supermarket":              "tnt",
    "tnt":                          "tnt",
    "ranch fresh":                  "ranch_fresh",
    "ranch fresh supermarket":      "ranch_fresh",
    "centra":                       "centra",
    "centra food market":           "centra",
    "costco":                       "costco",
    "metro":                        "metro",
    "freshco":                      "freshco",
    "fresh co":                     "freshco",
    "loblaws":                      "loblaws",
    "sobeys":                       "sobeys",
    "farm boy":                     "farm_boy",
    "longos":                       "longos",
    "longo's":                      "longos",
    "giant tiger":                  "giant_tiger",
    "shoppers drug mart":           "shoppers",
    "shoppers":                     "shoppers",
}

def normalize_store(store: str) -> str:
    """Return canonical snake_case store key."""
    if not store:
        return "unknown"
    s = store.strip().lower()
    return STORE_MAP.get(s, re.sub(r"\s+", "_", s))


# ── Item name normalization ───────────────────────────────────────────────────

# Brand/retailer prefixes to strip
BRAND_PREFIXES = [
    "compliments", "president's choice", "pc", "great value", "kirkland",
    "kirkland signature", "our finest", "no name", "selection",
    "life smart", "irresistibles", "sensations", "blue menu",
    "haagen-dazs", "tropicana", "dempster's", "gay lea", "lactantia",
]

# Descriptor words to strip (add to matching, reduce false misses)
STRIP_WORDS = [
    "boneless", "skinless", "bone-in", "bone in",
    "fresh", "frozen", "whole", "halved", "cut", "sliced", "diced",
    "extra", "extra-lean", "lean", "medium", "large", "jumbo", "small",
    "organic", "natural", "wild", "farm raised", "atlantic",
    "canadian", "ontario", "halal", "kosher",
    "value pack", "family pack", "bulk",
    "seedless", "ripe",
]

# Synonym map: normalize common name variants to one canonical form
SYNONYM_MAP = {
    # Chicken
    "chicken breast":        "chicken breast",
    "chicken breasts":       "chicken breast",
    "boneless chicken":      "chicken breast",
    "chicken thigh":         "chicken thigh",
    "chicken thighs":        "chicken thigh",
    "chicken drumstick":     "chicken drumstick",
    "chicken drumsticks":    "chicken drumstick",
    "chicken leg":           "chicken leg",
    "chicken legs":          "chicken leg",
    "chicken wing":          "chicken wing",
    "chicken wings":         "chicken wing",
    "whole chicken":         "whole chicken",
    "chicken":               "chicken",
    # Pork
    "pork loin":             "pork loin",
    "pork shoulder":         "pork shoulder",
    "pork belly":            "pork belly",
    "pork chop":             "pork chop",
    "pork chops":            "pork chop",
    "pork ribs":             "pork rib",
    "pork rib":              "pork rib",
    # Beef
    "ground beef":           "ground beef",
    "beef steak":            "beef steak",
    "striploin":             "beef striploin",
    "ribeye":                "beef ribeye",
    "rib eye":               "beef ribeye",
    # Salmon / seafood
    "atlantic salmon":       "salmon",
    "salmon fillet":         "salmon",
    "salmon fillets":        "salmon",
    "sockeye salmon":        "salmon",
    "coho salmon":           "salmon",
    "shrimp":                "shrimp",
    "prawns":                "shrimp",
    "tiger shrimp":          "shrimp",
    # Eggs
    "large eggs":            "eggs large",
    "extra-large eggs":      "eggs xl",
    "xl eggs":               "eggs xl",
    "medium eggs":           "eggs medium",
    "free run eggs":         "eggs free run",
    "free range eggs":       "eggs free range",
    # Produce — plurals and variants
    "potatoes":              "potato",
    "sweet potatoes":        "sweet potato",
    "yams":                  "yam",
    "onions":                "onion",
    "mushrooms":             "mushroom",
    "oranges":               "orange",
    "apples":                "apple",
    "pears":                 "pear",
    "mangoes":               "mango",
    "mangos":                "mango",
    "grapes":                "grape",
    "strawberries":          "strawberry",
    "blackberries":          "blackberry",
    "avocados":              "avocado",
    "cucumbers":             "cucumber",
    "eggplants":             "eggplant",
    "bok choy":              "bok choy",
    "bok choy sprout":       "bok choy",
    "yu choy":               "yu choy",
    "bean sprouts":          "bean sprout",
    "green onions":          "green onion",
    "scallions":             "green onion",
    "cauliflowers":          "cauliflower",
    "broccoli crowns":       "broccoli",
    "flat cabbage":          "napa cabbage",
    "napa cabbage":          "napa cabbage",
    "kale":                  "kale",
    "beets":                 "beet",
    "lotus root":            "lotus root",
    "ginger root":           "ginger",
    "ginger":                "ginger",
    # Rice
    "jasmine rice":          "jasmine rice",
    "long grain rice":       "long grain rice",
    "short grain rice":      "short grain rice",
    "sushi rice":            "sushi rice",
    "brown rice":            "brown rice",
    "basmati rice":          "basmati rice",
}


def normalize_item(item: str) -> str:
    """
    Return a canonical lowercase item name suitable for history lookup and dedupe keys.
    Steps: lowercase → strip brand → strip descriptors → synonym map → collapse whitespace.
    """
    if not item:
        return "unknown"

    s = item.strip().lower()

    # 1. Strip brand prefixes
    for brand in sorted(BRAND_PREFIXES, key=len, reverse=True):
        if s.startswith(brand):
            s = s[len(brand):].strip().lstrip("-").strip()

    # 2. Strip leading/trailing descriptor words
    for word in sorted(STRIP_WORDS, key=len, reverse=True):
        # Strip from front
        if s.startswith(word + " "):
            s = s[len(word):].strip()
        # Strip from end
        if s.endswith(" " + word):
            s = s[: -len(word)].strip()

    # 3. Synonym map — full string match first
    if s in SYNONYM_MAP:
        return SYNONYM_MAP[s]

    # 4. Partial synonym match (contains key)
    for key, canonical in sorted(SYNONYM_MAP.items(), key=lambda x: len(x[0]), reverse=True):
        if key in s:
            return canonical

    # 5. Collapse whitespace and return
    return re.sub(r"\s+", " ", s).strip()


# ── Dedupe key ────────────────────────────────────────────────────────────────

def dedupe_key(store: str, item: str, unit: str, run_date: str | None = None) -> str:
    """
    Build canonical dedupe key: Store|normalized_item|unit_basis|YYYY-MM-DD
    Matches format expected by Step 9 of SKILL.md.
    run_date defaults to today if not provided.
    """
    d = run_date or date.today().isoformat()
    return f"{normalize_store(store)}|{normalize_item(item)}|{normalize_unit(unit)}|{d}"


# ── History lookup key (Step 5) ───────────────────────────────────────────────

def history_key(store: str, item: str) -> str:
    """
    Build lookup key for 30-day history table: normalize(store)|normalize(item)
    No unit or date — intentionally broad for cross-period matching.
    """
    return f"{normalize_store(store)}|{normalize_item(item)}"


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Normalize grocery item names, units, and store names.")
    parser.add_argument("--item",       help="Item name to normalize")
    parser.add_argument("--unit",       help="Unit string to normalize")
    parser.add_argument("--store",      help="Store name to normalize")
    parser.add_argument("--date",       help="Date YYYY-MM-DD (default: today)")
    parser.add_argument("--dedupe-key", action="store_true",
                        help="Output dedupe key (requires --store, --item, --unit)")
    parser.add_argument("--history-key", action="store_true",
                        help="Output history lookup key (requires --store, --item)")
    args = parser.parse_args()

    if args.dedupe_key:
        if not all([args.store, args.item, args.unit]):
            print("ERROR: --dedupe-key requires --store, --item, and --unit", file=sys.stderr)
            sys.exit(1)
        print(dedupe_key(args.store, args.item, args.unit, args.date))

    elif args.history_key:
        if not all([args.store, args.item]):
            print("ERROR: --history-key requires --store and --item", file=sys.stderr)
            sys.exit(1)
        print(history_key(args.store, args.item))

    else:
        if args.item:
            print(f"item:  {normalize_item(args.item)}")
        if args.unit:
            print(f"unit:  {normalize_unit(args.unit)}")
        if args.store:
            print(f"store: {normalize_store(args.store)}")


if __name__ == "__main__":
    main()
