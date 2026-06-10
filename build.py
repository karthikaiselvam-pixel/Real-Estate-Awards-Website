#!/usr/bin/env python3
"""
World Real Estate Excellence Awards — Static Page Generator
Generates all 50+ pages with unique 1500-2000 word SEO-optimized content.
"""
import os
import json
import random
import re
from pathlib import Path

ROOT = Path(__file__).parent
PHOTOS_DIR = ROOT / "photos"
NOM_URL = "https://goldentreeawards.com/award-nomination"
SITE_URL = "https://goldentreeawards.com/world-real-estate-awards"

# Load + shuffle photo pool (deterministic for round-robin)
random.seed(2026)
ALL_PHOTOS = sorted([p.name for p in PHOTOS_DIR.glob("award*.webp")]) + \
             sorted([p.name for p in PHOTOS_DIR.glob("resized_webp*.webp")]) + \
             sorted([p.name for p in PHOTOS_DIR.glob("banner*.webp")]) + \
             sorted([p.name for p in PHOTOS_DIR.glob("speaking*.webp")])
random.shuffle(ALL_PHOTOS)

_photo_idx = 0
def take_photos(n, used=None):
    """Round-robin photo picker; avoids duplicates within `used` set."""
    global _photo_idx
    out = []
    seen = set(used) if used else set()
    tries = 0
    while len(out) < n and tries < len(ALL_PHOTOS) * 2:
        p = ALL_PHOTOS[_photo_idx % len(ALL_PHOTOS)]
        _photo_idx += 1
        tries += 1
        if p in seen:
            continue
        out.append(p)
        seen.add(p)
    return out

# ============================================================================
# Shared HTML fragments
# ============================================================================

HEADER_HTML = '''<header class="site-header">
  <div class="container header-inner">
    <a href="index.html" class="site-logo" aria-label="World Real Estate Excellence Awards">
      <span class="logo-icon">W</span>
      <span class="logo-text">
        <span class="line1">World Real Estate Excellence Awards</span>
        <span class="line2">Global Property Recognition · Since 2019</span>
      </span>
    </a>
    <nav class="primary-nav" aria-label="Primary">
      <div class="nav-item"><a class="nav-link" href="index.html">Home</a></div>
      <div class="nav-item"><a class="nav-link" href="about.html">About</a></div>
      <div class="nav-item">
        <a class="nav-link has-dropdown" href="award-categories.html">Categories</a>
        <div class="dropdown" role="menu">
          <a href="property-developer-awards.html">Developer Awards</a>
          <a href="architecture-awards.html">Architecture Awards</a>
          <a href="broker-awards.html">Broker Awards</a>
          <a href="interior-design-awards.html">Interior Design</a>
          <a href="luxury-real-estate-awards.html">Luxury Property</a>
          <a href="smart-building-awards.html">Smart Building</a>
          <a href="award-categories.html">All Categories</a>
        </div>
      </div>
      <div class="nav-item">
        <a class="nav-link has-dropdown" href="global-real-estate-awards.html">Regions</a>
        <div class="dropdown" role="menu">
          <a href="asia-real-estate-awards.html">Asia</a>
          <a href="europe-real-estate-awards.html">Europe</a>
          <a href="middle-east-property-awards.html">Middle East</a>
          <a href="north-america-real-estate-awards.html">North America</a>
          <a href="south-america-property-awards.html">South America</a>
          <a href="africa-real-estate-awards.html">Africa</a>
          <a href="oceania-real-estate-awards.html">Oceania</a>
          <a href="gcc-property-awards.html">GCC</a>
          <a href="luxury-property-awards-worldwide.html">Luxury Worldwide</a>
          <a href="global-real-estate-awards.html">Global</a>
        </div>
      </div>
      <div class="nav-item"><a class="nav-link" href="past-winners.html">Winners</a></div>
      <div class="nav-item"><a class="nav-link" href="award-judging-criteria.html">Judging</a></div>
      <div class="nav-item"><a class="nav-link" href="resources.html">Resources</a></div>
      <div class="nav-item"><a class="nav-link" href="blog.html">Blog</a></div>
      <div class="nav-item"><a class="nav-link" href="gallery.html">Gallery</a></div>
      <div class="nav-item"><a class="nav-link" href="faq.html">FAQ</a></div>
      <div class="nav-item"><a class="nav-link" href="contact.html">Contact</a></div>
      <a class="nav-cta" href="''' + NOM_URL + '''" target="_blank" rel="noopener">Nominate Now ›</a>
    </nav>
    <button class="menu-toggle" aria-label="Open menu"><span></span><span></span><span></span></button>
  </div>
  <nav class="mobile-nav" aria-label="Mobile">
    <div class="mobile-nav-links">
      <a href="index.html">Home</a>
      <a href="about.html">About Awards</a>
      <a href="award-categories.html">Award Categories</a>
      <div class="mobile-nav-section-title">Regions</div>
      <a href="asia-real-estate-awards.html">Asia</a>
      <a href="europe-real-estate-awards.html">Europe</a>
      <a href="middle-east-property-awards.html">Middle East</a>
      <a href="north-america-real-estate-awards.html">North America</a>
      <a href="south-america-property-awards.html">South America</a>
      <a href="africa-real-estate-awards.html">Africa</a>
      <a href="oceania-real-estate-awards.html">Oceania</a>
      <a href="gcc-property-awards.html">GCC</a>
      <a href="luxury-property-awards-worldwide.html">Luxury Worldwide</a>
      <a href="global-real-estate-awards.html">Global Awards</a>
      <div class="mobile-nav-section-title">Programme</div>
      <a href="past-winners.html">Past Winners</a>
      <a href="award-judging-criteria.html">Judging Process</a>
      <a href="resources.html">Resources</a>
      <a href="blog.html">Blog</a>
      <a href="gallery.html">Gallery</a>
      <a href="faq.html">FAQ</a>
      <a href="contact.html">Contact</a>
    </div>
    <a class="mobile-nav-cta" href="''' + NOM_URL + '''" target="_blank" rel="noopener">Nominate Now</a>
  </nav>
</header>'''

