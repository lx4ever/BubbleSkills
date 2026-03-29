#!/usr/bin/env python3
"""
discover-flyer-images.py
Fetches flyer listing pages for image-based stores and returns ordered image URLs.

Usage:
    python3 discover-flyer-images.py --store "Ranch Fresh"
    python3 discover-flyer-images.py --store all
    python3 discover-flyer-images.py --store "Metro" --json

Outputs to stdout. Use --json for machine-readable output.
"""

import argparse
import json
import re
import sys
import urllib.request
import urllib.error
from urllib.parse import urljoin, urlparse

# ── Store definitions ──────────────────────────────────────────────────────────

STORES = {
    "Ranch Fresh": {
        "listing_urls": [
            "https://flyers.smartcanucks.ca/ranch-fresh-supermarket-canada",
            "https://www.ranchfresh.ca/index1.html",
        ],
        "image_patterns": [
            r"uploads/pages/\d+/[^\"']+\.jpe?g",   # SmartCanucks pattern
            r"static/image/flyer[^\"']+\.jpe?g",    # ranchfresh.ca pattern
        ],
        "find_flyer_link": True,   # Must follow a sub-link to reach page images
        "flyer_link_pattern": r'href="(/canada/ranch-fresh-supermarket-flyer[^"]+)"',
        "flyer_link_base": "https://flyers.smartcanucks.ca",
    },
    "Centra": {
        "listing_urls": [
            "https://www.flyers-on-line.com/centra-food-market/aurora",
            "https://centrafoods.ca/pages/weekly-deals",
        ],
        "image_patterns": [
            r"https?://[^\"'\s]+(?:flyer|page|weekly|upload)[^\"'\s]+\.(?:jpe?g|png|webp)",
            r'src="([^"]+\.(?:jpe?g|png|webp))"',
        ],
        "find_flyer_link": False,
    },
    "Metro": {
        "listing_urls": [
            "https://www.flyerseek.com/metro-weekly-flyer",
        ],
        "image_patterns": [
            r"https?://[^\"'\s]+(?:flyer|page|weekly|upload)[^\"'\s]+\.(?:jpe?g|png|webp)",
        ],
        "find_flyer_link": False,
    },
    "FreshCo": {
        "listing_urls": [
            "https://www.flyerseek.com/freshco-weekly-flyer-on",
        ],
        "image_patterns": [
            r"https?://[^\"'\s]+(?:flyer|page|weekly|upload)[^\"'\s]+\.(?:jpe?g|png|webp)",
        ],
        "find_flyer_link": False,
    },
}

# ── URL filter rules (from store-registry.md) ─────────────────────────────────

INCLUDE_KEYWORDS = ["flyer", "page", "weekly", "upload", "static/image"]
INCLUDE_EXTS     = (".jpg", ".jpeg", ".png", ".webp")
EXCLUDE_KEYWORDS = ["logo", "thumb", "icon", "avatar", "banner", "placeholder"]


def passes_filter(url: str) -> bool:
    u = url.lower()
    if not any(u.endswith(ext) for ext in INCLUDE_EXTS):
        return False
    if any(kw in u for kw in EXCLUDE_KEYWORDS):
        return False
    if any(kw in u for kw in INCLUDE_KEYWORDS):
        return True
    return False


# ── HTTP helpers ──────────────────────────────────────────────────────────────

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
}


