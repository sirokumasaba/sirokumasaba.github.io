# -*- coding: utf-8 -*-
"""白熊鯖サイト 自動テスト（Python + Playwright/Chromium）
使い方: python3 tests/run_tests.py   （サイト直下で実行。ネットワーク不要）
サブパス（/shirokuma-site/）配下に配信して GitHub Pages プロジェクトサイト相当の条件で検査します。
注意: 実際の GitHub Pages 上での検証ではありません。"""
import os, re, sys, json, shutil, tempfile, threading, functools, http.server, socketserver
from html.parser import HTMLParser
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = ["index","about","plugins","join","news","recruitment","rules-faq","gallery"]
SUB = "/shirokuma-site/"
R = []  # (area, name, status, detail)
def rec(area, name, ok, detail=""): R.append((area, name, "PASS" if ok else "FAIL", detail))

tmp = tempfile.mkdtemp(); dst = os.path.join(tmp, "shirokuma-site")
shutil.copytree(ROOT, dst, ignore=shutil.ignore_patterns("tests", ".git", "*.md"))
class H(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
handler = functools.partial(H, directory=tmp)
srv = socketserver.TCPServer(("127.0.0.1", 0), handler); PORT = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
BASE = f"http://127.0.0.1:{PORT}{SUB}"

# ---------- 静的検査 ----------
class P(HTMLParser):
    def __init__(s): super().__init__(); s.links=[]; s.ids=[]; s.h1=0; s.title=""; s.desc=""; s.lang=""; s._t=False; s.imgs_noalt=0
    def handle_starttag(s, t, a):
        a = dict(a)
        if t=="html": s.lang=a.get("lang","")
        if t=="h1": s.h1+=1
        if t=="title": s._t=True
        if t=="meta" and a.get("name")=="description": s.desc=a.get("content","")
        if t=="img" and "alt" not in a: s.imgs_noalt+=1
        if "id" in a: s.ids.append(a["id"])
        for k in ("href","src"):
            if k in a: s.links.append(a[k])
    def handle_endtag(s,t):
        if t=="title": s._t=False
    def handle_data(s,d):
        if s._t: s.title+=d
titles=set(); descs=set()
for p in PAGES:
    f = os.path.join(ROOT, p+".html"); ok = os.path.exists(f); rec("静的","ページ存在 "+p+".html", ok)
    if not ok: continue
    src = open(f, encoding="utf-8").read(); ps = P(); ps.feed(src)
    rec("静的",f"{p}: lang=ja / h1が1つ / titleとdescriptionあり / img alt", ps.lang=="ja" and ps.h1==1 and ps.title and ps.desc and ps.imgs_noalt==0, f"lang={ps.lang} h1={ps.h1}")
    rec("静的",f"{p}: id重複なし", len(ps.ids)==len(set(ps.ids)), str([i for i in set(ps.ids) if ps.ids.count(i)>1]))
    titles.add(ps.title); descs.add(ps.desc)
    bad=[]; absb=[]
    for l in ps.links:
        if l.startswith(("http:","https:","mailto:","#","data:")):
            if l.startswith("http"): bad.append(("外部リンクあり",l))
            continue
        if l.startswith("/"): absb.append(l); continue
        path = urlparse(l).path
        if not os.path.exists(os.path.join(ROOT, path)): bad.append(("存在しない参照", l))
    rec("静的",f"{p}: 相対参照が全て存在（リンク切れなし）", not [b for b in bad if b[0]=="存在しない参照"], str(bad))
    rec("静的",f"{p}: ルート絶対パス(/…)の参照なし", not absb, str(absb))
    rec("静的",f"{p}: 外部スクリプト/リソースを読み込まない", not [b for b in bad if b[0]=="外部リンクあり"], str(bad))
rec("静的","ページ毎にtitle/descriptionが一意", len(titles)==len(PAGES) and len(descs)==len(PAGES))
for jsf in ["main","pages","links","data/news","data/gallery","data/plugins"]:
    rc = os.system(f"node --check {ROOT}/assets/js/{jsf}.js >/dev/null 2>&1"); rec("静的",f"JS構文チェック {jsf}.js", rc==0)
css = open(ROOT+"/assets/css/style.css",encoding="utf-8").read()
rec("静的","CSSに prefers-reduced-motion 対応あり", "prefers-reduced-motion" in css)
rec("静的","CSSの括弧が対応している", css.count("{")==css.count("}"))

# ---------- ブラウザ検査 ----------
def lum(c):
    c=[x/255 for x in c]; c=[x/12.92 if x<=0.03928 else ((x+0.055)/1.055)**2.4 for x in c]; return 0.2126*c[0]+0.7152*c[1]+0.0722*c[2]
def ratio(a,b):
    la,lb=lum(a),lum(b); hi,lo=max(la,lb),min(la,lb); return (hi+0.05)/(lo+0.05)

with sync_playwright() as pw:
    br = pw.chromium.launch(); 
    os.makedirs("/tmp/shots", exist_ok=True)
    # 各ページ × 幅
    for w,h,label in [(320,640,"320px"),(390,844,"390px"),(820,1180,"タブレット820px"),(1440,900,"デスクトップ1440px")]:
        ctx = br.new_context(viewport={"width":w,"height":h}); 
        for p in PAGES:
            pg = ctx.new_page(); errs=[]; fails=[]
            pg.on("console", lambda m, e=errs: e.append(m.text) if m.type in ("error","warning") else None)
            pg.on("pageerror", lambda x, e=errs: e.append(str(x)))
            pg.on("requestfailed", lambda r, f=fails: f.append(r.url))
            pg.on("response", lambda r, f=fails: f.append(f"{r.status} {r.url}") if r.status>=400 else None)
            pg.goto(BASE+p+".html", wait_until="networkidle")
            ov = pg.evaluate("document.documentElement.scrollWidth - window.innerWidth")
            rec("レスポンシブ",f"{label} {p}: 横スクロールなし", ov<=0, f"overflow={ov}px")
            if w==1440:
                rec("コンソール",f"{p}: JSエラー/警告・リソース読込失敗なし", not errs and not fails, str(errs+fails))
            if p in ("index","join","rules-faq") and w in (320,1440):
                pg.screenshot(path=f"/tmp/shots/{p}-{w}.png", full_page=True)
            pg.close()
        ctx.close()
    # ---- 機能テスト（デスクトップ） ----
    ctx = br.new_context(viewport={"width":1440,"height":900}, permissions=["clipboard-read","clipboard-write"])
    pg = ctx.new_page(); pg.goto(BASE+"index.html", wait_until="networkidle")
    cur = pg.evaluate("[...document.querySelectorAll('.sidebar a[aria-current]')].map(a=>a.getAttribute('href'))")
    rec("ナビ","現在のページに aria-current が付く（index）", cur==["index.html"], str(cur))
    pos = pg.evaluate("getComputedStyle(document.querySelector('.sidebar')).position+' '+Math.round(document.querySelector('.sidebar').getBoundingClientRect().left)")
    rec("ナビ","PCでサイドバーが左側に表示される", pos.startswith("sticky 0"), pos)
    ok=True
    for p in PAGES:
        pg.goto(BASE+p+".html"); hrefs=pg.evaluate("[...document.querySelectorAll('.sidebar .nav a')].map(a=>a.getAttribute('href'))")
        ok = ok and hrefs==[x+".html" for x in PAGES[:1]+["about","plugins","join","news","recruitment","rules-faq","gallery"]]
        pg.goto(BASE+p+".html")
    rec("ナビ","全ページでサイドバーのリンク構成が同一", ok)
    # リンクを実際にクリックして遷移＋戻る/進む
    pg.goto(BASE+"index.html"); pg.click(".sidebar a[href='about.html']"); pg.wait_for_load_state()
    a1 = pg.url.endswith("about.html"); pg.go_back(); b1 = pg.url.endswith("index.html"); pg.go_forward(); c1 = pg.url.endswith("about.html")
    rec("ナビ","リンククリック遷移・戻る・進むが動作", a1 and b1 and c1, pg.url)
    # テーマ
    pg.goto(BASE+"index.html"); 
    t0 = pg.evaluate("document.documentElement.dataset.theme")
    pg.click(".sidebar [data-theme-toggle]"); t1 = pg.evaluate("document.documentElement.dataset.theme")
    pr = pg.get_attribute(".sidebar [data-theme-toggle]","aria-pressed")
    rec("テーマ","切り替えで data-theme が変わり aria-pressed が更新", t0!=t1 and pr==("true" if t1=="dark" else "false"), f"{t0}->{t1}, pressed={pr}")
    pg.goto(BASE+"about.html"); t2 = pg.evaluate("document.documentElement.dataset.theme")
    rec("テーマ","選択がlocalStorageで他ページにも保持される", t2==t1, t2)
    for th in ("light","dark"):
        pg.evaluate(f"document.documentElement.setAttribute('data-theme','{th}')")
        cs = pg.evaluate("""()=>{const q=s=>{const e=document.querySelector(s);const c=getComputedStyle(e);return [c.color,c.backgroundColor]};
          return {body:[getComputedStyle(document.body).color,getComputedStyle(document.body).backgroundColor], btn:q('.sidebar .nav a'), side:getComputedStyle(document.querySelector('.sidebar')).backgroundColor}}""")
        parse=lambda s:[int(x) for x in re.findall(r"\d+",s)[:3]]
        r1 = ratio(parse(cs["body"][0]),parse(cs["body"][1]))
        rec("テーマ",f"{th}モード 本文コントラスト比 ≥ 4.5", r1>=4.5, f"{r1:.1f}:1")
    # OS配色（初回）
    c2 = br.new_context(color_scheme="dark"); p2=c2.new_page(); p2.goto(BASE+"index.html")
    rec("テーマ","OSダーク設定のとき初期表示がダーク", p2.evaluate("document.documentElement.dataset.theme")=="dark"); c2.close()
    # localStorage不可でも動作
    c3 = br.new_context(); p3=c3.new_page(); p3.add_init_script("Object.defineProperty(window,'localStorage',{get(){throw new Error('blocked')}})")
    e3=[]; p3.on("pageerror", lambda x: e3.append(str(x))); p3.goto(BASE+"index.html"); p3.click(".sidebar [data-theme-toggle]")
    rec("テーマ","localStorage利用不可でもエラーなく切り替え可能", not e3 and p3.evaluate("document.documentElement.dataset.theme") in ("light","dark"), str(e3)); c3.close()
    # 未設定リンク
    pg.goto(BASE+"index.html")
    d = pg.evaluate("[...document.querySelectorAll('[data-link]')].map(a=>[a.getAttribute('href'),a.getAttribute('aria-disabled'),a.textContent.trim()])")
    rec("リンク","未設定の外部リンクは href なし・aria-disabled・準備中表示", d and all(x[0] is None and x[1]=="true" and "準備中" in x[2] for x in d), str(d))
    # 設定済みリンク（links.js を差し替えて検証）
    c4 = br.new_context(); p4=c4.new_page()
    p4.route("**/assets/js/links.js", lambda r: r.fulfill(content_type="text/javascript", body='window.SITE_LINKS={discord:"https://discord.gg/test-invite",contact:"https://forms.example/contact",recruit:"javascript:alert(1)"};'))
    p4.goto(BASE+"recruitment.html")
    dd = p4.evaluate("[...document.querySelectorAll('[data-link]')].map(a=>[a.dataset.link,a.getAttribute('href'),a.getAttribute('target'),a.getAttribute('rel')])")
    dmap = {x[0]:x for x in dd}
    rec("リンク","設定済みURLは有効化され target=_blank rel=noopener noreferrer", dmap["discord"][1]=="https://discord.gg/test-invite" and dmap["discord"][2]=="_blank" and "noopener" in dmap["discord"][3], str(dmap["discord"]))
    rec("リンク","https以外（javascript:等）は無効のまま", dmap["recruit"][1] is None, str(dmap["recruit"])); c4.close()
    # 参加方法：コピー
    pg.goto(BASE+"join.html")
    st = pg.evaluate("[...document.querySelectorAll('[data-copy-btn]')].map(b=>b.disabled)")
    rec("コピー","接続情報が未設定のとき、全てのコピーボタンが無効", st and all(st), str(st))
    pg.evaluate("navigator.clipboard.writeText('SENTINEL')"); pg.evaluate("[...document.querySelectorAll('[data-copy-btn]')].forEach(b=>b.click())")
    rec("コピー","未設定ボタンをクリックしてもクリップボードは変化しない", pg.evaluate("navigator.clipboard.readText()")=="SENTINEL")
    rec("コピー","未設定の項目に「準備中」が表示される", pg.evaluate("[...document.querySelectorAll('[data-info] .val')].every(v=>v.textContent==='準備中')"))
    c5 = br.new_context(permissions=["clipboard-read","clipboard-write"]); p5=c5.new_page()
    p5.route("**/join.html", lambda r: r.fulfill(content_type="text/html", body=r.fetch().text().replace('javaAddress: "",','javaAddress: "play.test.invalid",').replace('bedrockPort: "",','bedrockPort: "19132",')))
    p5.goto(BASE+"join.html"); 
    rows = p5.evaluate("[...document.querySelectorAll('[data-info]')].map(r=>[r.dataset.info,r.querySelector('.val').textContent,r.querySelector('button')?r.querySelector('button').disabled:null])")
    rm = {r[0]:r for r in rows}
    rec("コピー","設定済み項目のみボタン有効、未設定は無効のまま", rm["javaAddress"][2]==False and rm["bedrockPort"][2]==False and rm["bedrockAddress"][2]==True, str(rows))
    p5.click("[data-info=javaAddress] button"); p5.wait_for_timeout(200)
    rec("コピー","設定済みアドレスがクリップボードにコピーされる", p5.evaluate("navigator.clipboard.readText()")=="play.test.invalid")
    rec("コピー","コピー成功の通知が表示される", "コピーしました" in p5.inner_text(".toast"))
    c5.close()
    # Clipboard API なし → フォールバック
    c6 = br.new_context(); p6=c6.new_page()
    p6.route("**/join.html", lambda r: r.fulfill(content_type="text/html", body=r.fetch().text().replace('javaAddress: "",','javaAddress: "play.test.invalid",')))
    p6.add_init_script("Object.defineProperty(navigator,'clipboard',{value:undefined});document.execCommand=function(){window.__fb=true;return true}")
    p6.goto(BASE+"join.html"); p6.click("[data-info=javaAddress] button"); p6.wait_for_timeout(200)
    rec("コピー","Clipboard API 非対応時は execCommand にフォールバック", p6.evaluate("window.__fb===true")); c6.close()
    # FAQ
    pg.goto(BASE+"rules-faq.html")
    b = pg.locator(".acc-btn").first; pid=b.get_attribute("aria-controls")
    s0 = (b.get_attribute("aria-expanded"), pg.locator("#"+pid).is_hidden())
    b.click(); s1 = (b.get_attribute("aria-expanded"), pg.locator("#"+pid).is_visible())
    b.click(); s2 = (b.get_attribute("aria-expanded"), pg.locator("#"+pid).is_hidden())
    rec("FAQ","クリックで開閉し aria-expanded が連動", s0==("false",True) and s1==("true",True) and s2==("false",True), str((s0,s1,s2)))
    b.focus(); pg.keyboard.press("Enter"); k1=b.get_attribute("aria-expanded"); pg.keyboard.press("Space"); k2=b.get_attribute("aria-expanded")
    rec("FAQ","キーボード（Enter/Space）で開閉できる", k1=="true" and k2=="false", f"{k1},{k2}")
    c7 = br.new_context(java_script_enabled=False); p7=c7.new_page(); p7.goto(BASE+"rules-faq.html")
    rec("FAQ","JS無効でも回答が閲覧できる（全文表示）", p7.locator(".acc-panel").first.is_visible()); c7.close()
    # トップへ戻る
    pg.goto(BASE+"index.html"); v0 = pg.locator("#top-btn").is_visible()
    pg.evaluate("window.scrollTo(0,1500)"); pg.wait_for_timeout(400); v1=pg.locator("#top-btn").is_visible()
    pg.click("#top-btn"); pg.wait_for_timeout(1200); y=pg.evaluate("window.pageYOffset")
    rec("トップへ戻る","スクロール後に表示され、押すと先頭へ戻る", (not v0) and v1 and y==0, f"{v0},{v1},y={y}")
    # 空データ表示
    for p,ids in [("news",["news-empty","news-list"]),("gallery",["gallery-empty","gallery-list"]),("plugins",["plugin-empty","plugin-list"])]:
        pg.goto(BASE+p+".html"); rec("空データ",f"{p}: データ空で「準備中/なし」表示、崩れなし", pg.locator("#"+ids[0]).is_visible() and pg.evaluate("document.documentElement.scrollWidth<=innerWidth"))
    pg.goto(BASE+"index.html"); rec("空データ","トップ: お知らせ空の表示・プラグイン準備中表示", "お知らせはまだありません" in pg.inner_text("#home-news") and "準備中" in pg.inner_text("#home-plugins-count"))
    # 開設状況
    txt = pg.inner_text(".status"); rec("未確定情報","トップのサーバー状況が「開設準備中」でプレイヤー数等がない", "開設準備中" in txt and not re.search(r"\d+\s*(人|players|/)",txt), txt.replace("\n"," "))
    allt = ""
    for p in PAGES: pg.goto(BASE+p+".html"); allt += pg.inner_text("body")
    rec("未確定情報","全ページにIPアドレス形式・discord.gg URL・架空数値(オンライン○人)がない", not re.search(r"\b\d{1,3}(\.\d{1,3}){3}\b|discord\.gg|オンライン\s*\d|\d+\s*人がオンライン",allt))
    ctx.close()
    # ---- データ投入テスト ----
    NEWS = 'window.NEWS_CATEGORIES=["お知らせ","イベント"];window.NEWS_DATA=[{id:"a",date:"2026-01-01",category:"お知らせ",title:"古い告知",body:"alpha本文"},{id:"b",date:"2026-03-01",category:"イベント",title:"新しいイベント",body:"beta本文"},{id:"c",date:"2026-02-01",category:"お知らせ",title:"中間の告知",body:"gamma"},{id:"d",date:"2026-04-01",category:"お知らせ",title:"<b>XSS</b>",body:"x"}];'
    ctx = br.new_context(viewport={"width":390,"height":844}); pg = ctx.new_page()
    pg.route("**/data/news.js", lambda r: r.fulfill(content_type="text/javascript", body=NEWS))
    pg.goto(BASE+"news.html")
    order = pg.eval_on_selector_all("#news-list h3","e=>e.map(x=>x.textContent)")
    rec("お知らせ","新しい順に表示される", order[:3]==["<b>XSS</b>","新しいイベント","中間の告知"], str(order))
    rec("お知らせ","本文のHTMLは実行されず文字として表示（XSS対策）", pg.locator("#news-list b").count()==0)
    pg.fill("#news-q","beta"); n1=pg.locator("#news-list > li").count(); c1=pg.inner_text("#news-count")
    pg.fill("#news-q","存在しない語"); n2=pg.locator("#news-list > li").count(); e2=pg.locator("#news-empty").is_visible()
    pg.click("#news-clear"); n3=pg.locator("#news-list > li").count()
    rec("お知らせ","キーワード検索・件数表示・該当なし表示・クリア", n1==1 and "1 件" in c1 and n2==0 and e2 and n3==4, f"{n1},{c1},{n2},{e2},{n3}")
    pg.select_option("#news-cat","イベント"); n4=pg.locator("#news-list > li").count()
    rec("お知らせ","カテゴリ絞り込み", n4==1)
    pg.goto(BASE+"index.html"); rec("お知らせ","トップに最新3件を表示", pg.locator("#home-news > li").count()==3)
    G='window.GALLERY_CATEGORIES=["サバイバル","建築"];window.GALLERY_DATA=[{id:"1",title:"A",description:"d",category:"建築",image:"assets/images/gallery/none.png",alt:"x"},{id:"2",title:"B",description:"d",category:"サバイバル"}];'
    pg2 = ctx.new_page(); pg2.route("**/data/gallery.js", lambda r: r.fulfill(content_type="text/javascript", body=G)); pg2.goto(BASE+"gallery.html"); pg2.wait_for_timeout(300)
    tot=pg2.locator("#gallery-list > li").count(); pg2.click(".chip:has-text('建築')"); one=pg2.locator("#gallery-list > li").count()
    pr = pg2.get_attribute(".chip:has-text('建築')","aria-pressed")
    pg2.click(".chip:has-text('サバイバル')"); pg2.click(".chip:has-text('すべて')"); back=pg2.locator("#gallery-list > li").count()
    rec("ギャラリー","カテゴリ絞り込み・全表示・aria-pressed", tot==2 and one==1 and pr=="true" and back==2, f"{tot},{one},{pr},{back}")
    try: pg2.wait_for_function("document.querySelectorAll('#gallery-list .placeholder').length===2", timeout=3000)
    except Exception: pass
    rec("ギャラリー","画像の読み込み失敗・画像なしでも「準備中」表示でレイアウト維持", pg2.locator("#gallery-list .placeholder").count()==2 and pg2.evaluate("document.documentElement.scrollWidth<=innerWidth"))
    PL='window.PLUGIN_CATEGORIES=["便利機能","経済"];window.PLUGINS_DATA=[{id:"t",name:"テストプラグインA",category:"便利機能",status:"導入済み",summary:"要約",commands:[{command:"/testa",description:"説明"}]},{id:"u",name:"テストプラグインB",category:"経済",status:"導入予定",summary:"x"}];'
    pg3 = ctx.new_page(); pg3.route("**/data/plugins.js", lambda r: r.fulfill(content_type="text/javascript", body=PL)); pg3.goto(BASE+"plugins.html")
    a=pg3.locator("#plugin-list > li").count(); pg3.fill("#plugin-q","プラグインB"); b_=pg3.locator("#plugin-list > li").count(); pg3.fill("#plugin-q",""); pg3.select_option("#plugin-cat","便利機能"); c_=pg3.locator("#plugin-list > li").count()
    rec("プラグイン","一覧・検索・カテゴリ絞り込み", (a,b_,c_)==(2,1,1), str((a,b_,c_)))
    rec("プラグイン","コマンド表が表示される", pg3.locator("#plugin-list code").first.inner_text()=="/testa" if c_ else False)
    rec("プラグイン","スマホ幅でコマンド表があっても横スクロールなし", pg3.evaluate("document.documentElement.scrollWidth<=innerWidth"))
    ctx.close()
    # ---- モバイルメニュー ----
    ctx = br.new_context(viewport={"width":390,"height":844}); pg = ctx.new_page(); pg.goto(BASE+"index.html")
    vis0 = pg.locator("#sidebar").is_visible()
    pg.click("#menu-btn"); pg.wait_for_timeout(450)
    vis1 = pg.locator("#sidebar").is_visible(); ex = pg.get_attribute("#menu-btn","aria-expanded")
    foc = pg.evaluate("document.activeElement.closest('#sidebar')!==null")
    size = pg.evaluate("Math.round(document.querySelector('#menu-btn').getBoundingClientRect().height)")
    rec("モバイルメニュー","初期は閉じ、ボタンで開く（aria-expanded連動・フォーカス移動）", (not vis0) and vis1 and ex=="true" and foc, f"{vis0},{vis1},{ex},{foc}")
    rec("モバイルメニュー","メニューボタンのタップ領域 ≥ 44px", size>=44, f"{size}px")
    for _ in range(14): pg.keyboard.press("Tab")
    rec("モバイルメニュー","開いている間はTabフォーカスがメニュー内に留まる", pg.evaluate("document.activeElement.closest('#sidebar')!==null"))
    pg.keyboard.press("Escape"); pg.wait_for_timeout(450)
    rec("モバイルメニュー","Escapeで閉じ、フォーカスがボタンに戻る", (not pg.locator("#sidebar").is_visible()) and pg.evaluate("document.activeElement.id")=="menu-btn")
    pg.click("#menu-btn"); pg.wait_for_timeout(450); pg.mouse.click(380,400); pg.wait_for_timeout(450)
    rec("モバイルメニュー","メニュー外（オーバーレイ）クリックで閉じる", not pg.locator("#sidebar").is_visible())
    pg.click("#menu-btn"); pg.wait_for_timeout(450); pg.click("#sidebar a[href='join.html']"); pg.wait_for_load_state()
    rec("モバイルメニュー","メニュー内リンクで遷移できる", pg.url.endswith("join.html"))
    pg.click("#menu-btn"); pg.wait_for_timeout(450); pg.screenshot(path="/tmp/shots/menu-open-390.png")
    pg.set_viewport_size({"width":1300,"height":800}); pg.wait_for_timeout(450)
    rec("モバイルメニュー","PC幅へ拡大するとメニューが閉じ、サイドバーが常時表示", (not pg.evaluate("document.body.classList.contains('menu-open')")) and pg.locator("#sidebar").is_visible())
    ctx.close()
    # 動きを減らす
    ctx = br.new_context(reduced_motion="reduce"); pg = ctx.new_page(); pg.goto(BASE+"index.html"); 
    an = pg.evaluate("getComputedStyle(document.querySelector('.hero-art .bear')).animationName")
    rec("アクセシビリティ","prefers-reduced-motion でアニメーションが停止", an=="none", an); ctx.close()
    # Edge
    try:
        be = pw.chromium.launch(channel="msedge"); be.close(); rec("ブラウザ","Microsoft Edge で実行", True)
    except Exception as e:
        R.append(("ブラウザ","Microsoft Edge での確認","BLOCKED","この環境にEdgeがありません"))
    br.close()
srv.shutdown(); shutil.rmtree(tmp, ignore_errors=True)
cnt={}
for a,n,s,d in R: cnt[s]=cnt.get(s,0)+1
json.dump(R, open("/tmp/test_results.json","w"), ensure_ascii=False, indent=1)
for a,n,s,d in R: print(f"[{s}] {a} | {n}" + (f"  -> {d}" if s!="PASS" and d else ""))
print(cnt); sys.exit(1 if cnt.get("FAIL") else 0)
