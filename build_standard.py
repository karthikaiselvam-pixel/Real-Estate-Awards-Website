#!/usr/bin/env python3
"""Build the standard site pages (about, contact, faq, past-winners, gallery, blog, resources, legal)."""
import sys
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

import build as B
from build import HEADER_HTML, FOOTER_HTML, NOM_URL, SITE_URL, take_photos
import json

# Reset photo index for these pages so we get fresh visuals
B._photo_idx = 0


def _head(title, desc, slug, keywords=""):
    canonical = f"{SITE_URL}/{slug}.html"
    img = "photos/award__(391).webp"
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{title}</title>
<meta name="description" content="{desc}" />
<meta name="keywords" content="{keywords}" />
<meta name="robots" content="index, follow, max-image-preview:large" />
<meta name="theme-color" content="#0B163D" />
<link rel="canonical" href="{canonical}" />
<meta property="og:type" content="website" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{desc}" />
<meta property="og:url" content="{canonical}" />
<meta property="og:image" content="{img}" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{title}" />
<meta name="twitter:description" content="{desc}" />
<meta name="twitter:image" content="{img}" />
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect width='100' height='100' rx='14' fill='%230B163D'/%3E%3Ctext x='50' y='66' font-family='Georgia,serif' font-size='52' font-weight='700' fill='%23C8A45D' text-anchor='middle'%3EW%3C/text%3E%3C/svg%3E" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link rel="stylesheet" href="css/main.css" /></head><body>'''


def _wrap(body, head_block):
    return head_block + HEADER_HTML + body + FOOTER_HTML


def _page_hero(eyebrow, h1, h1_accent, intro, hero_img, breadcrumbs):
    bc = ""
    for i, (n, u) in enumerate(breadcrumbs):
        if i == len(breadcrumbs) - 1:
            bc += f'<span>{n}</span>'
        else:
            bc += f'<a href="{u}">{n}</a><span class="breadcrumb-sep">›</span>'
    return f'''<section class="page-hero">
  <img class="page-hero-img" src="photos/{hero_img}" alt="{h1}" loading="eager" />
  <div class="container page-hero-content">
    <div class="breadcrumb">{bc}</div>
    <span class="hero-eyebrow">{eyebrow}</span>
    <h1>{h1} <span>{h1_accent}</span></h1>
    <p>{intro}</p>
  </div>
</section>'''


def _cta_banner():
    return f'''<section class="cta-banner"><div class="container cta-banner-inner">
  <div><h2>Recognise Real Estate Excellence Worldwide</h2><p>Celebrate exceptional developers, architects and property brands. Join leading real estate companies on the global stage.</p></div>
  <div class="cta-banner-actions">
    <a class="btn btn-gold btn-lg" href="{NOM_URL}" target="_blank" rel="noopener">Nominate Now ›</a>
    <a class="btn btn-outline-white btn-lg" href="award-categories.html">Browse Categories</a>
  </div>
</div></section>'''


