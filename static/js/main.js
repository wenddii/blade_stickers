/**
 * BLADE STICKERS — BRIGHT CULTURE BRAND JAVASCRIPT ENGINE
 * Fast, fluid, mobile-first, high performance vanilla JS.
 */

document.addEventListener('DOMContentLoaded', () => {
  initNavbar();
  initMobileMenu();
  initBackToTop();
  initScrollReveal();
  initStatCounters();
  initModalLightbox();
  initContactFormAjax();
  initCardHoverEffects();
});


/* ── Navbar Scroll Behavior ────────────────────────────────────────────────── */
function initNavbar() {
  const navbar = document.getElementById('mainNavbar');
  if (!navbar) return;

  window.addEventListener('scroll', () => {
    if (window.scrollY > 40) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  }, { passive: true });
}


/* ── Mobile Drawer Navigation ──────────────────────────────────────────────── */
function initMobileMenu() {
  const toggleBtn = document.getElementById('mobileToggle');
  const mobileMenu = document.getElementById('mobileMenu');

  if (!toggleBtn || !mobileMenu) return;

  toggleBtn.addEventListener('click', () => {
    const isOpen = mobileMenu.classList.toggle('open');
    toggleBtn.setAttribute('aria-expanded', isOpen);
    toggleBtn.textContent = isOpen ? '✕' : '☰';
    document.body.style.overflow = isOpen ? 'hidden' : '';
  });

  // Close when clicking any menu link
  mobileMenu.querySelectorAll('.mob-nav__link').forEach(link => {
    link.addEventListener('click', () => {
      mobileMenu.classList.remove('open');
      toggleBtn.textContent = '☰';
      toggleBtn.setAttribute('aria-expanded', 'false');
      document.body.style.overflow = '';
    });
  });
}


/* ── Back to Top Floating Button ───────────────────────────────────────────── */
function initBackToTop() {
  const topBtn = document.getElementById('backToTopBtn');
  if (!topBtn) return;

  window.addEventListener('scroll', () => {
    if (window.scrollY > 400) {
      topBtn.style.opacity = '1';
      topBtn.style.pointerEvents = 'auto';
    } else {
      topBtn.style.opacity = '0';
      topBtn.style.pointerEvents = 'none';
    }
  }, { passive: true });

  topBtn.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}


/* ── Intersection Observer Scroll Reveal ───────────────────────────────────── */
function initScrollReveal() {
  const elements = document.querySelectorAll('.js-reveal');
  if (!elements.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('revealed');
        observer.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.08,
    rootMargin: '0px 0px -30px 0px'
  });

  elements.forEach(el => observer.observe(el));
}


/* ── Smooth Eased Stat Counters ────────────────────────────────────────────── */
function initStatCounters() {
  const counters = document.querySelectorAll('.js-counter');
  if (!counters.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateCounter(entry.target);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.4 });

  counters.forEach(el => observer.observe(el));
}

function animateCounter(el) {
  const target = parseInt(el.getAttribute('data-target'), 10);
  if (isNaN(target)) return;

  const duration = 1800; // ms
  const startTime = performance.now();

  function update(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);

    // Ease-out cubic curve
    const eased = 1 - Math.pow(1 - progress, 3);
    const current = Math.floor(eased * target);

    el.textContent = current.toLocaleString() + '+';

    if (progress < 1) {
      requestAnimationFrame(update);
    } else {
      el.textContent = target.toLocaleString() + '+';
    }
  }

  requestAnimationFrame(update);
}


/* ── Quick View Modal / Lightbox ───────────────────────────────────────────── */
function initModalLightbox() {
  const modalBackdrop = document.getElementById('productModal');
  const closeBtn = document.getElementById('modalCloseBtn');

  if (!modalBackdrop) return;

  // Click handler on any quick view button
  document.addEventListener('click', (e) => {
    const trigger = e.target.closest('.js-quick-view');
    if (trigger) {
      e.preventDefault();
      const productId = trigger.getAttribute('data-product-id');
      fetchProductModalData(productId);
    }
  });

  if (closeBtn) {
    closeBtn.addEventListener('click', closeModal);
  }

  modalBackdrop.addEventListener('click', (e) => {
    if (e.target === modalBackdrop) {
      closeModal();
    }
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modalBackdrop.classList.contains('open')) {
      closeModal();
    }
  });

  function closeModal() {
    modalBackdrop.classList.remove('open');
    document.body.style.overflow = '';
  }
}

