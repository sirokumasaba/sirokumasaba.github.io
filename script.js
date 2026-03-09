/* ====================================================
   しろくま鯖 — script.js
==================================================== */

/* ===== PAGE NAVIGATION ===== */
function showPage(pageId) {
  // hide all pages
  document.querySelectorAll('.page').forEach(function(p) {
    p.classList.remove('active');
  });

  // show target page
  var target = document.getElementById('page-' + pageId);
  if (target) {
    target.classList.add('active');
    // scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
    // trigger reveal for newly shown elements
    setTimeout(function() { triggerReveal(); }, 50);
  }

  // update nav items
  document.querySelectorAll('.nav-item').forEach(function(item) {
    item.classList.remove('active');
    if (item.getAttribute('data-page') === pageId) {
      item.classList.add('active');
    }
  });

  // close sidebar on mobile
  if (window.innerWidth <= 900) {
    closeSidebar();
  }
}

/* ===== SIDEBAR ===== */
function toggleSidebar() {
  var sidebar = document.getElementById('sidebar');
  var overlay = document.getElementById('overlay');
  sidebar.classList.toggle('open');
  overlay.classList.toggle('show');
}

function closeSidebar() {
  var sidebar = document.getElementById('sidebar');
  var overlay = document.getElementById('overlay');
  sidebar.classList.remove('open');
  overlay.classList.remove('show');
}

/* ===== COPY TEXT ===== */
function copyText(text, btn) {
  navigator.clipboard.writeText(text).then(function() {
    showToast();
    if (btn) {
      var original = btn.innerHTML;
      btn.innerHTML = '✔ コピー済み';
      btn.classList.add('copied');
      setTimeout(function() {
        btn.innerHTML = original;
        btn.classList.remove('copied');
      }, 2000);
    }
  }).catch(function() {
    // fallback for older browsers
    var el = document.createElement('textarea');
    el.value = text;
    el.style.position = 'fixed';
    el.style.opacity = '0';
    document.body.appendChild(el);
    el.select();
    document.execCommand('copy');
    document.body.removeChild(el);
    showToast();
    if (btn) {
      var original = btn.innerHTML;
      btn.innerHTML = '✔ コピー済み';
      btn.classList.add('copied');
      setTimeout(function() {
        btn.innerHTML = original;
        btn.classList.remove('copied');
      }, 2000);
    }
  });
}

/* ===== TOAST ===== */
function showToast() {
  var toast = document.getElementById('toast');
  toast.classList.add('show');
  setTimeout(function() {
    toast.classList.remove('show');
  }, 2200);
}

/* ===== SCROLL REVEAL ===== */
function triggerReveal() {
  var reveals = document.querySelectorAll('.page.active .reveal');
  reveals.forEach(function(el, i) {
    setTimeout(function() {
      el.classList.add('visible');
    }, i * 60);
  });
}

/* On scroll inside main */
function onScroll() {
  var reveals = document.querySelectorAll('.page.active .reveal:not(.visible)');
  reveals.forEach(function(el) {
    var rect = el.getBoundingClientRect();
    if (rect.top < window.innerHeight - 60) {
      el.classList.add('visible');
    }
  });
}

/* ===== INIT ===== */
document.addEventListener('DOMContentLoaded', function() {
  // initial reveal
  setTimeout(triggerReveal, 100);

  // scroll listener
  window.addEventListener('scroll', onScroll, { passive: true });

  // close sidebar when clicking outside on desktop
  document.addEventListener('click', function(e) {
    if (window.innerWidth > 900) return;
    var sidebar = document.getElementById('sidebar');
    var hamburger = document.getElementById('hamburger');
    if (sidebar.classList.contains('open')) {
      if (!sidebar.contains(e.target) && !hamburger.contains(e.target)) {
        closeSidebar();
      }
    }
  });

  // Keyboard: Escape closes sidebar
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') closeSidebar();
  });
});
