// ── NAV SCROLL ──────────────────────────────────────────────────
const navbar = document.getElementById('navbar');
if (navbar) {
  window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.scrollY > 50);
  });
}

// ── HAMBURGER ───────────────────────────────────────────────────
const hamburger = document.getElementById('hamburger');
const navLinks = document.getElementById('navLinks');
if (hamburger && navLinks) {
  hamburger.addEventListener('click', () => {
    navLinks.classList.toggle('open');
    const spans = hamburger.querySelectorAll('span');
    spans[0].style.transform = navLinks.classList.contains('open') ? 'rotate(45deg) translate(5px,5px)' : '';
    spans[1].style.opacity = navLinks.classList.contains('open') ? '0' : '1';
    spans[2].style.transform = navLinks.classList.contains('open') ? 'rotate(-45deg) translate(5px,-5px)' : '';
  });
  navLinks.querySelectorAll('a').forEach(a => a.addEventListener('click', () => navLinks.classList.remove('open')));
}

// ── SCROLL REVEAL ────────────────────────────────────────────────
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry, i) => {
    if (entry.isIntersecting) {
      setTimeout(() => entry.target.classList.add('visible'), i * 80);
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

// ── AUTO-DISMISS FLASHES ─────────────────────────────────────────
document.querySelectorAll('.flash').forEach(flash => {
  setTimeout(() => flash.style.opacity = '0', 5000);
  setTimeout(() => flash.remove(), 5400);
});

// ── GALLERY HOVER ────────────────────────────────────────────────
document.querySelectorAll('.gallery-masonry-item').forEach(item => {
  item.addEventListener('mouseenter', () => item.querySelector('.overlay').style.opacity = '1');
  item.addEventListener('mouseleave', () => item.querySelector('.overlay').style.opacity = '0');
});

// ── SMOOTH COUNTER ANIMATION ─────────────────────────────────────
function animateCounter(el, target) {
  let start = 0;
  const duration = 1500;
  const increment = target / (duration / 16);
  const timer = setInterval(() => {
    start += increment;
    if (start >= target) { el.textContent = target + (el.dataset.suffix || ''); clearInterval(timer); }
    else el.textContent = Math.floor(start) + (el.dataset.suffix || '');
  }, 16);
}

const counterObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const el = entry.target;
      const val = parseInt(el.textContent.replace(/[^0-9]/g, ''));
      if (val) animateCounter(el, val);
      counterObserver.unobserve(el);
    }
  });
});
document.querySelectorAll('.hero-stat-num, .about-stat-num').forEach(el => counterObserver.observe(el));
