#!/usr/bin/env python3
"""
Bulk update all HTML files:
1. Replace external nomination links with internal award-nomination.html
2. Update contact details (address, phone, WhatsApp)
3. Add "Nominate Now" to footer Quick Links
4. Update hero/CTA button links
"""

import os
import re
import glob

BASE = os.path.dirname(os.path.abspath(__file__))
HTML_FILES = glob.glob(os.path.join(BASE, "*.html"))

REPLACEMENTS = [
    # ----------------------------------------------------------------
    # External nomination links → internal page (various patterns)
    # ----------------------------------------------------------------
    (
        'href="https://goldentreeawards.com/award-nomination" target="_blank" rel="noopener"',
        'href="award-nomination.html"',
    ),
    (
        "href='https://goldentreeawards.com/award-nomination' target='_blank' rel='noopener'",
        "href='award-nomination.html'",
    ),
    # Without rel=noopener
    (
        'href="https://goldentreeawards.com/award-nomination" target="_blank"',
        'href="award-nomination.html"',
    ),
    # Bare external link (no target)
    # Only replace when used as href alone (not in schema JSON)
    # We'll handle this via regex below, but add safe string match first
    # ----------------------------------------------------------------
    # WhatsApp float button — update phone
    # ----------------------------------------------------------------
    (
        'href="https://wa.me/971585856201"',
        'href="https://wa.me/971585862014"',
    ),
    (
        'href="https://wa.me/971585856201" target="_blank" rel="noopener"',
        'href="https://wa.me/971585862014" target="_blank" rel="noopener"',
    ),
    # ----------------------------------------------------------------
    # Footer address
    # ----------------------------------------------------------------
    (
        'The Binary by Omniyat, Office 1909-203, Business Bay, Dubai',
        'Iris Bay Tower, Business Bay, Dubai, UAE',
    ),
    (
        '📍 The Binary by Omniyat, Office 1909-203, Business Bay, Dubai',
        '📍 Iris Bay Tower, Business Bay, Dubai, UAE',
    ),
    # ----------------------------------------------------------------
    # Footer phone display
    # ----------------------------------------------------------------
    (
        '+971 58 585 6201',
        '+971 585862014',
    ),
    (
        'href="tel:+971585856201"',
        'href="tel:+971585862014"',
    ),
    (
        'href="tel:+971-585-8562014"',
        'href="tel:+971585862014"',
    ),
    # ----------------------------------------------------------------
    # WhatsApp contact links throughout pages
    # ----------------------------------------------------------------
    (
        'href="https://wa.me/971585856201"',
        'href="https://wa.me/971585862014"',
    ),
    (
        'wa.me/971585856201',
        'wa.me/971585862014',
    ),
]

# Regex replacement: bare href to external nomination without target="_blank"
# e.g. href="https://goldentreeawards.com/award-nomination" (followed by space or >)
REGEX_REPLACEMENTS = [
    (
        r'href="https://goldentreeawards\.com/award-nomination"(?!\s*target)',
        'href="award-nomination.html"',
    ),
]

# Footer Quick Links — add "Nominate Now" after the About link
# Pattern to find and add nomination link into the footer quick-links block
FOOTER_NOMINATE_INSERT = (
    '<a href="about.html">About</a>\n            <a href="award-categories.html">Categories</a>',
    '<a href="about.html">About</a>\n            <a href="award-nomination.html">Nominate Now</a>\n            <a href="award-categories.html">Categories</a>',
)
# Compact version (single-line or minimised footer)
FOOTER_NOMINATE_INSERT_COMPACT = (
    '<a href="about.html">About</a><a href="award-categories.html">Categories</a>',
    '<a href="about.html">About</a><a href="award-nomination.html">Nominate Now</a><a href="award-categories.html">Categories</a>',
)

updated_count = 0
for fpath in sorted(HTML_FILES):
    fname = os.path.basename(fpath)
    # Skip the nomination page itself (already correct)
    if fname == "award-nomination.html":
        continue

    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content

    # String replacements
    for old, new in REPLACEMENTS:
        content = content.replace(old, new)

    # Regex replacements
    for pattern, replacement in REGEX_REPLACEMENTS:
        content = re.sub(pattern, replacement, content)

    # Footer Quick Links — add "Nominate Now" if not already present
    if 'href="award-nomination.html">Nominate Now' not in content:
        old_f, new_f = FOOTER_NOMINATE_INSERT
        if old_f in content:
            content = content.replace(old_f, new_f)
        else:
            old_f, new_f = FOOTER_NOMINATE_INSERT_COMPACT
            if old_f in content:
                content = content.replace(old_f, new_f)

    if content != original:
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  Updated: {fname}")
        updated_count += 1
    else:
        print(f"  No change: {fname}")

print(f"\nDone. {updated_count}/{len(HTML_FILES)-1} files updated.")