FOOTER_HTML = '''<footer class="site-footer">
  <div class="container">
    <div class="footer-top">
      <div class="footer-grid">
        <div class="footer-brand">
          <div class="footer-logo">
            <span class="logo-icon">W</span>
            <span class="logo-text">
              <span class="line1">World Real Estate Excellence Awards</span>
              <span class="line2">Global Property Recognition</span>
            </span>
          </div>
          <p class="footer-desc">An international, jury-led awards programme recognising the world's leading property developers, architects, brokers, agencies, interior designers and luxury real estate brands.</p>
          <p class="footer-contact-item">📍 The Binary by Omniyat, Office 1909-203, Business Bay, Dubai</p>
          <p class="footer-contact-item">✉ <a href="mailto:awards@goldentreeawards.com">awards@goldentreeawards.com</a></p>
          <p class="footer-contact-item">📞 <a href="tel:+971585856201">+971 58 585 6201</a></p>
        </div>
        <div class="footer-col">
          <h4>Quick Links</h4>
          <div class="footer-links">
            <a href="index.html">Home</a>
            <a href="about.html">About</a>
            <a href="award-categories.html">Categories</a>
            <a href="past-winners.html">Past Winners</a>
            <a href="award-judging-criteria.html">Judging</a>
            <a href="gallery.html">Gallery</a>
            <a href="blog.html">Blog</a>
            <a href="faq.html">FAQ</a>
            <a href="contact.html">Contact</a>
          </div>
        </div>
        <div class="footer-col">
          <h4>Regions</h4>
          <div class="footer-links">
            <a href="asia-real-estate-awards.html">Asia</a>
            <a href="europe-real-estate-awards.html">Europe</a>
            <a href="middle-east-property-awards.html">Middle East</a>
            <a href="north-america-real-estate-awards.html">North America</a>
            <a href="south-america-property-awards.html">South America</a>
            <a href="africa-real-estate-awards.html">Africa</a>
            <a href="oceania-real-estate-awards.html">Oceania</a>
            <a href="gcc-property-awards.html">GCC</a>
            <a href="global-real-estate-awards.html">Global</a>
          </div>
        </div>
        <div class="footer-col">
          <h4>Awards</h4>
          <div class="footer-links">
            <a href="property-developer-awards.html">Developer</a>
            <a href="luxury-real-estate-awards.html">Luxury Property</a>
            <a href="architecture-awards.html">Architecture</a>
            <a href="broker-awards.html">Broker</a>
            <a href="interior-design-awards.html">Interior Design</a>
            <a href="smart-building-awards.html">Smart Building</a>
            <a href="sustainable-design-awards.html">Sustainable</a>
            <a href="property-management-awards.html">Property Mgmt</a>
            <a href="real-estate-agency-awards.html">Agencies</a>
          </div>
        </div>
        <div class="footer-newsletter">
          <h4>Stay Updated</h4>
          <p>Get key dates, jury announcements and category opens delivered to your inbox.</p>
          <form class="newsletter-form" novalidate>
            <input type="email" class="newsletter-input" placeholder="Your email address" aria-label="Email" required />
            <button type="submit" class="newsletter-btn">Subscribe</button>
          </form>
          <div class="social-links">
            <a class="social-link" href="#" aria-label="LinkedIn">in</a>
            <a class="social-link" href="#" aria-label="Instagram">ig</a>
            <a class="social-link" href="#" aria-label="Facebook">f</a>
            <a class="social-link" href="#" aria-label="X">x</a>
            <a class="social-link" href="#" aria-label="YouTube">▶</a>
          </div>
        </div>
      </div>
    </div>
    <div class="footer-bottom">
      <p>© 2026 World Real Estate Excellence Awards. All rights reserved.</p>
      <div class="footer-legal">
        <a href="privacy-policy.html">Privacy Policy</a>
        <a href="terms-conditions.html">Terms &amp; Conditions</a>
        <a href="refund-policy.html">Refund Policy</a>
        <a href="sitemap.xml">Sitemap</a>
      </div>
    </div>
  </div>
</footer>
<a class="whatsapp-float" href="https://wa.me/971585856201" target="_blank" rel="noopener" aria-label="WhatsApp">💬</a>
<button class="back-to-top" aria-label="Back to top">↑</button>
<script src="js/main.js"></script>
</body>
</html>'''