def fetch(url: str, timeout: int = 15) -> str | None:
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        print(f"  [WARN] HTTP {e.code} fetching {url}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"  [WARN] Error fetching {url}: {e}", file=sys.stderr)
        return None


# ── Page number extractor (for ordering) ─────────────────────────────────────

def page_num(url: str) -> int:
    """Extract trailing page number from URL for ordering, e.g. -3.jpg → 3."""
    m = re.search(r"-(\d+)\.(?:jpe?g|png|webp)$", url.lower())
    return int(m.group(1)) if m else 999


# ── Core discovery logic ──────────────────────────────────────────────────────

def discover(store_name: str) -> dict:
    cfg = STORES.get(store_name)
    if not cfg:
        return {"store": store_name, "status": "unknown_store", "images": [], "flyer_page": None}

    result = {
        "store": store_name,
        "status": "not_found",
        "images": [],
        "flyer_page": None,
        "source_url": None,
    }

    for listing_url in cfg["listing_urls"]:
        print(f"  Fetching listing: {listing_url}", file=sys.stderr)
        html = fetch(listing_url)
        if not html:
            continue

        target_html = html
        target_base = listing_url

        # Step 1: If this store needs a flyer sub-link, follow it first
        if cfg.get("find_flyer_link"):
            pattern = cfg.get("flyer_link_pattern", "")
            base    = cfg.get("flyer_link_base", "")
            m = re.search(pattern, html)
            if m:
                flyer_path = m.group(1)
                flyer_url  = base + flyer_path if flyer_path.startswith("/") else flyer_path
                print(f"  Following flyer link: {flyer_url}", file=sys.stderr)
                sub_html = fetch(flyer_url)
                if sub_html:
                    target_html = sub_html
                    target_base = flyer_url
                    result["flyer_page"] = flyer_url
            else:
                print(f"  [WARN] No flyer link found in listing page", file=sys.stderr)

        # Step 2: Extract image URLs using patterns
        found = set()
        for pattern in cfg["image_patterns"]:
            for m in re.finditer(pattern, target_html, re.IGNORECASE):
                raw = m.group(0) if m.lastindex is None else m.group(1)
                # Make absolute
                if raw.startswith("//"):
                    raw = "https:" + raw
                elif raw.startswith("/"):
                    parsed = urlparse(target_base)
                    raw = f"{parsed.scheme}://{parsed.netloc}{raw}"
                elif not raw.startswith("http"):
                    raw = urljoin(target_base, raw)
                if passes_filter(raw):
                    found.add(raw)

        # Step 3: Also scan all img src tags as a catch-all
        for m in re.finditer(r'<img[^>]+src=["\']([^"\']+)["\']', target_html, re.IGNORECASE):
            raw = m.group(1)
            if raw.startswith("//"):
                raw = "https:" + raw
            elif raw.startswith("/"):
                parsed = urlparse(target_base)
                raw = f"{parsed.scheme}://{parsed.netloc}{raw}"
            elif not raw.startswith("http"):
                raw = urljoin(target_base, raw)
            if passes_filter(raw):
                found.add(raw)

        if found:
            ordered = sorted(found, key=page_num)
            result["images"]     = ordered
            result["source_url"] = listing_url
            result["status"]     = "ok"
            print(f"  ✅ Found {len(ordered)} image(s) for {store_name}", file=sys.stderr)
            break  # First successful source wins; no need to try fallback
        else:
            print(f"  [WARN] No images found at {listing_url}", file=sys.stderr)

    if result["status"] != "ok":
        result["status"] = "failed"
        print(f"  ❌ All sources failed for {store_name}", file=sys.stderr)

    return result


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Discover flyer image URLs for image-based stores.")
    parser.add_argument("--store", default="all",
                        help='Store name e.g. "Ranch Fresh", "Centra", "Metro", "FreshCo", or "all"')
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="Output full JSON (default: plain URL list)")
    args = parser.parse_args()

    targets = list(STORES.keys()) if args.store.lower() == "all" else [args.store]

    results = []
    for store in targets:
        print(f"\n→ Discovering: {store}", file=sys.stderr)
        results.append(discover(store))

    if args.as_json:
        print(json.dumps(results, indent=2))
    else:
        # Plain output: one URL per line, prefixed with store name
        for r in results:
            if r["status"] == "ok":
                for url in r["images"]:
                    print(f"{r['store']}\t{url}")
            else:
                print(f"# {r['store']}: {r['status']}", file=sys.stderr)


if __name__ == "__main__":
    main()
