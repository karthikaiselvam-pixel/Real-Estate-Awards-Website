#!/usr/bin/env python3
"""
Replace all image src attributes in 56 HTML files.

Classification by CSS class / parent context:
  hero          → Final-Photos/Hero/hero-NN.jpg        (18 available, round-robin)
  about-section → Final-Photos/About/about-NNN.jpg    (102 available, round-robin)
  thumbnail/card→ Final-Photos/Thumbnail/thumb-NNN.png (102 available, round-robin)

Hero img classes / contexts:
  .hero-slide img, .page-hero-img, .nomination-hero-slide img,
  .region-card img  (regional hero cards)

About img classes / contexts:
  .about-img-main, .testimonial-avatar (fallback),
  .gallery-item img (gallery = mix of hero+about → use about)

Thumbnail img classes / contexts:
  .category-card-img, .article-img, .sidebar-article-img,
  .about-img (badges / small about images)
"""

import os, re, glob

BASE = "/Users/karthikv/Real Estate Awards"

HERO_COUNT  = 18
ABOUT_COUNT = 102
THUMB_COUNT = 102

# Global round-robin counters (persist across files so pages get different images)
hero_ctr  = [0]
about_ctr = [0]
thumb_ctr = [0]

def next_hero():
    p = f"Final-Photos/Hero/hero-{(hero_ctr[0] % HERO_COUNT) + 1:02d}.jpg"
    hero_ctr[0] += 1
    return p

def next_about():
    p = f"Final-Photos/About/about-{(about_ctr[0] % ABOUT_COUNT) + 1:03d}.jpg"
    about_ctr[0] += 1
    return p

def next_thumb():
    p = f"Final-Photos/Thumbnail/thumb-{(thumb_ctr[0] % THUMB_COUNT) + 1:03d}.png"
    thumb_ctr[0] += 1
    return p


# ── Classification regexes (applied to the full img tag + up to 300 chars before it) ──

HERO_PATTERNS = [
    r'class="[^"]*hero-slide[^"]*"',
    r'class="page-hero-img"',
    r'class="[^"]*nomination-hero-slide[^"]*"',
    r'class="[^"]*region-card[^"]*"',        # region cards use hero images
]

ABOUT_PATTERNS = [
    r'class="about-img-main"',
    r'class="[^"]*testimonial-avatar[^"]*"',
    r'class="[^"]*gallery-item[^"]*"',        # gallery uses about images
]

THUMB_PATTERNS = [
    r'class="category-card-img"',
    r'class="[^"]*article-img[^"]*"',
    r'class="[^"]*sidebar-article-img[^"]*"',
]

def classify(context: str) -> str:
    """
    context = up to 400 chars before the img tag + the img tag itself.
    Returns 'hero', 'about', or 'thumb'.
    """
    for pat in HERO_PATTERNS:
        if re.search(pat, context, re.IGNORECASE):
            return 'hero'
    for pat in ABOUT_PATTERNS:
        if re.search(pat, context, re.IGNORECASE):
            return 'about'
    for pat in THUMB_PATTERNS:
        if re.search(pat, context, re.IGNORECASE):
            return 'thumb'
    # Fallback: look at parent context
    if re.search(r'class="[^"]*hero[^"]*"', context, re.IGNORECASE):
        return 'hero'
    if re.search(r'class="[^"]*gallery[^"]*"', context, re.IGNORECASE):
        return 'about'
    if re.search(r'class="[^"]*card[^"]*"', context, re.IGNORECASE):
        return 'thumb'
    # Default: about (general content images)
    return 'about'


def pick_image(img_type: str) -> str:
    if img_type == 'hero':
        return next_hero()
    elif img_type == 'thumb':
        return next_thumb()
    else:
        return next_about()


def process_file(fpath: str) -> int:
    fname = os.path.basename(fpath)
    with open(fpath, encoding='utf-8') as f:
        content = f.read()

    # Find every img tag that references 'photos/' and replace its src
    # We look back up to 500 chars for context
    replacements = 0

    def replacer(m):
        nonlocal replacements
        start = max(0, m.start() - 500)
        context = content[start: m.end()]
        img_type = classify(context)
        new_src = pick_image(img_type)
        replacements += 1
        return m.group(0).replace(m.group(1), new_src)

    # Match src="photos/..." inside an img tag
    new_content = re.sub(
        r'<img\b[^>]*\bsrc="(photos/[^"]+)"[^>]*>',
        replacer,
        content,
        flags=re.DOTALL
    )

    if new_content != content:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  {fname}: {replacements} image(s) replaced")
        return replacements
    else:
        print(f"  {fname}: no changes (no photos/ references found)")
        return 0


# ── Run across all HTML files ────────────────────────────────────────────────

html_files = sorted(glob.glob(os.path.join(BASE, "*.html")))
total_replaced = 0

for fpath in html_files:
    total_replaced += process_file(fpath)

print(f"\nTotal: {total_replaced} image references updated across {len(html_files)} files.")
print(f"Counters → hero:{hero_ctr[0]}  about:{about_ctr[0]}  thumb:{thumb_ctr[0]}")