# ============================================================
# ABOUT
# ============================================================
def about_page():
    hero_img, *gallery = take_photos(9)
    head = _head(
        "About The Awards | World Real Estate Excellence Awards",
        "Learn about the World Real Estate Excellence Awards — an international, jury-led recognition programme honouring outstanding developers, architects, brokers and luxury property brands across 90+ countries.",
        "about",
        "about world real estate awards, property awards programme, real estate awards organisation"
    )
    body = _page_hero(
        "About The Programme",
        "About The World Real Estate",
        "Excellence Awards",
        "An international, jury-led recognition programme honouring outstanding property developers, architects, brokers, agencies, interior designers and luxury real estate brands across 90+ countries.",
        hero_img,
        [("Home","index.html"),("About","about.html")]
    )
    body += f'''<section class="section content-section"><div class="container">
  <div class="content-grid">
    <div class="content-body">
      <h2>Our Story</h2>
      <p>The <strong>World Real Estate Excellence Awards</strong> was founded to give the global real estate industry a credible, independent recognition platform — one built on transparent criteria, an independent jury, and a footprint that genuinely reaches the developers, architects, brokers and luxury property brands shaping the built environment.</p>
      <p>Since launch, the programme has honoured more than 450 organisations and projects across 90+ countries, spanning Asia, Europe, the Middle East, North America, South America, Africa and Oceania. The Awards has become the most internationally trusted real estate recognition programme — followed by institutional investors, family offices, lenders, occupiers and HNW buyers worldwide.</p>

      <h2>Mission</h2>
      <p>To identify, recognise and globally amplify the most exceptional work in international real estate — across every layer of the value chain, in every major region of the world, judged independently against published criteria. The mission is built on three principles: <strong>credibility</strong> (independent jury, transparent criteria, declared conflicts), <strong>reach</strong> (90+ countries, seven regions, 35+ categories) and <strong>commercial value</strong> (recognition that materially supports the winning organisation's commercial outcomes).</p>

      <h2>What Makes The Programme Different</h2>
      <ul>
        <li>Independent jury of senior global property developers, architects, fund executives and academic experts</li>
        <li>Published scoring criteria, weightings and methodology for every category</li>
        <li>Regional context — category set tuned to each region's specific market dynamics</li>
        <li>Comprehensive — 35+ categories spanning developer, architecture, broker, agency, design, smart, sustainable and luxury recognition</li>
        <li>Commercially focused — recognition is designed to deliver measurable commercial impact for winners</li>
        <li>Permanent — the digital and print seal is for permanent use across marketing, sales, PR and investor materials</li>
      </ul>

      <h2>The Jury</h2>
      <p>The independent jury is composed of senior global property developers, master architects, real estate fund executives, urban planners, luxury market analysts, sustainability specialists and academic experts. Jurors are appointed by the jury chair, declare conflicts of interest and recuse themselves from any entry where independence cannot be guaranteed. The jury chair publishes a yearly methodology note alongside each shortlist announcement.</p>
      <p>The jury approach combines regional depth — each region has a dedicated regional jury with category-specific specialists — with global oversight. This ensures projects are judged both in their specific market context and against international peer work, producing recognition that resonates at every commercial level.</p>

      <h2>Programme Structure</h2>
      <p>The programme runs across seven regions: Asia, Europe, the Middle East, North America, South America, Africa and Oceania. Each region has dedicated categories alongside pan-regional and global recognition. Entrants can compete at country level, regional level, continental level and global level, with separate jury scoring at each stage.</p>
      <p>The 2026 calendar runs in three windows. The early-bird window closes in early Q2 (discounted fees); the standard window closes mid-Q3 (standard fees); the late-entry window closes Q4 (premium fees). Shortlists are announced four to six weeks before the gala in November.</p>

      <h2>The Gala</h2>
      <p>The international gala is held annually in Dubai in November, bringing together the world's leading developers, architects, brokers, agencies, investors and property brands for the most credible recognition night in global real estate. Past gala attendees include senior representatives from major master developers, listed real estate platforms, leading architectural practices and the international press community.</p>
      <p>Winners are announced live at the gala, with recognition assets — trophy, digital seal, print seal, editorial profile, winners directory listing — issued shortly afterwards. The gala is followed by the publication of the winners directory, press programme and alumni network communications.</p>

      <h2>Recognition Assets</h2>
      <p>Winners receive a comprehensive recognition package. The package includes a globally recognised physical trophy presented at the gala, a digital and print winner's seal with detailed usage guidelines, an editorial profile published in the official winners directory, a press release distributed to international real estate media, and invitations to ongoing industry networking events. Winners also gain access to the World Real Estate Excellence Awards alumni network.</p>

      <h2>Get Involved</h2>
      <p>Submit your nomination via the official entry portal. The form takes 20–30 minutes per category and accepts written submissions, project images, drawings, videos and supporting evidence. The awards team can be contacted directly for entry consultation at awards@goldentreeawards.com.</p>
      <p>For partnership conversations — sponsorship, media partnership, jury participation — please contact the awards team. For press enquiries, the international press programme can be accessed through the resources section.</p>
    </div>
    <aside class="content-sidebar">
      <div class="sidebar-widget">
        <h4>Programme Quick Links</h4>
        <div class="sidebar-links">
          <a href="award-categories.html">Award Categories</a>
          <a href="award-judging-criteria.html">Judging Criteria</a>
          <a href="award-submission-guide.html">Submission Guide</a>
          <a href="award-benefits.html">Award Benefits</a>
          <a href="past-winners.html">Past Winners</a>
          <a href="resources.html">Resources</a>
          <a href="contact.html">Contact The Team</a>
        </div>
      </div>
      <div class="sidebar-cta">
        <h4>Submit Your Nomination</h4>
        <p>Begin a nomination via the official entry portal.</p>
        <a class="btn btn-gold" href="{NOM_URL}" target="_blank" rel="noopener">Nominate Now ›</a>
      </div>
    </aside>
  </div>
</div></section>
{_cta_banner()}
<section class="section gallery-section"><div class="container">
  <div class="section-header center">
    <span class="section-eyebrow">Inside The Programme</span>
    <h2 class="section-title h2">Photography From Past Editions</h2>
    <div class="section-divider"></div>
  </div>
  <div class="gallery-grid">
    <div class="gallery-item wide"><img src="photos/{gallery[0]}" alt="World Real Estate Awards gala 1" data-clickable loading="lazy" /></div>
    <div class="gallery-item"><img src="photos/{gallery[1]}" alt="World Real Estate Awards gala 2" data-clickable loading="lazy" /></div>
    <div class="gallery-item tall"><img src="photos/{gallery[2]}" alt="World Real Estate Awards gala 3" data-clickable loading="lazy" /></div>
    <div class="gallery-item"><img src="photos/{gallery[3]}" alt="World Real Estate Awards gala 4" data-clickable loading="lazy" /></div>
    <div class="gallery-item"><img src="photos/{gallery[4]}" alt="World Real Estate Awards gala 5" data-clickable loading="lazy" /></div>
    <div class="gallery-item wide"><img src="photos/{gallery[5]}" alt="World Real Estate Awards gala 6" data-clickable loading="lazy" /></div>
    <div class="gallery-item"><img src="photos/{gallery[6]}" alt="World Real Estate Awards gala 7" data-clickable loading="lazy" /></div>
    <div class="gallery-item"><img src="photos/{gallery[7]}" alt="World Real Estate Awards gala 8" data-clickable loading="lazy" /></div>
  </div>
</div></section>'''
    return _wrap(body, head)


