/* ============================================================
   World Real Estate Excellence Awards — Main JavaScript
   ============================================================ */

(function () {
  'use strict';

  /* ---------- Sticky Header ---------- */
  const header = document.querySelector('.site-header');
  if (header) {
    window.addEventListener('scroll', () => {
      header.classList.toggle('scrolled', window.scrollY > 50);
    }, { passive: true });
  }

  /* ---------- Mobile Nav ---------- */
  const toggle = document.querySelector('.menu-toggle');
  const mobileNav = document.querySelector('.mobile-nav');
  if (toggle && mobileNav) {
    toggle.addEventListener('click', () => {
      const open = mobileNav.classList.toggle('open');
      toggle.classList.toggle('open', open);
      document.body.style.overflow = open ? 'hidden' : '';
    });
    mobileNav.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', () => {
        mobileNav.classList.remove('open');
        toggle.classList.remove('open');
        document.body.style.overflow = '';
      });
    });
  }

  /* ---------- Hero Slider ---------- */
  const slides = document.querySelectorAll('.hero-slide');
  const dots = document.querySelectorAll('.hero-dot');
  if (slides.length > 1) {
    let current = 0;
    const show = (i) => {
      slides[current].classList.remove('active');
      dots[current] && dots[current].classList.remove('active');
      current = (i + slides.length) % slides.length;
      slides[current].classList.add('active');
      dots[current] && dots[current].classList.add('active');
    };
    dots.forEach((d, i) => d.addEventListener('click', () => show(i)));
    const timer = setInterval(() => show(current + 1), 5500);
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) clearInterval(timer);
    });
  }

  /* ---------- FAQ Accordion ---------- */
  document.querySelectorAll('.faq-question').forEach(btn => {
    btn.addEventListener('click', () => {
      const item = btn.closest('.faq-item');
      const answer = item.querySelector('.faq-answer');
      const isOpen = btn.classList.contains('open');
      // Close all
      document.querySelectorAll('.faq-question.open').forEach(q => {
        q.classList.remove('open');
        q.closest('.faq-item').querySelector('.faq-answer').classList.remove('open');
      });
      if (!isOpen) {
        btn.classList.add('open');
        answer.classList.add('open');
      }
    });
  });

  /* ---------- Back to Top ---------- */
  const btt = document.querySelector('.back-to-top');
  if (btt) {
    window.addEventListener('scroll', () => {
      btt.classList.toggle('visible', window.scrollY > 500);
    }, { passive: true });
    btt.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
  }

  /* ---------- Animate on Scroll ---------- */
  const aosEls = document.querySelectorAll('.aos');
  if (aosEls.length) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); observer.unobserve(e.target); } });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
    aosEls.forEach(el => observer.observe(el));
  }

  /* ---------- Counter Animation ---------- */
  const counters = document.querySelectorAll('[data-count]');
  if (counters.length) {
    const countObserver = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          const el = e.target;
          const target = parseInt(el.getAttribute('data-count'), 10);
          const suffix = el.getAttribute('data-suffix') || '';
          let start = 0;
          const duration = 1800;
          const step = (timestamp) => {
            if (!start) start = timestamp;
            const progress = Math.min((timestamp - start) / duration, 1);
            const val = Math.floor(progress * target);
            el.textContent = val + suffix;
            if (progress < 1) requestAnimationFrame(step);
            else el.textContent = target + suffix;
          };
          requestAnimationFrame(step);
          countObserver.unobserve(el);
        }
      });
    }, { threshold: 0.5 });
    counters.forEach(c => countObserver.observe(c));
  }

  /* ---------- Image click → nomination ---------- */
  const NOM_URL = 'https://goldentreeawards.com/award-nomination';
  document.querySelectorAll('img[data-clickable]').forEach(img => {
    img.style.cursor = 'pointer';
    img.addEventListener('click', () => window.open(NOM_URL, '_blank', 'noopener'));
  });

  /* ---------- Newsletter form ---------- */
  document.querySelectorAll('.newsletter-form').forEach(form => {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const input = form.querySelector('.newsletter-input');
      if (input && input.value) {
        const btn = form.querySelector('.newsletter-btn');
        if (btn) { btn.textContent = '✓ Subscribed'; btn.style.background = '#2ecc71'; }
        input.value = '';
      }
    });
  });

  /* ---------- Active nav highlight ---------- */
  const path = window.location.pathname;
  document.querySelectorAll('.nav-link, .mobile-nav-links a').forEach(a => {
    if (a.getAttribute('href') && path.endsWith(a.getAttribute('href').replace(/^\.\//, '').replace(/\/+$/, ''))) {
      a.classList.add('active');
    }
  });

})();
