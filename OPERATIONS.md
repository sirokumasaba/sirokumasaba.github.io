# 運用ガイド（初心者向け）

編集は GitHub の画面（ファイルを開く → 鉛筆アイコン ✏️ → 編集 → 「Commit changes」）だけでできます。反映まで数分かかります。
**注意：** `"` と `,` を消さないでください。間違えるとその部分が表示されなくなります。

---

## 1. Discord招待URLを変更する

ファイル：`assets/js/links.js`

```js
window.SITE_LINKS = {
  discord: "https://discord.gg/ここに招待コード",
  contact: "",
  recruit: ""
};
```
`https://` で始まるURLを入れると、全ページ（サイドバー・ヒーロー・フッター）のDiscordボタンが自動で有効になります。空 `""` に戻すと「準備中」表示に戻ります。

## 2. サーバーアドレス・ポート・バージョンを変更する

ファイル：`join.html` の下の方にある `window.SERVER_INFO`

```js
window.SERVER_INFO = {
  javaAddress: "play.example.com",   // Java版アドレス
  bedrockAddress: "play.example.com", // 統合版アドレス
  bedrockPort: "19132",              // 統合版ポート
  version: "1.21 以降",              // 対応バージョン
  notes: "接続に関する注意事項"
};
```
設定した項目だけが表示され、「コピー」ボタンが使えるようになります。空のままの項目は「準備中」になります。
**統合版の対応状況が確認できるまで、統合版の項目は空のままにしてください。** 統合版の手順の上にある注意書き（`join.html` の「統合版からの接続可否は…」）も、対応が確定したら書き換えてください。
トップページ（`index.html`）の「サーバー状況」の「準備中」「開設準備中」は文字を直接書き換えます（`status` クラスの部分）。

## 3. お知らせを追加・編集・削除する

ファイル：`assets/js/data/news.js`

追加：`window.NEWS_DATA = [` と `];` の間に1件ずつ書きます（最後の `}` の後ろにカンマ）。
```js
window.NEWS_DATA = [
  { id: "2026-05-01-open", date: "2026-05-01", category: "お知らせ",
    title: "公式サイトを公開しました", body: "本文です。\n2行目はこのように書きます。" },
  { id: "2026-05-10-event", date: "2026-05-10", category: "イベント",
    title: "イベント開催", body: "詳細はDiscordで。" }
];
```
- `date` は `年-月-日`（半角）。新しい順に自動で並びます。
- `category` は `window.NEWS_CATEGORIES` に書いたものから選ぶと絞り込みに出ます。カテゴリ名は同じ行で自由に変更できます。
- 編集は該当の文字を直すだけ、削除は `{ ... },` の1件分を丸ごと消します。
- ホームには最新3件が自動で表示されます。

## 4. ギャラリー画像を追加・変更する／ 8. Minecraftスクリーンショットを追加する

1. 画像（`.png` / `.jpg` / `.webp`）を `assets/images/gallery/` にアップロードします（目安：横1600px以下、1枚1MB以下）。
2. `assets/js/data/gallery.js` に追記します。
```js
window.GALLERY_DATA = [
  { id: "g1", title: "拠点の全景", description: "みんなで作った拠点です。",
    category: "建築", image: "assets/images/gallery/base.png", alt: "拠点の全景のスクリーンショット" }
];
```
`category` は「サバイバル／建築／イベント／ミニゲーム」から選びます（`window.GALLERY_CATEGORIES` で変更可）。**実際のスクリーンショットだけ**を登録してください。

参加方法ページの手順画像は、`assets/images/guide/` に画像を置き、`join.html` の「スクリーンショット準備中」の `<div class="placeholder ...">…</div>` を次のように置き換えます。
```html
<img src="assets/images/guide/java-1.png" alt="マルチプレイを選ぶ画面" style="border:2px solid #12263a">
```

## 5. 募集人数・仕事内容を変更する

ファイル：`recruitment.html`。`約3名` や `<li>…</li>` の文字を直接書き換えます。応募条件・年齢・活動時間・選考基準・権限は、現在「要確認（未確定）」です。決まったら、その表の文字を書き換えてください。

## 6. 問い合わせ・応募フォームのURLを変更する

ファイル：`assets/js/links.js`
```js
  contact: "https://forms.gle/お問い合わせフォーム",
  recruit: "https://forms.gle/応募フォーム"
```
設定すると、フッター・トップ・スタッフ募集ページのボタンが自動で有効になり、外部サイトが新しいタブで開きます。

## 7. ロゴ・ヒーロー画像を差し替える

- ロゴ：`assets/images/logo.png` を**同じ名前で上書き**（背景透過のPNG推奨。サイドバーは濃い紺色の背景です）。
- ファビコン：`assets/images/favicon.png` を上書き。
- ヒーロー画像：現在はCSSで描いた仮の風景です。画像に変えるときは `assets/images/hero/` に画像を置き、`assets/css/style.css` の `.hero` に `background-image: url("../images/hero/hero.png"); background-size: cover;` を追加します（文字が読めるか必ず確認してください）。

## 9. ルールやFAQを編集する

ファイル：`rules-faq.html`
- ルール：`rule("…","…")` 相当の `<article class="card rule-card">…</article>` の文章を直接編集。
- FAQ：`<div class="acc-item">…</div>` を1セットとして、質問（`<button>` の中）と回答（`<p>` の中）を書き換えます。追加するときは、`id="q9"` `aria-controls="a9"` `id="a9"` `aria-labelledby="q9"` のように**番号をそろえて**コピーしてください。
- 処罰の方針が決まったら「違反への対応について」の文を書き換えます。

## 10. GitHub Pagesへ反映する

ファイルを編集して「Commit changes」を押すだけです。数分後に公開サイトに反映されます。反映されない場合は `Ctrl + F5`。詳しくは README.md の「GitHub Pages 公開手順」を参照してください。

---

## 11. プラグイン紹介を追加する（追加ページ）

ファイル：`assets/js/data/plugins.js`
```js
window.PLUGINS_DATA = [
  {
    id: "example",
    name: "プラグイン名",
    category: "便利機能",          // PLUGIN_CATEGORIES から選ぶ
    status: "導入済み",            // 導入済み / 導入予定 / 検討中
    summary: "一行の紹介",
    description: "詳しい説明",
    features: ["できること1", "できること2"],
    commands: [ { command: "/example", description: "コマンドの説明" } ],
    notes: "注意事項"
  }
];
```
`features` `commands` `notes` は省略できます。**導入が確定したプラグインだけ**を載せてください。キーワード検索・カテゴリ絞り込みは自動で動きます。

## 色を変えたいとき

`assets/css/style.css` の先頭にある `:root { --ice: …; --grass: …; }` などの色を書き換えます（ダークモードは `[data-theme="dark"]` の部分）。