# ============================================================
# CONTACT
# ============================================================
def contact_page():
    hero_img = take_photos(1)[0]
    head = _head(
        "Contact Us | World Real Estate Excellence Awards",
        "Contact the World Real Estate Excellence Awards team — email, WhatsApp, office address in Business Bay, Dubai. We respond within one business day.",
        "contact",
        "contact world real estate awards, real estate awards office dubai, awards team contact"
    )
    body = _page_hero(
        "Contact The Awards Team",
        "Get In Touch With",
        "The Awards Team",
        "Email, WhatsApp or visit our office in Business Bay, Dubai. We respond to all enquiries within one business day, in English and Arabic.",
        hero_img,
        [("Home","index.html"),("Contact","contact.html")]
    )
    body += f'''<section class="section content-section"><div class="container">
  <div class="contact-info-grid">
    <div class="contact-details">
      <div class="contact-item">
        <div class="contact-item-icon">✉</div>
        <div>
          <h4>Email</h4>
          <p><a href="mailto:awards@goldentreeawards.com">awards@goldentreeawards.com</a></p>
          <p style="font-size:0.78rem; color:var(--text-muted); margin-top:0.4rem;">For all entry, partnership and press enquiries.</p>
        </div>
      </div>
      <div class="contact-item">
        <div class="contact-item-icon">📞</div>
        <div>
          <h4>Phone &amp; WhatsApp</h4>
          <p><a href="tel:+971585856201">+971 58 585 6201</a></p>
          <p><a href="https://wa.me/971585856201" target="_blank" rel="noopener">WhatsApp Chat ›</a></p>
        </div>
      </div>
      <div class="contact-item">
        <div class="contact-item-icon">📍</div>
        <div>
          <h4>Office</h4>
          <p>The Binary by Omniyat<br />Office 1909 – 203, 19th Floor<br />Business Bay, Dubai<br />United Arab Emirates</p>
        </div>
      </div>
      <div class="contact-item">
        <div class="contact-item-icon">⏰</div>
        <div>
          <h4>Business Hours</h4>
          <p>Sunday – Thursday<br />09:00 – 18:00 GST<br />Response within 1 business day</p>
        </div>
      </div>
    </div>
    <div>
      <h2 style="font-family:var(--font-heading); font-size:1.6rem; color:var(--navy); margin-bottom:1rem;">Office Location</h2>
      <p style="margin-bottom:1.5rem; color:var(--text-muted);">Our awards secretariat is based in The Binary by Omniyat in Dubai's Business Bay — the heart of the regional real estate community.</p>
      <div class="map-embed">
        <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3614.246!2d55.265!3d25.187!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0!2zMjXCsDExJzEzLjIiTiA1NcKwMTUnNTQuMCJF!5e0!3m2!1sen!2sae!4v1700000000" loading="lazy" allowfullscreen referrerpolicy="no-referrer-when-downgrade" title="World Real Estate Excellence Awards Office Location"></iframe>
      </div>
    </div>
  </div>
</div></section>
{_cta_banner()}'''
    return _wrap(body, head)


