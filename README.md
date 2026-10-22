# 白熊鯖 公式サイト

Minecraftサーバー「白熊鯖」の公式サイトです。HTML / CSS / Vanilla JavaScript だけで作られており、**ビルド不要・外部サービス不要**で、GitHub Pages にそのまま公開できます。

> 現在は **開設準備中** の状態です。サーバーアドレス・Discord招待URL・各種フォームURL・実際のスクリーンショットなど、未確定の情報はすべて「準備中」と表示されます（架空の情報は載せていません）。

## ページ一覧

| ファイル | ページ |
|---|---|
| `index.html` | ホーム |
| `about.html` | 白熊鯖について |
| `plugins.html` | プラグイン紹介（追加ページ） |
| `join.html` | 参加方法・接続情報 |
| `news.html` | お知らせ |
| `recruitment.html` | スタッフ募集 |
| `rules-faq.html` | ルール・FAQ |
| `gallery.html` | ギャラリー |

## ファイル構成

```text
/
├── index.html ほか 7 ページ
├── .nojekyll                  GitHub Pages用（そのまま配信するための印）
├── assets/
│   ├── css/style.css          共通スタイル（色は先頭の変数で変更可）
│   ├── js/
│   │   ├── links.js           ★ Discord / 問い合わせ / 応募フォームのURL
│   │   ├── main.js            共通機能（テーマ・メニュー・FAQ・コピー等）
│   │   ├── pages.js           ページ別の表示処理
│   │   └── data/
│   │       ├── news.js        ★ お知らせデータ
│   │       ├── gallery.js     ★ ギャラリーデータ
│   │       └── plugins.js     ★ プラグイン紹介データ
│   └── images/
│       ├── logo.png           仮のロゴ（差し替え推奨）
│       ├── favicon.png
│       ├── hero/ gallery/ guide/   画像置き場
├── tests/run_tests.py         自動テスト
├── README.md / OPERATIONS.md / TEST_REPORT.md / PRE_LAUNCH_CHECKLIST.md
```

★ が日常的に編集するファイルです。接続情報（サーバーアドレス等）は `join.html` 内の `window.SERVER_INFO` を編集します。詳しくは **OPERATIONS.md** を見てください。

## ローカルで確認する

`index.html` をブラウザで開くだけでも動きます。より本番に近い確認は次のとおりです。

```bash
python3 -m http.server 8000
# ブラウザで http://localhost:8000/ を開く
```

## 実装上の方針

- すべてのパスは**相対パス**です。`https://ユーザー名.github.io/リポジトリ名/` のようなサブパス配下でも動きます。
- 未設定のURL・接続情報は、ボタンが自動で「準備中」の無効表示になり、コピーもできません。
- プレイヤー数や稼働状況の自動取得は**未実装**です（GitHub Pagesは静的ホスティングで、サーバーの状態を取得するAPIが別途必要なため）。
- 問い合わせ・応募の送信機能もありません（バックエンドがないため）。外部フォーム（Googleフォーム等）のURLを設定して使います。
- 画像のロゴ `assets/images/logo.png` は、コードで生成した**仮のドット絵**です。正式なロゴができたら同名で差し替えてください。
- OGP画像・canonical URL は、公開URLが未確定のため設定していません（後述）。

## GitHub Pages 公開手順

1. **リポジトリを用意**：GitHub にログインし、右上の「＋」→「New repository」で新規作成（Public）。名前は自由です（例：`shirokuma-site`）。
2. **ファイルをアップロード**：リポジトリ画面で「uploading an existing file」を選び、このフォルダの**中身すべて**（`index.html`、`assets` フォルダ、`.nojekyll` など）をドラッグ＆ドロップして「Commit changes」。
   - Gitに慣れている場合：`git add . && git commit -m "公開" && git push`
   - `index.html` が**リポジトリの一番上の階層**にあることを確認してください。
3. **Pagesを有効化**：リポジトリの「Settings」→ 左メニュー「Pages」→「Build and deployment」の Source を **Deploy from a branch**、Branch を **main** / **/ (root)** にして「Save」。
4. **公開URLを確認**：数分後、同じ画面の上部に `https://ユーザー名.github.io/リポジトリ名/` と表示されます。
5. **公開後の確認**：全ページを開き、CSSが効いているか・画像が出るか・メニューが動くかを確認（PRE_LAUNCH_CHECKLIST.md 参照）。
6. **更新の反映**：ファイルを編集して「Commit changes」すると、数分で自動的に反映されます。反映されないときは `Ctrl + F5`（スマホはキャッシュ削除）。
7. **うまくいかないとき**：
   - 404 → `index.html` が最上階層にあるか／Pagesの設定が main・root か確認。
   - 見た目が崩れる → `assets` フォルダごとアップロードされているか確認。ファイル名の大文字小文字も区別されます。
   - 「Actions」タブに赤い×がないか確認。
8. **将来、独自ドメインを使う場合**：Settings → Pages → Custom domain にドメインを入力し、ドメイン側のDNSで GitHub Pages 向けの設定（CNAME / Aレコード）を行います。本サイトは相対パスなので、ドメイン変更でもファイルの修正は不要です。詳細は GitHub の公式ドキュメントを参照してください。

> GitHubのパスワードやトークンなどの秘密情報は、サイトのファイルに絶対に書かないでください。

## OGP・ファビコン・sitemapについて

- ファビコンは `assets/images/favicon.png` を使用しています。差し替えは同名で上書きしてください。
- OGP画像（SNSで共有したときの画像）は未用意です。公開URLが決まってから、各HTMLの `<head>` に次の2行を追加してください（`〇〇` は実際のURL）。
  ```html
  <meta property="og:image" content="https://〇〇/assets/images/ogp.png">
  <meta property="og:url" content="https://〇〇/">
  ```
- `sitemap.xml` / `robots.txt` は、公開URLが未確定のため作成していません。
