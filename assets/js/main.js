/* 白熊鯖 公式サイト — 共通処理（テーマ・メニュー・リンク・アコーディオン・コピー・トップへ戻る） */
(function () {
  'use strict';
  var doc = document, root = doc.documentElement, body = doc.body;
  root.classList.add('js');
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;

  function qa(s, c) { return Array.prototype.slice.call((c || doc).querySelectorAll(s)); }
  var toastEl, toastTimer;
  function toast(msg) {
    if (!toastEl) {
      toastEl = doc.createElement('div');
      toastEl.className = 'toast'; toastEl.setAttribute('role', 'status'); toastEl.setAttribute('aria-live', 'polite');
      body.appendChild(toastEl);
    }
    toastEl.textContent = msg; toastEl.classList.add('show');
    clearTimeout(toastTimer); toastTimer = setTimeout(function () { toastEl.classList.remove('show'); }, 2400);
  }
  window.shirokumaToast = toast;

  /* ---- テーマ ---- */
  function themeUI() {
    var dark = root.getAttribute('data-theme') === 'dark';
    qa('[data-theme-toggle]').forEach(function (b) {
      b.setAttribute('aria-pressed', dark ? 'true' : 'false');
      var l = b.querySelector('.tt-label'); if (l) l.textContent = dark ? 'ダークモード：ON' : 'ダークモード：OFF';
    });
  }
  qa('[data-theme-toggle]').forEach(function (b) {
    b.addEventListener('click', function () {
      var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('shirokuma-theme', next); } catch (e) { /* 保存不可でも動作継続 */ }
      themeUI();
    });
  });
  themeUI();

  /* ---- 外部リンク（未設定なら無効表示） ---- */
  var L = window.SITE_LINKS || {};
  qa('[data-link]').forEach(function (a) {
    var url = String(L[a.getAttribute('data-link')] || '').trim();
    if (/^https:\/\/[^\s]+$/i.test(url)) {
      a.href = url; a.target = '_blank'; a.rel = 'noopener noreferrer';
      a.classList.remove('is-disabled'); a.removeAttribute('aria-disabled'); a.removeAttribute('tabindex');
      var t = a.getAttribute('data-text-on'); if (t) a.textContent = t;
      var s = doc.createElement('span'); s.className = 'sr-only'; s.textContent = '（外部サイトが新しいタブで開きます）'; a.appendChild(s);
    }
  });
  qa('[data-link-note]').forEach(function (n) {
    var url = String(L[n.getAttribute('data-link-note')] || '').trim();
    if (/^https:\/\//i.test(url)) n.hidden = true;
  });

  /* ---- モバイルメニュー ---- */
  var sb = doc.getElementById('sidebar'), mb = doc.getElementById('menu-btn'), ov = doc.getElementById('overlay');
  var mq = window.matchMedia('(max-width: 960px)');
  function isOpen() { return body.classList.contains('menu-open'); }
  function openMenu() {
    body.classList.add('menu-open'); mb.setAttribute('aria-expanded', 'true');
    var f = sb.querySelector('a[href]'); if (f) setTimeout(function () { f.focus(); }, 30);
  }
  function closeMenu(ret) {
    body.classList.remove('menu-open'); mb.setAttribute('aria-expanded', 'false'); if (ret) mb.focus();
  }
  if (sb && mb) {
    mb.addEventListener('click', function () { isOpen() ? closeMenu(true) : openMenu(); });
    if (ov) ov.addEventListener('click', function () { closeMenu(true); });
    doc.addEventListener('keydown', function (e) {
      if (!isOpen() || !mq.matches) return;
      if (e.key === 'Escape') { closeMenu(true); return; }
      if (e.key === 'Tab') {
        var f = qa('a[href],button:not([disabled])', sb).filter(function (x) { return x.offsetParent !== null; });
        if (!f.length) return;
        var first = f[0], last = f[f.length - 1];
        if (e.shiftKey && (doc.activeElement === first || !sb.contains(doc.activeElement))) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && doc.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    });
    var onMq = function () { if (!mq.matches) closeMenu(false); };
    mq.addEventListener ? mq.addEventListener('change', onMq) : mq.addListener(onMq);
  }

  /* ---- アコーディオン（JS無効時は全文表示） ---- */
  qa('.acc-btn').forEach(function (b) {
    var p = doc.getElementById(b.getAttribute('aria-controls')); if (!p) return;
    p.hidden = true; b.setAttribute('aria-expanded', 'false');
    b.addEventListener('click', function () {
      var open = b.getAttribute('aria-expanded') === 'true';
      b.setAttribute('aria-expanded', open ? 'false' : 'true'); p.hidden = open;
    });
  });

  /* ---- トップへ戻る ---- */
  var tb = doc.getElementById('top-btn');
  if (tb) {
    var onScroll = function () { tb.classList.toggle('show', window.pageYOffset > 400); };
    window.addEventListener('scroll', onScroll, { passive: true }); onScroll();
    tb.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' });
      var t = doc.getElementById('main'); if (t) { t.setAttribute('tabindex', '-1'); t.focus({ preventScroll: true }); }
    });
  }

  /* ---- スクロール出現 ---- */
  var rv = qa('.reveal');
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: 0.12 });
    rv.forEach(function (n) { io.observe(n); });
  } else { rv.forEach(function (n) { n.classList.add('in'); }); }

  /* ---- コピー（設定済みの値のみ） ---- */
  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) return navigator.clipboard.writeText(text);
    return new Promise(function (ok, ng) {
      try {
        var t = doc.createElement('textarea'); t.value = text; t.setAttribute('readonly', '');
        t.style.cssText = 'position:fixed;left:-9999px;top:0'; body.appendChild(t); t.select();
        var r = doc.execCommand('copy'); body.removeChild(t); r ? ok() : ng(new Error('copy failed'));
      } catch (e) { ng(e); }
    });
  }
  window.shirokumaCopy = function (text, label) {
    text = String(text == null ? '' : text).trim();
    if (!text) { toast('コピーできる情報が未設定です'); return; }
    copyText(text).then(function () { toast((label || '内容') + 'をコピーしました'); },
      function () { toast('コピーに失敗しました。手動で選択してコピーしてください'); });
  };
})();