# ============================================================
# FAQ
# ============================================================
def faq_page():
    hero_img = take_photos(1)[0]
    head = _head(
        "FAQ | Frequently Asked Questions | World Real Estate Excellence Awards",
        "Complete frequently asked questions about the World Real Estate Excellence Awards — eligibility, categories, judging, entry fees, deadlines and benefits.",
        "faq",
        "real estate awards faq, property awards questions, world real estate awards help"
    )
    body = _page_hero(
        "Frequently Asked Questions",
        "Frequently Asked",
        "Questions",
        "Everything you need to know about entering, judging, deadlines, fees, the gala and what winners receive.",
        hero_img,
        [("Home","index.html"),("FAQ","faq.html")]
    )

    all_faqs = [
      ("Programme Overview", [
        ("What are the World Real Estate Excellence Awards?", "An international, jury-led recognition programme honouring outstanding property developers, architects, brokers, agencies, interior designers and luxury property brands across 90+ countries."),
        ("Who organises the programme?", "The programme is delivered by Golden Tree Awards, an independent international awards organiser headquartered in Dubai. The awards secretariat is based in Business Bay, Dubai."),
        ("How long has the programme been running?", "Since 2019. More than 450 organisations and projects have been honoured across the programme's history."),
        ("How many categories are there?", "35+ categories across seven regions and 90+ countries, spanning developer, architecture, broker, agency, luxury, smart, sustainable and specialist tracks."),
        ("Is the programme independent?", "Yes. The jury is independent, declared conflicts are recused, and scoring criteria are published in advance."),
      ]),
      ("Eligibility &amp; Entry", [
        ("Who can submit a nomination?", "Property developers, architects, brokers, agencies, construction firms, interior designers, smart-building specialists, property managers and proptech innovators of any size across any region."),
        ("Are boutique organisations eligible?", "Yes. Sub-categories ensure boutique organisations compete fairly with larger international brands."),
        ("Can international developers operating in a region enter regional awards?", "Yes. International developers, architects and brokers actively operating in a region are eligible with judging context appropriate to their footprint."),
        ("How many categories can I enter?", "There is no hard cap. Most entrants compete in two to four categories; multi-category entries qualify for discounted fees."),
        ("What's the cost of entry?", "Entry fees vary by category and entry window — early-bird (discounted), standard, and late-entry (premium). Specific pricing is on the official entry portal."),
      ]),
      ("Judging &amp; Criteria", [
        ("How are entries judged?", "Independently by a senior global jury against published criteria specific to each category. The jury chair publishes a yearly methodology note."),
        ("Are scoring weightings published?", "Yes. Category-specific weightings are published in the resources section and alongside each category's detailed criteria."),
        ("How is sustainability assessed?", "Through verified performance — embodied carbon, operational energy, water, biodiversity — and credible third-party certification. Marketing claims without supporting evidence score poorly."),
        ("How long does judging take?", "Eligibility review ~2 weeks after entry close; jury scoring ~4–6 weeks; shortlists ~4–6 weeks before the gala; winners revealed live at the gala."),
        ("Can a scoring decision be appealed?", "Eligibility queries can be raised during eligibility review. Final jury scoring decisions are not subject to challenge to preserve independence."),
      ]),
      ("Winners &amp; Recognition", [
        ("What do winners receive?", "A globally recognised physical trophy, a digital and print winner's seal with usage guidelines, an editorial profile in the winners directory, press release distribution and alumni network access."),
        ("How long is the recognition valid?", "Permanent. Winners can use the seal indefinitely. Year-specific recognition (e.g. '2026 Winner') is particularly impactful in the year following."),
        ("Are seal usage guidelines provided?", "Yes. Detailed digital and print usage guidelines accompany the winner's seal."),
        ("Can a single project win multiple awards?", "Yes. A single project can win at country, regional and global level with separate jury scoring at each stage."),
        ("When is the gala?", "Each year in November in Dubai. Specific dates are published on the official entry portal."),
      ]),
      ("Process &amp; Submission", [
        ("How do I submit?", "Online via the official entry portal. 20–30 minutes per category."),
        ("What evidence is required?", "Written submission, photography, drawings (where applicable), performance data and supporting documentation. Specifics vary by category."),
        ("What file formats are accepted?", "JPG, PNG, PDF, MP4. Maximum file sizes are published on the entry portal."),
        ("Can I edit my entry after submission?", "Yes — until the entry-close deadline. Late edits cannot be accepted."),
        ("How do I get entry consultation?", "Contact the awards team at awards@goldentreeawards.com or WhatsApp +971 58 585 6201."),
      ]),
    ]

    body += '<section class="section faq-section"><div class="container">'
    for section_title, faqs in all_faqs:
      body += f'<div style="margin-bottom:3rem;"><h2 style="text-align:center; font-family:var(--font-heading); color:var(--navy); margin-bottom:1.5rem;">{section_title}</h2>'
      body += '<div class="faq-grid">'
      half = (len(faqs) + 1) // 2
      for col in (faqs[:half], faqs[half:]):
        body += '<div class="faq-col">'
        for q, a in col:
          body += f'<div class="faq-item"><button class="faq-question">{q} <span class="faq-icon">+</span></button><div class="faq-answer"><div class="faq-answer-inner">{a}</div></div></div>'
        body += '</div>'
      body += '</div></div>'
    body += '</div></section>'
    body += _cta_banner()

    # FAQ schema
    faq_schema_items = []
    for _, faqs in all_faqs:
      for q, a in faqs:
        faq_schema_items.append({"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}})
    schema_block = f'<script type="application/ld+json">{json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":faq_schema_items}, ensure_ascii=False)}</script>'
    head = head.replace('</head>', schema_block + '</head>') if '</head>' in head else head + schema_block

    return _wrap(body, head)


# ============================================================
# PAST WINNERS
# ============================================================
def past_winners_page():
    photos = take_photos(20)
    head = _head(
        "Past Winners | World Real Estate Excellence Awards",
        "Browse past winners of the World Real Estate Excellence Awards — leading property developers, architects, brokers and luxury property brands honoured across 90+ countries.",
        "past-winners",
        "past winners real estate awards, property award winners, real estate excellence winners"
    )
    body = _page_hero(
        "Past Winners",
        "Past Winners Of The",
        "Excellence Awards",
        "More than 450 organisations and projects across 90+ countries have been honoured by the World Real Estate Excellence Awards. Browse a selection of recent winners below.",
        photos[0],
        [("Home","index.html"),("Past Winners","past-winners.html")]
    )

    winners = [
      ("2025", "Luxury Master Developer", "Developer Of The Year — Global", "Branded Residence Portfolio"),
      ("2025", "International Architecture Studio", "Architecture Excellence Award", "Mixed-Use Landmark"),
      ("2025", "Prime Real Estate Agency", "Agency Of The Year — Luxury", "Luxury Sales Performance"),
      ("2025", "Smart Building Innovator", "Smart Building Of The Year", "Connected Residential Tower"),
      ("2025", "Sustainable Developer", "Sustainable Developer Of The Year", "Net-Positive Master Plan"),
      ("2025", "Branded Residence Operator", "Branded Residence Of The Year", "Hospitality-Partnered Residential"),
      ("2024", "Master Developer Group", "Master Developer Of The Year", "New City Programme"),
      ("2024", "Luxury Villa Developer", "Luxury Villa Of The Year", "Waterfront Estate"),
      ("2024", "Interior Design Studio", "Interior Design Of The Year", "Hospitality Interior"),
      ("2024", "Commercial Real Estate Platform", "Commercial Developer Of The Year", "Prime Office Tower"),
      ("2024", "Affordable Housing Builder", "Affordable Housing Of The Year", "Scaled Workforce Housing"),
      ("2024", "Resort Residence Operator", "Resort Residence Of The Year", "Beachfront Residence"),
    ]

    body += '<section class="section winners-section"><div class="container">'
    body += '''<div class="section-header center">
      <span class="section-eyebrow">Recent Winners</span>
      <h2 class="section-title h2">2024–2025 Award Winners</h2>
      <p class="section-desc">A snapshot of recently honoured developers, architects, brokers and luxury property brands across the programme.</p>
      <div class="section-divider"></div>
    </div>'''
    body += '<div class="winners-grid">'
    for i, (year, name, cat, project) in enumerate(winners):
      img = photos[1 + (i % (len(photos)-1))]
      body += f'''<div class="winner-card">
  <img class="winner-img" src="photos/{img}" alt="{name} {project}" data-clickable loading="lazy" />
  <div class="winner-body">
    <span class="winner-year">{year}</span>
    <h4>{name}</h4>
    <p>{project}</p>
    <span class="winner-category">{cat}</span>
  </div>
</div>'''
    body += '</div></div></section>'

    body += '''<section class="section about-section"><div class="container">
  <div class="content-grid">
    <div class="content-body">
      <h2>About The Winners Directory</h2>
      <p>The Winners Directory is the official record of organisations and projects honoured by the World Real Estate Excellence Awards. More than 450 entries have been added since the programme launched, spanning Asia, Europe, the Middle East, North America, South America, Africa and Oceania.</p>
      <p>The directory is searchable by region, category, year and organisation type. Multi-year winners and multi-category winners are highlighted, reflecting the depth of their recognition footprint. The directory is reviewed by international press, partners and buyers as a credibility reference across multiple commercial channels.</p>
      <h2>How Past Winners Use The Recognition</h2>
      <p>Past winners consistently report measurable commercial impact in the period following the award — stronger inbound demand, faster sales cycles, higher conversion in international markets, improved competition shortlist rates and stronger inbound recruitment. Several past Developer Of The Year and Master Developer Of The Year winners have explicitly cited the recognition in subsequent investor materials.</p>
      <p>The recognition's value compounds over time. Multi-year winners — organisations that have been recognised across multiple editions — consistently rank among the most credible brands in their respective regional markets.</p>
      <h2>Becoming A Winner</h2>
      <p>The path to becoming a winner is open to any organisation operating across the property industry. Nominations are accepted from developers, architects, brokers, agencies, construction firms, interior designers, property managers, smart-building specialists and proptech innovators.</p>
    </div>
    <aside class="content-sidebar">
      <div class="sidebar-widget">
        <h4>Browse By Category</h4>
        <div class="sidebar-links">
          <a href="property-developer-awards.html">Developer Awards</a>
          <a href="architecture-awards.html">Architecture Awards</a>
          <a href="luxury-real-estate-awards.html">Luxury Awards</a>
          <a href="real-estate-agency-awards.html">Agency Awards</a>
          <a href="broker-awards.html">Broker Awards</a>
          <a href="smart-building-awards.html">Smart Building</a>
          <a href="sustainable-developer-awards.html">Sustainable</a>
        </div>
      </div>'''
    body += f'''      <div class="sidebar-cta">
        <h4>Submit Your Nomination</h4>
        <p>Submit a nomination via the official entry portal.</p>
        <a class="btn btn-gold" href="{NOM_URL}" target="_blank" rel="noopener">Nominate Now ›</a>
      </div>
    </aside>
  </div>
</div></section>
{_cta_banner()}'''
    return _wrap(body, head)


# ============================================================
# GALLERY
# ============================================================
def gallery_page():
    photos = take_photos(24)
    head = _head(
        "Gallery | World Real Estate Excellence Awards",
        "Photography from past editions of the World Real Estate Excellence Awards — winners, jury, partners and the global property community on the gala stage.",
        "gallery",
        "real estate awards gallery, property awards photos, gala photography"
    )
    body = _page_hero(
        "Awards Gallery",
        "Moments From The",
        "Excellence Awards",
        "Photography from past editions of the World Real Estate Excellence Awards — winners on stage, jury panels, gala highlights and partner introductions across multiple years.",
        photos[0],
        [("Home","index.html"),("Gallery","gallery.html")]
    )

    body += '<section class="section gallery-section"><div class="container">'
    # Use a rich grid with mixed sizes
    layout = [
      ('wide', 1), ('', 2), ('tall', 3), ('', 4),
      ('', 5), ('wide', 6), ('', 7), ('', 8),
      ('tall', 9), ('', 10), ('', 11), ('wide', 12),
      ('', 13), ('', 14), ('', 15), ('wide', 16),
      ('', 17), ('tall', 18), ('', 19), ('', 20),
      ('', 21), ('wide', 22),
    ]
    body += '<div class="gallery-grid">'
    for cls, i in layout:
      if i < len(photos):
        body += f'<div class="gallery-item{" " + cls if cls else ""}"><img src="photos/{photos[i]}" alt="World Real Estate Awards moment {i}" data-clickable loading="lazy" /></div>'
    body += '</div></div></section>'
    body += _cta_banner()
    return _wrap(body, head)


# ============================================================
# BLOG
# ============================================================
def blog_page():
    photos = take_photos(12)
    head = _head(
        "Blog &amp; Insights | World Real Estate Excellence Awards",
        "Strategy, design and market thinking from the World Real Estate Excellence Awards — guides for developers, architects, agencies and luxury property brands.",
        "blog",
        "real estate awards blog, property awards insights, real estate strategy"
    )
    body = _page_hero(
        "Blog &amp; Insights",
        "Strategy, Design &amp;",
        "Market Thinking",
        "Practical strategy, design and market thinking from the World Real Estate Excellence Awards team and contributing experts.",
        photos[0],
        [("Home","index.html"),("Blog","blog.html")]
    )

    articles = [
      ("Awards Strategy", "How To Build A Winning Property Award Nomination",
       "The seven elements every shortlisted real estate entry has in common — and the mistakes that quietly disqualify strong projects.",
       photos[1], "5 min"),
      ("Market Insight", "Luxury Real Estate: Five Global Trends Reshaping The Sector",
       "From branded residences to wellness-led design, the forces redefining premium living across Dubai, London, New York and Singapore.",
       photos[2], "7 min"),
      ("Sustainability", "The Business Case For Sustainable Real Estate Development",
       "How net-positive design, smart-building systems and ESG reporting are now commercial drivers — not optional add-ons.",
       photos[3], "6 min"),
      ("Architecture", "How Architects Should Approach International Award Entries",
       "Project selection, photography, written narrative and the evidence that consistently wins architecture juries internationally.",
       photos[4], "8 min"),
      ("Developer", "Master Developer Strategy: Building Recognition For Multi-Decade Programmes",
       "How giga-project master developers should structure their international award programme across multiple commercial channels.",
       photos[5], "9 min"),
      ("Luxury", "Branded Residences: The State Of The Global Market In 2026",
       "Operator quality, service architecture and the structural shifts driving the next wave of branded residence launches worldwide.",
       photos[6], "6 min"),
      ("Brokerage", "Luxury Brokerage: Building HNW Credibility At Speed",
       "How emerging luxury brokers and agencies build credibility with the international HNW buyer base — the moves that compound.",
       photos[7], "5 min"),
      ("Interior Design", "Interior Design's Decade: Why The Function Is Now Strategic",
       "Why developers, hospitality operators and luxury residential brands are now placing interior design at the centre of commercial strategy.",
       photos[8], "7 min"),
      ("Smart Building", "Smart Buildings: What Institutional Investors Actually Want",
       "The smart-building features driving institutional commercial value — and the technology that is consistently ignored despite the marketing.",
       photos[9], "6 min"),
    ]

    body += '<section class="section blog-section"><div class="container">'
    body += '''<div class="section-header center">
      <span class="section-eyebrow">Articles</span>
      <h2 class="section-title h2">Latest Articles &amp; Guides</h2>
      <div class="section-divider"></div>
    </div>'''
    body += '<div class="articles-grid">'
    for cat, title, desc, img, read_time in articles:
      body += f'''<article class="article-card">
  <div class="article-img-wrap"><a href="blog.html"><img class="article-img" src="photos/{img}" alt="{title}" loading="lazy" /></a></div>
  <div class="article-body">
    <span class="article-cat">{cat}</span>
    <h3>{title}</h3>
    <p>{desc}</p>
    <div class="article-meta"><span>{read_time} read</span><span>· Awards Insights</span></div>
  </div>
</article>'''
    body += '</div></div></section>'
    body += _cta_banner()
    return _wrap(body, head)


# ============================================================
# RESOURCES
# ============================================================
def resources_page():
    hero_img = take_photos(1)[0]
    head = _head(
        "Resources | World Real Estate Excellence Awards",
        "Entry guides, judging criteria, sample submissions, key dates and downloadable resources for the World Real Estate Excellence Awards.",
        "resources",
        "real estate awards resources, property awards downloads, awards entry materials"
    )
    body = _page_hero(
        "Resources &amp; Downloads",
        "Entry Guides &amp;",
        "Programme Resources",
        "Entry guides, judging criteria documents, sample submissions, key dates and downloadable resources for the 2026 programme.",
        hero_img,
        [("Home","index.html"),("Resources","resources.html")]
    )

    resources = [
      ("Entry Guide", "Complete 2026 entry guide covering category selection, evidence preparation, written submission and submission process.", "award-submission-guide.html"),
      ("Judging Criteria", "Detailed scoring methodology, category-specific weightings and the jury chair's annual methodology note.", "award-judging-criteria.html"),
      ("Category Overview", "Complete list of 35+ categories across developer, architecture, broker, agency, luxury, smart, sustainable and specialist tracks.", "award-categories.html"),
      ("Benefits Overview", "Tangible commercial benefits of winning — visibility, brand authority, sales acceleration, investor confidence, talent.", "award-benefits.html"),
      ("Past Winners", "Searchable directory of past winners across 90+ countries and all category tracks.", "past-winners.html"),
      ("Regional Programmes", "Regional category sets across Asia, Europe, Middle East, Americas, Africa, Oceania and GCC.", "global-real-estate-awards.html"),
      ("FAQ", "Complete frequently asked questions covering eligibility, entry, judging, fees, deadlines and recognition.", "faq.html"),
      ("Press Programme", "International press programme around the gala — partner publications, distribution, contact information.", "contact.html"),
    ]

    body += '<section class="section content-section"><div class="container">'
    body += '<div class="related-grid">'
    for title, desc, url in resources:
      body += f'<div class="related-card"><h4>{title}</h4><p>{desc}</p><a href="{url}">Open ›</a></div>'
    body += '</div></div></section>'

    body += '''<section class="section about-section"><div class="container">
  <div class="content-grid">
    <div class="content-body">
      <h2>Key Dates — 2026 Edition</h2>
      <ul>
        <li><strong>Early-Bird Entry Window:</strong> Q1 2026 — Discounted fees, longest review period</li>
        <li><strong>Standard Entry Window:</strong> Q2–Q3 2026 — Standard fees, full eligibility review</li>
        <li><strong>Late Entry Window:</strong> Q4 2026 — Premium fees, expedited review</li>
        <li><strong>Eligibility Review:</strong> 2 weeks after each window close</li>
        <li><strong>Jury Scoring:</strong> 4–6 weeks following eligibility review</li>
        <li><strong>Shortlist Announcement:</strong> 4–6 weeks before the gala</li>
        <li><strong>International Gala:</strong> Mid-November 2026 — Dubai</li>
      </ul>

      <h2>Entry Process At A Glance</h2>
      <ol style="padding-left:1.4rem; margin-bottom:1.5rem;">
        <li>Select your categories (most entrants choose 2–4)</li>
        <li>Prepare your evidence package (photography, drawings, data)</li>
        <li>Draft and submit your written entry online</li>
        <li>Pay the entry fee — multi-category discounts apply</li>
        <li>Receive acknowledgment from the awards secretariat</li>
        <li>Respond to any eligibility clarifications</li>
        <li>Receive shortlist notification</li>
        <li>Attend the gala (winners revealed live)</li>
      </ol>

      <h2>Photography &amp; Visual Guidance</h2>
      <p>Visual evidence carries significant weight, particularly in architecture, luxury and design categories. We recommend professional architectural and editorial photography rather than marketing-led brochure imagery — the awards' archive is shared with international press partners, and strong photography compounds the recognition's commercial value.</p>

      <h2>Press &amp; Partner Programme</h2>
      <p>The international press programme around the gala includes partner publications across luxury, real estate, architecture and design media. Press accreditation, partner introduction enquiries and media partnership conversations should be directed to the awards team at awards@goldentreeawards.com.</p>
    </div>
    <aside class="content-sidebar">'''
    body += f'''      <div class="sidebar-cta">
        <h4>Begin Your Nomination</h4>
        <p>Submit via the official entry portal — 20–30 minutes per category.</p>
        <a class="btn btn-gold" href="{NOM_URL}" target="_blank" rel="noopener">Nominate Now ›</a>
      </div>
      <div class="sidebar-widget">
        <h4>Quick Links</h4>
        <div class="sidebar-links">
          <a href="award-submission-guide.html">Submission Guide</a>
          <a href="award-judging-criteria.html">Judging Criteria</a>
          <a href="award-categories.html">All Categories</a>
          <a href="award-benefits.html">Benefits</a>
          <a href="faq.html">FAQ</a>
          <a href="past-winners.html">Past Winners</a>
          <a href="contact.html">Contact Us</a>
        </div>
      </div>
    </aside>
  </div>
</div></section>
{_cta_banner()}'''
    return _wrap(body, head)


# ============================================================
# LEGAL PAGES
# ============================================================
def privacy_page():
    head = _head("Privacy Policy | World Real Estate Excellence Awards", "Privacy policy for the World Real Estate Excellence Awards programme.", "privacy-policy", "privacy policy")
    body = _page_hero("Privacy Policy", "Privacy", "Policy", "How we collect, use and protect your information when you interact with the World Real Estate Excellence Awards.", "award__(391).webp", [("Home","index.html"),("Privacy Policy","privacy-policy.html")])
    body += '''<section class="section content-section"><div class="container">
<div class="content-body">
<h2>Introduction</h2>
<p>This Privacy Policy explains how the World Real Estate Excellence Awards (operated by Golden Tree Awards) collects, uses and protects personal information from entrants, partners and visitors. By submitting a nomination or using this website you agree to the practices described below.</p>

<h2>Information We Collect</h2>
<p>We collect: contact details (name, email, phone, organisation), submission content (project descriptions, photography, drawings, supporting evidence), payment information (processed via PCI-compliant third-party processors), and website usage data (cookies, IP address, browser type).</p>

<h2>How We Use Information</h2>
<ul>
<li>To process nominations, eligibility review, jury scoring and winner announcements</li>
<li>To communicate updates on the programme, gala and recognition</li>
<li>To publish winners in the official directory and shared with international press partners</li>
<li>To process payments and issue receipts</li>
<li>To improve the entry process and website experience</li>
<li>To send programme news and updates to subscribers</li>
</ul>

<h2>Sharing Information</h2>
<p>We share entry content with our independent jury (under conflict-of-interest declarations), award secretariat staff and authorised partners. Winners are published publicly. We do not sell personal information to third parties.</p>

<h2>Data Retention</h2>
<p>Entry data is retained for the duration of the programme cycle and archived as part of the winners directory. Contact data is retained while you wish to receive programme updates. You can request deletion of personal data at any time.</p>

<h2>Your Rights</h2>
<p>You have the right to access, correct, delete or export your personal data. To exercise these rights, contact us at awards@goldentreeawards.com.</p>

<h2>Cookies</h2>
<p>This website uses essential cookies for site functionality and analytics cookies to understand usage. You can disable cookies via your browser settings.</p>

<h2>Security</h2>
<p>We use industry-standard security measures including encrypted data transmission, restricted access controls and regular security review.</p>

<h2>Contact</h2>
<p>For privacy enquiries: awards@goldentreeawards.com or +971 58 585 6201.</p>

<p style="color:var(--text-muted); font-size:0.82rem; margin-top:2rem;">Last updated: 24 May 2026</p>
</div>
</div></section>'''
    return _wrap(body, head)


def terms_page():
    head = _head("Terms &amp; Conditions | World Real Estate Excellence Awards", "Terms and conditions for the World Real Estate Excellence Awards programme.", "terms-conditions", "terms conditions")
    body = _page_hero("Terms &amp; Conditions", "Terms &amp;", "Conditions", "Terms and conditions governing participation in the World Real Estate Excellence Awards.", "award__(391).webp", [("Home","index.html"),("Terms &amp; Conditions","terms-conditions.html")])
    body += '''<section class="section content-section"><div class="container">
<div class="content-body">
<h2>Programme Overview</h2>
<p>The World Real Estate Excellence Awards is operated by Golden Tree Awards. By submitting a nomination, entrants agree to these terms and conditions in full.</p>

<h2>Eligibility</h2>
<p>The programme is open to property developers, architects, brokers, agencies, construction firms, interior designers, property managers, smart-building specialists and proptech innovators. Entrants must be legally established and authorised to enter on behalf of the work or organisation submitted.</p>

<h2>Entry Process</h2>
<p>Entries are submitted online via the official entry portal. Entry fees are payable at submission and are non-refundable. Entrants warrant that submitted material is accurate, that all consents required for image and content use have been obtained, and that the entry does not infringe third-party rights.</p>

<h2>Judging</h2>
<p>Entries are scored by an independent jury against published criteria. Scoring decisions are final. Eligibility queries may be raised during the eligibility review stage. The jury reserves the right to reclassify entries to the most appropriate category.</p>

<h2>Recognition &amp; Seal Use</h2>
<p>Winners may use the award seal in marketing, sales, PR and digital presence indefinitely, subject to the provided usage guidelines. Misuse of the seal (including misrepresentation of category or year) may result in revocation of recognition.</p>

<h2>Intellectual Property</h2>
<p>Entrants retain ownership of submitted material. By entering, entrants grant the programme a perpetual, royalty-free licence to use submitted imagery and content for award promotion, the winners directory, press programme and partner publications.</p>

<h2>Limitation Of Liability</h2>
<p>The programme is provided 'as is'. Golden Tree Awards' total liability for any claim relating to the programme is limited to the entry fee paid by the entrant.</p>

<h2>Force Majeure</h2>
<p>Golden Tree Awards is not liable for delays or cancellations arising from force majeure events, including pandemic, civil unrest, regulatory change or other circumstances beyond reasonable control.</p>

<h2>Governing Law</h2>
<p>These terms are governed by the laws of the United Arab Emirates. Disputes are subject to the exclusive jurisdiction of the courts of Dubai.</p>

<h2>Contact</h2>
<p>For terms enquiries: awards@goldentreeawards.com or +971 58 585 6201.</p>

<p style="color:var(--text-muted); font-size:0.82rem; margin-top:2rem;">Last updated: 24 May 2026</p>
</div></div></section>'''
    return _wrap(body, head)


def refund_page():
    head = _head("Refund Policy | World Real Estate Excellence Awards", "Refund policy for the World Real Estate Excellence Awards programme.", "refund-policy", "refund policy")
    body = _page_hero("Refund Policy", "Refund", "Policy", "Refund terms for entry fees in the World Real Estate Excellence Awards programme.", "award__(391).webp", [("Home","index.html"),("Refund Policy","refund-policy.html")])
    body += '''<section class="section content-section"><div class="container">
<div class="content-body">
<h2>Entry Fees</h2>
<p>All entry fees paid to the World Real Estate Excellence Awards are non-refundable once an entry has been submitted and acknowledged by the awards secretariat. This reflects the costs of eligibility review, jury preparation and administrative processing incurred from the point of submission.</p>

<h2>Cancellation By Entrant</h2>
<p>Entrants may withdraw an entry at any time before the entry-close deadline. Withdrawn entries are not eligible for refund, but the entrant's submission is removed from review.</p>

<h2>Cancellation By Programme</h2>
<p>In the unlikely event the programme is cancelled in full (not postponed) before jury scoring begins, entrants will receive a pro-rated refund. If the programme is postponed, entries are transferred automatically to the rescheduled edition.</p>

<h2>Payment Disputes</h2>
<p>Payment disputes must be raised within 14 days of payment. Contact awards@goldentreeawards.com with the payment reference and a description of the issue.</p>

<h2>Errors</h2>
<p>If an entrant pays for a category they cannot enter (for example, due to eligibility ineligibility identified during review), the awards secretariat will work with the entrant to redirect the fee to an eligible category. Refunds in such cases are at the discretion of the awards secretariat.</p>

<h2>Currency &amp; Taxes</h2>
<p>All fees are charged in US dollars unless otherwise specified. Local taxes, payment processing fees and currency conversion charges (where applicable) are non-refundable.</p>

<h2>Contact</h2>
<p>For refund enquiries: awards@goldentreeawards.com or +971 58 585 6201.</p>

<p style="color:var(--text-muted); font-size:0.82rem; margin-top:2rem;">Last updated: 24 May 2026</p>
</div></div></section>'''
    return _wrap(body, head)


# ============================================================
# RUN
# ============================================================
PAGES = [
  ("about.html", about_page),
  ("contact.html", contact_page),
  ("faq.html", faq_page),
  ("past-winners.html", past_winners_page),
  ("gallery.html", gallery_page),
  ("blog.html", blog_page),
  ("resources.html", resources_page),
  ("privacy-policy.html", privacy_page),
  ("terms-conditions.html", terms_page),
  ("refund-policy.html", refund_page),
]

if __name__ == "__main__":
    for filename, fn in PAGES:
      html = fn()
      (ROOT / filename).write_text(html, encoding="utf-8")
      print(f"  wrote {filename} ({len(html):,} chars)")
    print(f"\n✓ Wrote {len(PAGES)} standard pages")