def head_html(title, description, slug, keywords, hero_image):
    """Generate full SEO head."""
    canonical = f"{SITE_URL}/{slug}.html"
    og_image = f"photos/{hero_image}"
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta http-equiv="X-UA-Compatible" content="IE=edge" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{title}</title>
<meta name="description" content="{description}" />
<meta name="keywords" content="{', '.join(keywords)}" />
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />
<meta name="author" content="World Real Estate Excellence Awards" />
<meta name="theme-color" content="#0B163D" />
<link rel="canonical" href="{canonical}" />
<meta property="og:type" content="website" />
<meta property="og:site_name" content="World Real Estate Excellence Awards" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{description}" />
<meta property="og:url" content="{canonical}" />
<meta property="og:image" content="{og_image}" />
<meta property="og:locale" content="en_US" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{title}" />
<meta name="twitter:description" content="{description}" />
<meta name="twitter:image" content="{og_image}" />
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect width='100' height='100' rx='14' fill='%230B163D'/%3E%3Ctext x='50' y='66' font-family='Georgia,serif' font-size='52' font-weight='700' fill='%23C8A45D' text-anchor='middle'%3EW%3C/text%3E%3C/svg%3E" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link rel="stylesheet" href="css/main.css" />'''


def schema_org_block(title, description, slug, faqs, breadcrumbs):
    org = {
      "@context": "https://schema.org", "@type": "Organization",
      "name": "World Real Estate Excellence Awards",
      "url": SITE_URL + "/",
      "logo": SITE_URL + "/photos/award__(391).webp",
      "address": {"@type":"PostalAddress","streetAddress":"The Binary by Omniyat, Office 1909-203, Business Bay","addressLocality":"Dubai","addressCountry":"AE"},
      "contactPoint": {"@type":"ContactPoint","telephone":"+971-585-8562014","contactType":"customer service","email":"awards@goldentreeawards.com","areaServed":"Worldwide"}
    }
    article = {
      "@context": "https://schema.org", "@type": "Article",
      "headline": title,
      "description": description,
      "image": f"{SITE_URL}/photos/award__(391).webp",
      "author": {"@type": "Organization", "name": "World Real Estate Excellence Awards"},
      "publisher": {"@type":"Organization","name":"World Real Estate Excellence Awards","logo":{"@type":"ImageObject","url":f"{SITE_URL}/photos/award__(391).webp"}},
      "datePublished": "2026-01-15",
      "dateModified": "2026-05-24",
      "mainEntityOfPage": {"@type":"WebPage","@id":f"{SITE_URL}/{slug}.html"}
    }
    faq_schema = {
      "@context":"https://schema.org","@type":"FAQPage",
      "mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]
    }
    bc_schema = {
      "@context":"https://schema.org","@type":"BreadcrumbList",
      "itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":f"{SITE_URL}/{u}"} for i,(n,u) in enumerate(breadcrumbs)]
    }
    event_schema = {
      "@context":"https://schema.org","@type":"Event",
      "name": "World Real Estate Excellence Awards 2026",
      "description": description,
      "startDate":"2026-11-14T18:00",
      "endDate":"2026-11-14T23:00",
      "eventStatus":"https://schema.org/EventScheduled",
      "eventAttendanceMode":"https://schema.org/OfflineEventAttendanceMode",
      "location":{"@type":"Place","name":"Dubai","address":{"@type":"PostalAddress","addressLocality":"Dubai","addressCountry":"AE"}},
      "organizer":{"@type":"Organization","name":"World Real Estate Excellence Awards","url":SITE_URL+"/"},
      "offers":{"@type":"Offer","url":NOM_URL,"availability":"https://schema.org/InStock","validFrom":"2026-01-15"},
      "image":f"{SITE_URL}/photos/award__(391).webp"
    }
    blocks = []
    for s in (org, article, faq_schema, bc_schema, event_schema):
        blocks.append(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>')
    return "\n".join(blocks)


def breadcrumb_html(breadcrumbs):
    parts = []
    for i, (n, u) in enumerate(breadcrumbs):
        if i == len(breadcrumbs) - 1:
            parts.append(f'<span>{n}</span>')
        else:
            parts.append(f'<a href="{u}">{n}</a><span class="breadcrumb-sep">›</span>')
    return f'<div class="breadcrumb">{"".join(parts)}</div>'


def page_hero_html(eyebrow, h1, h1_accent, intro, hero_image, breadcrumbs, meta_items):
    bc = breadcrumb_html(breadcrumbs)
    meta = "".join(f'<span>{m}</span>' for m in meta_items)
    return f'''<section class="page-hero">
  <img class="page-hero-img" src="photos/{hero_image}" alt="{h1}" loading="eager" />
  <div class="container page-hero-content">
    {bc}
    <span class="hero-eyebrow">{eyebrow}</span>
    <h1>{h1} <span>{h1_accent}</span></h1>
    <p>{intro}</p>
    <div class="page-hero-meta">{meta}</div>
    <div style="margin-top:1.5rem;">
      <a class="btn btn-gold" href="{NOM_URL}" target="_blank" rel="noopener">Nominate Now ›</a>
      <a class="btn btn-outline-white" href="award-categories.html" style="margin-left:0.5rem;">Explore Categories</a>
    </div>
  </div>
</section>'''


def stats_strip(stats):
    items = ""
    for n, l in stats:
        items += f'<div class="stat-item"><span class="stat-num">{n}</span><span class="stat-label">{l}</span></div>'
    return f'<section class="stats-bar"><div class="container"><div class="stats-inner">{items}</div></div></section>'


def cta_banner(headline, sub, btn1=("Nominate Now", NOM_URL, True), btn2=None):
    b1 = f'<a class="btn btn-gold btn-lg" href="{btn1[1]}" target="_blank" rel="noopener">{btn1[0]} ›</a>' if btn1[2] else f'<a class="btn btn-gold btn-lg" href="{btn1[1]}">{btn1[0]} ›</a>'
    b2 = ""
    if btn2:
        b2 = f'<a class="btn btn-outline-white btn-lg" href="{btn2[1]}">{btn2[0]}</a>'
    return f'''<section class="cta-banner"><div class="container cta-banner-inner">
  <div><h2>{headline}</h2><p>{sub}</p></div>
  <div class="cta-banner-actions">{b1}{b2}</div>
</div></section>'''


def cta_gold(headline, sub, btn_text="Register For Awards", btn_url=NOM_URL):
    return f'''<section class="cta-gold-bar"><div class="container">
  <h2 class="h2">{headline}</h2>
  <p>{sub}</p>
  <a class="btn btn-navy btn-lg" href="{btn_url}" target="_blank" rel="noopener">{btn_text} ›</a>
</div></section>'''


def benefits_section(eyebrow, headline, sub, items):
    cards = "".join(f'<div class="benefit-card"><span class="benefit-icon">{i}</span><h3>{t}</h3><p>{d}</p></div>' for i,t,d in items)
    return f'''<section class="section benefits-section"><div class="container">
  <div class="section-header center">
    <span class="section-eyebrow">{eyebrow}</span>
    <h2 class="section-title h2 white">{headline}</h2>
    <p class="section-desc white">{sub}</p>
    <div class="section-divider"></div>
  </div>
  <div class="benefits-grid">{cards}</div>
</div></section>'''


def process_section():
    return '''<section class="process-section"><div class="container">
  <div class="section-header center" style="padding-top:3rem;">
    <span class="section-eyebrow">Judging Process</span>
    <h2 class="section-title h2 white">From Nomination To Recognition</h2>
    <p class="section-desc white">Transparent, independent and built on published criteria.</p>
    <div class="section-divider"></div>
  </div>
  <div class="process-steps">
    <div class="process-step"><div class="process-step-num">1</div><h3>Submit Nomination</h3><p>Complete the online entry form, upload project files and supporting evidence aligned with your chosen category.</p></div>
    <div class="process-step"><div class="process-step-num">2</div><h3>Eligibility Review</h3><p>Our awards secretariat verifies category fit and entry completeness before forwarding to the jury.</p></div>
    <div class="process-step"><div class="process-step-num">3</div><h3>Independent Scoring</h3><p>A senior independent jury scores entries against published criteria with weightings published in advance.</p></div>
    <div class="process-step"><div class="process-step-num">4</div><h3>Winners Announced</h3><p>Winners are revealed at the international gala and recognition assets issued for global use.</p></div>
  </div>
  <div class="text-center" style="padding:2.5rem 0 3.5rem;">
    <a class="btn btn-gold btn-lg" href="award-judging-criteria.html">View Detailed Criteria ›</a>
  </div>
</div></section>'''


def gallery_strip(images, alt_prefix):
    items = ""
    cls_seq = ["wide", "", "tall", "", "", "wide", "", ""]
    for i, p in enumerate(images[:8]):
        cls = cls_seq[i] if i < len(cls_seq) else ""
        items += f'<div class="gallery-item{" " + cls if cls else ""}"><img src="photos/{p}" alt="{alt_prefix} {i+1}" data-clickable loading="lazy" /></div>'
    return f'''<section class="section gallery-section"><div class="container">
  <div class="section-header center">
    <span class="section-eyebrow">Gallery</span>
    <h2 class="section-title h2">A Look Inside The Awards Programme</h2>
    <p class="section-desc">Photography from past editions of the World Real Estate Excellence Awards.</p>
    <div class="section-divider"></div>
  </div>
  <div class="gallery-grid">{items}</div>
</div></section>'''


def related_section(items):
    cards = ""
    for t, d, url in items:
        cards += f'<div class="related-card"><h4>{t}</h4><p>{d}</p><a href="{url}">Explore ›</a></div>'
    return f'''<section class="section related-section"><div class="container">
  <div class="section-header center">
    <span class="section-eyebrow">Related</span>
    <h2 class="section-title h2">Explore More Awards &amp; Regions</h2>
    <div class="section-divider"></div>
  </div>
  <div class="related-grid">{cards}</div>
</div></section>'''


def faq_section(faqs):
    half = (len(faqs) + 1) // 2
    col1 = faqs[:half]
    col2 = faqs[half:]
    def col(items):
        out = ""
        for q, a in items:
            out += f'<div class="faq-item"><button class="faq-question">{q} <span class="faq-icon">+</span></button><div class="faq-answer"><div class="faq-answer-inner">{a}</div></div></div>'
        return out
    return f'''<section class="section faq-section"><div class="container">
  <div class="section-header center">
    <span class="section-eyebrow">FAQ</span>
    <h2 class="section-title h2">Frequently Asked Questions</h2>
    <div class="section-divider"></div>
  </div>
  <div class="faq-grid">
    <div class="faq-col">{col(col1)}</div>
    <div class="faq-col">{col(col2)}</div>
  </div>
</div></section>'''


def content_section(body_html, sidebar_html=None):
    if sidebar_html is None:
        sidebar_html = ""
    return f'''<section class="section content-section"><div class="container">
  <div class="content-grid">
    <div class="content-body">{body_html}</div>
    <aside class="content-sidebar">{sidebar_html}</aside>
  </div>
</div></section>'''


def sidebar_widget_html(related_links, cta_headline="Recognise Your Excellence"):
    links = "".join(f'<a href="{u}">{n}</a>' for n, u in related_links)
    return f'''<div class="sidebar-widget">
  <h4>Related Pages</h4>
  <div class="sidebar-links">{links}</div>
</div>
<div class="sidebar-cta">
  <h4>{cta_headline}</h4>
  <p>Submit your nomination today and join the world's most credible real estate awards.</p>
  <a class="btn btn-gold" href="{NOM_URL}" target="_blank" rel="noopener">Nominate Now ›</a>
</div>'''


def winners_strip(images, items):
    cards = ""
    for i, (year, name, cat, project) in enumerate(items):
        img = images[i % len(images)]
        cards += f'''<div class="winner-card">
  <img class="winner-img" src="photos/{img}" alt="{name} {project}" data-clickable loading="lazy" />
  <div class="winner-body">
    <span class="winner-year">{year}</span>
    <h4>{name}</h4>
    <p>{project}</p>
    <span class="winner-category">{cat}</span>
  </div>
</div>'''
    return f'''<section class="section winners-section"><div class="container">
  <div class="section-header center">
    <span class="section-eyebrow">Past Winners</span>
    <h2 class="section-title h2">Recent Award Winners</h2>
    <p class="section-desc">A snapshot of recently honoured developers, architects and property brands.</p>
    <div class="section-divider"></div>
  </div>
  <div class="winners-grid">{cards}</div>
</div></section>'''


def award_list_html(items):
    out = '<div class="award-list">'
    for i, (t, d) in enumerate(items, 1):
        out += f'<div class="award-list-item"><div class="num">{i}</div><div><h4>{t}</h4><p>{d}</p></div></div>'
    out += "</div>"
    return out


def thumb_row(images, alts):
    """Render a thumbnail strip (4-up) for use inline."""
    cards = ""
    for img, alt in zip(images, alts):
        cards += f'<div class="winner-card"><img class="winner-img" src="photos/{img}" alt="{alt}" data-clickable loading="lazy" /></div>'
    return f'<div class="winners-grid" style="margin:1.5rem 0;">{cards}</div>'


def render_page(cfg):
    """Build a complete HTML page from cfg dict."""
    slug = cfg["slug"]
    title = cfg["title"]
    desc = cfg["description"]
    keywords = cfg["keywords"]
    used_imgs = set()
    hero_img = cfg.get("hero_image") or take_photos(1)[0]
    used_imgs.add(hero_img)
    gallery_imgs = take_photos(8, used_imgs); used_imgs.update(gallery_imgs)
    winner_imgs = take_photos(4, used_imgs); used_imgs.update(winner_imgs)
    inline_imgs = take_photos(4, used_imgs); used_imgs.update(inline_imgs)

    breadcrumbs = cfg.get("breadcrumbs", [("Home", "index.html"), (cfg["h1_main"] + " " + cfg.get("h1_accent",""), slug + ".html")])
    head = head_html(title, desc, slug, keywords, hero_img)
    schemas = schema_org_block(title, desc, slug, cfg["faqs"], breadcrumbs)

    hero = page_hero_html(
        cfg["eyebrow"],
        cfg["h1_main"],
        cfg.get("h1_accent", ""),
        cfg["intro"],
        hero_img,
        breadcrumbs,
        cfg.get("meta_items", ["★ Independent Jury", "✓ Global Recognition", "◈ 90+ Countries"])
    )

    stats = stats_strip(cfg.get("stats", [
        ("90+","Countries"), ("35+","Categories"), ("1,200+","Nominations"), ("450+","Winners"), ("7","Regions")
    ]))

    # Build the editorial content body (1500-2000 words)
    body_paras = []
    for h2, paras in cfg["sections"]:
        body_paras.append(f'<h2>{h2}</h2>')
        for p in paras:
            if isinstance(p, list):
                body_paras.append("<ul>" + "".join(f"<li>{li}</li>" for li in p) + "</ul>")
            elif p.startswith("AWARDS:"):
                # Embed award list
                items = json.loads(p[len("AWARDS:"):])
                body_paras.append(award_list_html(items))
            elif p.startswith("THUMBS:"):
                alts = json.loads(p[len("THUMBS:"):])
                body_paras.append(thumb_row(inline_imgs[:len(alts)], alts))
            else:
                body_paras.append(f'<p>{p}</p>')
    body_html = "\n".join(body_paras)

    # Sidebar
    sidebar = sidebar_widget_html(cfg.get("sidebar_links", []), cta_headline=cfg.get("sidebar_cta", "Submit Your Nomination"))

    benefits = benefits_section(
        cfg.get("benefits_eyebrow", "Why Participate"),
        cfg.get("benefits_headline", "Real, Measurable Benefits Of Award Recognition"),
        cfg.get("benefits_sub", "Beyond the trophy — winning unlocks tangible commercial advantages that move real estate brands forward."),
        cfg.get("benefits_items", [
            ("★", "Global Visibility", "Press releases, editorial features and a profile in the official winners directory reaching investors, partners and clients worldwide."),
            ("◈", "Brand Authority", "An independent, jury-verified seal of excellence that elevates positioning across marketing, sales, investor decks and digital presence."),
            ("◆", "Sales Acceleration", "Recognition has been shown to lift conversion rates and shorten sales cycles in luxury and premium real estate segments."),
            ("◉", "Investor Confidence", "Strengthen credibility with institutional investors, family offices and capital partners evaluating your projects."),
            ("⬢", "Networking", "Access curated networking with master developers, architects, agencies, lenders and proptech leaders at the international gala."),
            ("▲", "Talent Attraction", "Award-winning employers attract stronger architectural, design, sales and engineering talent in competitive markets.")
        ])
    )

    cta1 = cta_banner(
        cfg.get("cta1_headline", "Recognise Real Estate Excellence Worldwide"),
        cfg.get("cta1_sub", "Celebrate exceptional developers, architects and property brands. Join leading real estate companies on the global stage."),
        btn1=("Nominate Now", NOM_URL, True),
        btn2=("Browse Categories", "award-categories.html")
    )

    cta2 = cta_gold(
        cfg.get("cta2_headline", "Turn Property Excellence Into Global Recognition"),
        cfg.get("cta2_sub", "Join leading real estate brands worldwide.")
    )

    winners = winners_strip(winner_imgs, cfg.get("winners", [
        ("2025", "Luxury Master Developer", "Developer Of The Year", "Branded Residence Portfolio"),
        ("2025", "International Architecture Studio", "Architecture Excellence", "Mixed-Use Landmark"),
        ("2024", "Prime Real Estate Agency", "Agency Of The Year", "Luxury Sales Performance"),
        ("2024", "Smart Building Innovator", "Smart Building Award", "Connected Residential Tower"),
    ]))

    gallery = gallery_strip(gallery_imgs, cfg["h1_main"])
    faqs = faq_section(cfg["faqs"])
    related = related_section(cfg.get("related", []))
    process = process_section()

    final_cta = cta_banner(
        "Ready To Be Recognised On The Global Stage?",
        "Submit your nomination today and join the most credible real estate awards programme in the world.",
        btn1=("Submit Nomination", NOM_URL, True),
        btn2=("Contact The Team", "contact.html")
    )

    return f'''{head}
{schemas}
</head>
<body>
{HEADER_HTML}
{hero}
{stats}
<section class="section content-section"><div class="container">
  <div class="content-grid">
    <div class="content-body">{body_html}</div>
    <aside class="content-sidebar">{sidebar}</aside>
  </div>
</div></section>
{cta1}
{benefits}
{process}
{winners}
{gallery}
{cta2}
{faqs}
{related}
{final_cta}
{FOOTER_HTML}
'''