function fetchProductModalData(productId) {
  const modalBackdrop = document.getElementById('productModal');
  const modalImg = document.getElementById('modalImg');
  const modalCategory = document.getElementById('modalCategory');
  const modalTitle = document.getElementById('modalTitle');
  const modalPrice = document.getElementById('modalPrice');
  const modalDesc = document.getElementById('modalDesc');
  const modalDetailLink = document.getElementById('modalDetailLink');
  const modalTelegramLink = document.getElementById('modalTelegramLink');
  const modalWhatsAppLink = document.getElementById('modalWhatsAppLink');

  if (!modalBackdrop) return;

  fetch(`/products/api/${productId}/modal/`)
    .then(response => response.json())
    .then(data => {
      if (modalImg) modalImg.src = data.image_url || '';
      if (modalCategory) modalCategory.textContent = data.category;
      if (modalTitle) modalTitle.textContent = data.title;
      if (modalPrice) {
        modalPrice.textContent = data.price && !data.price.includes('Custom') ? `$${data.price}` : data.price;
      }
      if (modalDesc) modalDesc.textContent = data.description;
      if (modalDetailLink) modalDetailLink.href = data.url;

      // CTA order deep links
      const encodedMsg = encodeURIComponent(`Hi Blade Stickers! I want to order/inquire: ${data.title}`);
      if (modalTelegramLink) {
        modalTelegramLink.href = `https://t.me/bladestickers?text=${encodedMsg}`;
      }
      if (modalWhatsAppLink) {
        modalWhatsAppLink.href = `https://wa.me/251912345678?text=${encodedMsg}`;
      }

      modalBackdrop.classList.add('open');
      document.body.style.overflow = 'hidden';
    })
    .catch(err => console.error('Error loading product details:', err));
}


/* ── Contact Form AJAX ─────────────────────────────────────────────────────── */
function initContactFormAjax() {
  const form = document.getElementById('contactForm');
  const alertBox = document.getElementById('contactFormAlert');

  if (!form) return;

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const formData = new FormData(form);
    const submitBtn = form.querySelector('button[type="submit"]');

    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.textContent = 'Sending... ⏳';
    }

    fetch(form.action, {
      method: 'POST',
      body: formData,
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
      }
    })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        form.reset();
        if (alertBox) {
          alertBox.style.display = 'block';
          alertBox.className = 'alert alert--ok';
          alertBox.textContent = data.message;
        }
      } else {
        if (alertBox) {
          alertBox.style.display = 'block';
          alertBox.className = 'alert alert--err';
          alertBox.textContent = 'Please check the entered information and try again.';
        }
      }
    })
    .catch(err => {
      console.error('Contact submission error:', err);
      if (alertBox) {
        alertBox.style.display = 'block';
        alertBox.className = 'alert alert--err';
        alertBox.textContent = 'Connection error. Please contact us directly on WhatsApp.';
      }
    })
    .finally(() => {
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Send Message 🚀';
      }
    });
  });
}


/* ── Subtle Micro-Interactions on Desktop Cards ───────────────────────────── */
function initCardHoverEffects() {
  if ('ontouchstart' in window) return;

  const cards = document.querySelectorAll('.pcard, .cat, .comm-item');
  cards.forEach(card => {
    card.addEventListener('mouseenter', () => {
      card.style.transition = 'transform 0.3s cubic-bezier(0.22, 1, 0.36, 1), box-shadow 0.3s cubic-bezier(0.22, 1, 0.36, 1)';
    });
  });
}
