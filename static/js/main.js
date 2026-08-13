/**
 * BLADE STICKERS — PREMIUM MOTION ENGINE
 * Culture brand interactions. Physical. Intentional. Smooth.
 */

document.addEventListener('DOMContentLoaded', () => {
  initNavbar();
  initMobileMenu();
  initBackToTop();
  initScrollReveal();
  initStatCounters();
  initModalLightbox();
  initContactFormAjax();
  initMagneticCards();
  initParallaxDepth();
});


/* ── Navbar scroll behavior ────────────────────────────────────────────────── */
function initNavbar() {
  const navbar = document.getElementById('mainNavbar');
  if (!navbar) return;

  let lastScroll = 0;

  window.addEventListener('scroll', () => {
    const currentScroll = window.scrollY;

    if (currentScroll > 50) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }

    lastScroll = currentScroll;
  }, { passive: true });
}


/* ── Mobile Menu ───────────────────────────────────────────────────────────── */
function initMobileMenu() {
  const toggleBtn = document.getElementById('mobileToggle');
  const navLinks = document.getElementById('navLinks');

  if (!toggleBtn || !navLinks) return;

  toggleBtn.addEventListener('click', () => {
    const isOpen = navLinks.classList.toggle('open');
    toggleBtn.setAttribute('aria-expanded', isOpen);
    toggleBtn.textContent = isOpen ? '✕' : '☰';

    // Prevent body scroll when menu is open
    document.body.style.overflow = isOpen ? 'hidden' : '';
  });

  // Close on link click
  navLinks.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
      navLinks.classList.remove('open');
      toggleBtn.textContent = '☰';
      document.body.style.overflow = '';
    });
  });
}


/* ── Back to Top ───────────────────────────────────────────────────────────── */
function initBackToTop() {
  const topBtn = document.getElementById('backToTopBtn');
  if (!topBtn) return;

  window.addEventListener('scroll', () => {
    if (window.scrollY > 500) {
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


/* ── Scroll Reveal — staggered with rotation correction ────────────────────── */
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
    threshold: 0.1,
    rootMargin: '0px 0px -40px 0px'
  });

  elements.forEach(el => observer.observe(el));
}


/* ── Stat Counter Animation — smooth eased counting ────────────────────────── */
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
  }, { threshold: 0.5 });

  counters.forEach(el => observer.observe(el));
}

function animateCounter(el) {
  const target = parseInt(el.getAttribute('data-target'), 10);
  if (isNaN(target)) return;

  const duration = 2000; // ms
  const startTime = performance.now();

  function update(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);

    // Ease out cubic
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

  // Open modal trigger
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
      if (modalPrice) modalPrice.textContent = data.price;
      if (modalDesc) modalDesc.textContent = data.description;
      if (modalDetailLink) modalDetailLink.href = data.url;

      // CTA order links
      const encodedMsg = encodeURIComponent(`Hi Blade Stickers! I want to inquire/order: ${data.title}`);
      if (modalTelegramLink) {
        modalTelegramLink.href = `https://t.me/bladestickers?text=${encodedMsg}`;
      }
      if (modalWhatsAppLink) {
        modalWhatsAppLink.href = `https://wa.me/251912345678?text=${encodedMsg}`;
      }

      modalBackdrop.classList.add('open');
      document.body.style.overflow = 'hidden';
    })
    .catch(err => console.error('Error fetching product data:', err));
}


/* ── Contact Form AJAX ─────────────────────────────────────────────────────── */
function initContactFormAjax() {
  const form = document.getElementById('contactForm');
  const alertBox = document.getElementById('contactFormAlert');

  if (!form) return;

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const formData = new FormData(form);

    // Disable submit button
    const submitBtn = form.querySelector('button[type="submit"]');
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.textContent = 'Sending...';
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
          alertBox.className = 'contact-alert success-alert';
          alertBox.textContent = data.message;
        }
      } else {
        if (alertBox) {
          alertBox.style.display = 'block';
          alertBox.className = 'contact-alert error-alert';
          alertBox.textContent = 'Please check the fields and try again.';
        }
      }
    })
    .catch(err => {
      console.error('Submission error:', err);
      if (alertBox) {
        alertBox.style.display = 'block';
        alertBox.className = 'contact-alert error-alert';
        alertBox.textContent = 'Network error. Please try again.';
      }
    })
    .finally(() => {
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Send Message →';
      }
    });
  });
}


/* ── Magnetic Cards — subtle cursor-following tilt ─────────────────────────── */
function initMagneticCards() {
  // Only on non-touch devices
  if ('ontouchstart' in window) return;

  const cards = document.querySelectorAll('.product-card, .polaroid, .category-card');

  cards.forEach(card => {
    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const centerX = rect.width / 2;
      const centerY = rect.height / 2;

      const rotateX = ((y - centerY) / centerY) * -3;
      const rotateY = ((x - centerX) / centerX) * 3;

      card.style.transform = `perspective(800px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-10px) scale(1.02)`;
    });

    card.addEventListener('mouseleave', () => {
      card.style.transform = '';
    });
  });
}


/* ── Parallax Depth — subtle movement on scroll ───────────────────────────── */
function initParallaxDepth() {
  const heroStickers = document.querySelectorAll('.hero-sticker');
  if (!heroStickers.length) return;

  let ticking = false;

  window.addEventListener('scroll', () => {
    if (!ticking) {
      requestAnimationFrame(() => {
        const scrolled = window.scrollY;

        heroStickers.forEach((sticker, index) => {
          const speed = 0.03 + (index * 0.015);
          const yOffset = scrolled * speed;
          const baseTransform = sticker.style.transform || '';

          // Only apply parallax within viewport
          if (scrolled < window.innerHeight) {
            sticker.style.setProperty('--parallax-y', `${yOffset}px`);
          }
        });

        ticking = false;
      });

      ticking = true;
    }
  }, { passive: true });
}
