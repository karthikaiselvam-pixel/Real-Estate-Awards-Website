#!/usr/bin/env python3
"""
Build all pages for the World Real Estate Excellence Awards website.
Run: python3 build_all.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

from build import render_page, NOM_URL, SITE_URL, ALL_PHOTOS, take_photos  # noqa
import build as B
from content_regions import REGIONS
from content_keywords import KEYWORDS as K1
from content_keywords_2 import KEYWORDS_2 as K2
from content_keywords_3 import KEYWORDS_3 as K3
from content_keywords_4 import KEYWORDS_4 as K4
from content_keywords_5 import KEYWORDS_5 as K5

ALL_CONFIGS = REGIONS + K1 + K2 + K3 + K4 + K5

print(f"Total pages to render: {len(ALL_CONFIGS)}")

# Reset photo index for deterministic ordering
B._photo_idx = 0

written = []
for cfg in ALL_CONFIGS:
    slug = cfg["slug"]
    out_path = ROOT / f"{slug}.html"
    html = render_page(cfg)
    out_path.write_text(html, encoding="utf-8")
    written.append(slug)
    print(f"  wrote {slug}.html ({len(html):,} chars)")

print(f"\n✓ Rendered {len(written)} pages")

# ============================================================
# Generate sitemap.xml
# ============================================================
all_slugs = ["index"] + [c["slug"] for c in ALL_CONFIGS] + [
    "about", "contact", "faq", "past-winners", "gallery", "blog", "resources",
    "privacy-policy", "terms-conditions", "refund-policy"
]
sitemap_urls = ""
for slug in all_slugs:
    path = "" if slug == "index" else f"{slug}.html"
    sitemap_urls += f'''  <url>
    <loc>{SITE_URL}/{path}</loc>
    <changefreq>weekly</changefreq>
    <priority>{"1.0" if slug == "index" else "0.8" if "real-estate-awards" in slug or "property-awards" in slug else "0.7"}</priority>
  </url>
'''
sitemap = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{sitemap_urls}</urlset>
'''
(ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8")
print(f"✓ Wrote sitemap.xml ({len(all_slugs)} URLs)")

# ============================================================
# Generate robots.txt
# ============================================================
robots = f'''User-agent: *
Allow: /
Disallow: /build.py
Disallow: /build_all.py
Disallow: /content_*.py

Sitemap: {SITE_URL}/sitemap.xml
'''
(ROOT / "robots.txt").write_text(robots, encoding="utf-8")
print("✓ Wrote robots.txt")

print(f"\n✓ All done. {len(all_slugs)} total pages in sitemap.")
