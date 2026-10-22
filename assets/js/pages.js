/* 白熊鯖 公式サイト — ページ別処理（お知らせ・ギャラリー・プラグイン・参加方法・トップ） */
(function () {
  'use strict';
  var doc = document;
  function $(id) { return doc.getElementById(id); }
  function el(tag, cls, text) { var e = doc.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; }
  function arr(x) { return Array.isArray(x) ? x : []; }
  function fillOptions(sel, list, allLabel) {
    sel.appendChild(new Option(allLabel, ''));
    list.forEach(function (c) { sel.appendChild(new Option(c, c)); });
  }
  function norm(s) { return String(s == null ? '' : s).toLowerCase(); }

  /* ---------- お知らせ ---------- */
  function sortedNews() {
    return arr(window.NEWS_DATA).slice().sort(function (a, b) { return String(b.date).localeCompare(String(a.date)); });
  }
  function newsCard(n) {
    var li = el('li', 'card news-item');
    var t = el('time', null, n.date || ''); if (n.date) t.setAttribute('datetime', n.date);
    var h = el('div'); h.appendChild(el('span', 'badge', n.category || 'お知らせ'));
    li.appendChild(t); li.appendChild(h);
    li.appendChild(el('h3', null, n.title || '（無題）'));
    if (n.body) li.appendChild(el('p', null, n.body));
    return li;
  }
  var nl = $('news-list');
  if (nl) {
    var q = $('news-q'), cat = $('news-cat'), cnt = $('news-count'), clr = $('news-clear'), emp = $('news-empty');
    fillOptions(cat, arr(window.NEWS_CATEGORIES), 'すべてのカテゴリ');
    var renderNews = function () {
      var kw = norm(q.value).trim(), c = cat.value;
      var rs = sortedNews().filter(function (n) {
        return (!c || n.category === c) && (!kw || norm(n.title + ' ' + n.body + ' ' + n.category).indexOf(kw) > -1);
      });
      nl.textContent = '';
      rs.forEach(function (n) { nl.appendChild(newsCard(n)); });
      var total = sortedNews().length;
      cnt.textContent = total ? rs.length + ' 件のお知らせ（全 ' + total + ' 件）' : '';
      emp.hidden = rs.length > 0;
      emp.textContent = total ? '条件に一致するお知らせはありません。キーワードやカテゴリを変更してください。' : 'お知らせはまだありません。公式発表があり次第、こちらに掲載します。';
    };
    q.addEventListener('input', renderNews); cat.addEventListener('change', renderNews);
    clr.addEventListener('click', function () { q.value = ''; cat.value = ''; renderNews(); q.focus(); });
    renderNews();
  }
  var hn = $('home-news');
  if (hn) {
    var latest = sortedNews().slice(0, 3);
    if (!latest.length) { hn.appendChild(el('li', 'empty', 'お知らせはまだありません。公式発表があり次第、こちらに掲載します。')); }
    latest.forEach(function (n) { hn.appendChild(newsCard(n)); });
  }

  /* ---------- ギャラリー ---------- */
  var gl = $('gallery-list');
  if (gl) {
    var cats = arr(window.GALLERY_CATEGORIES), chips = $('gallery-chips'), gc = $('gallery-count'), ge = $('gallery-empty'), cur = '';
    var drawGallery = function () {
      var all = arr(window.GALLERY_DATA);
      var rs = all.filter(function (g) { return !cur || g.category === cur; });
      gl.textContent = '';
      rs.forEach(function (g) {
        var li = el('li', 'card shot'), img = el('div', 'img');
        var ph = function () { img.textContent = ''; var p = el('div', 'placeholder', '準備中'); p.style.height = '100%'; p.style.aspectRatio = 'auto'; img.appendChild(p); };
        if (g.image) {
          var i = el('img'); i.src = g.image; i.alt = g.alt || g.title || ''; i.loading = 'lazy'; i.decoding = 'async';
          i.addEventListener('error', ph); img.appendChild(i);
        } else { ph(); }
        var b = el('div', 'body'); b.appendChild(el('span', 'badge', g.category || ''));
        b.appendChild(el('h3', null, g.title || '')); if (g.description) b.appendChild(el('p', null, g.description));
        li.appendChild(img); li.appendChild(b); gl.appendChild(li);
      });
      gc.textContent = all.length ? rs.length + ' 件の画像' : '';
      ge.hidden = rs.length > 0;
      ge.textContent = all.length ? 'このカテゴリの画像はまだありません。' : 'ギャラリーは準備中です。サーバーの開設後、実際のスクリーンショットを掲載します。';
    };
    ['すべて'].concat(cats).forEach(function (c) {
      var b = el('button', 'chip', c); b.type = 'button'; b.setAttribute('aria-pressed', (c === 'すべて') ? 'true' : 'false');
      b.addEventListener('click', function () {
        cur = c === 'すべて' ? '' : c;
        Array.prototype.forEach.call(chips.children, function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
        drawGallery();
      });
      chips.appendChild(b);
    });
    drawGallery();
  }

  /* ---------- プラグイン ---------- */
  var pl = $('plugin-list');
  if (pl) {
    var pq = $('plugin-q'), pc = $('plugin-cat'), pcnt = $('plugin-count'), pemp = $('plugin-empty'), pclr = $('plugin-clear');
    fillOptions(pc, arr(window.PLUGIN_CATEGORIES), 'すべてのカテゴリ');
    var drawPlugins = function () {
      var all = arr(window.PLUGINS_DATA), kw = norm(pq.value).trim(), c = pc.value;
      var rs = all.filter(function (p) {
        return (!c || p.category === c) && (!kw || norm([p.name, p.summary, p.description, p.category].join(' ')).indexOf(kw) > -1);
      });
      pl.textContent = '';
      rs.forEach(function (p) {
        var li = el('li', 'card'), hd = el('div', 'pl-head');
        hd.appendChild(el('h3', null, p.name || '（名称未設定）'));
        if (p.category) hd.appendChild(el('span', 'badge', p.category));
        if (p.status) hd.appendChild(el('span', 'badge ' + (p.status === '導入済み' ? 'green' : 'soon'), p.status));
        li.appendChild(hd);
        if (p.summary) li.appendChild(el('p', null, p.summary)).style.fontWeight = '700';
        if (p.description) { var d = el('p', null, p.description); d.style.whiteSpace = 'pre-line'; li.appendChild(d); }
        if (arr(p.features).length) { var ul = el('ul', 'feat-list'); p.features.forEach(function (f) { ul.appendChild(el('li', null, f)); }); li.appendChild(ul); }
        if (arr(p.commands).length) {
          var w = el('div', 'scroll-x'), t = el('table', 'cmds'), th = el('thead'), tr = el('tr');
          tr.appendChild(el('th', null, 'コマンド')); tr.appendChild(el('th', null, '内容')); th.appendChild(tr); t.appendChild(th);
          var tb = el('tbody');
          p.commands.forEach(function (cm) { var r = el('tr'), td = el('td'); td.appendChild(el('code', null, cm.command || '')); r.appendChild(td); r.appendChild(el('td', null, cm.description || '')); tb.appendChild(r); });
          t.appendChild(tb); w.appendChild(t); li.appendChild(w);
        }
        if (p.notes) { var n = el('p', null, '注意：' + p.notes); n.style.marginTop = '12px'; n.style.color = 'var(--muted)'; li.appendChild(n); }
        pl.appendChild(li);
      });
      pcnt.textContent = all.length ? rs.length + ' 件のプラグイン（全 ' + all.length + ' 件）' : '';
      pemp.hidden = rs.length > 0;
      pemp.textContent = all.length ? '条件に一致するプラグインはありません。' : 'プラグイン情報は準備中です。導入するプラグインが確定し次第、機能やコマンドをこちらで紹介します。';
    };
    pq.addEventListener('input', drawPlugins); pc.addEventListener('change', drawPlugins);
    pclr.addEventListener('click', function () { pq.value = ''; pc.value = ''; drawPlugins(); pq.focus(); });
    drawPlugins();
  }
  var hp = $('home-plugins-count');
  if (hp) { var n = arr(window.PLUGINS_DATA).length; hp.textContent = n ? n + ' 件のプラグインを紹介中' : 'プラグイン情報は準備中です'; }

  /* ---------- 参加方法：接続情報 ---------- */
  var info = window.SERVER_INFO;
  if (info) {
    Array.prototype.forEach.call(doc.querySelectorAll('[data-info]'), function (row) {
      var key = row.getAttribute('data-info'), v = String(info[key] == null ? '' : info[key]).trim();
      var out = row.querySelector('.val'), btn = row.querySelector('[data-copy-btn]');
      if (v) {
        out.textContent = v; out.classList.remove('unset');
        if (btn) { btn.disabled = false; btn.removeAttribute('aria-disabled'); btn.textContent = 'コピー';
          btn.addEventListener('click', function () { window.shirokumaCopy(v, row.getAttribute('data-label')); }); }
      } else {
        out.textContent = '準備中'; out.classList.add('unset');
        if (btn) { btn.disabled = true; btn.setAttribute('aria-disabled', 'true'); btn.textContent = 'コピー不可'; }
      }
    });
  }
})();
