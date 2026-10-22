# 検証レポート（TEST_REPORT）

実施日：2026-10-22 ／ 実施環境：Linuxコンテナ内の Chromium 141（Playwright・ヘッドレス）、Node.js v22（JS構文チェック）

検証対象は `/shirokuma-site/` というサブパス配下にローカル配信したサイトです。**実際の GitHub Pages 上での検証ではありません。**

## 結果サマリー

| 区分 | 件数 | 内容 |
|---|---|---|
| PASS | 145 | 自動テストで実際に実施し成功 |
| FAIL | 0 | 最終実行で失敗なし（経緯は下記「修正内容」） |
| BLOCKED | 2 | Edge、GitHub Pages実環境（下記） |
| NOT RUN | 4 | 実機・スクリーンリーダー等（下記） |

再実行：サイト直下で `python3 tests/run_tests.py`（要 Python + Playwright + Chromium）。

## 実施できなかったテスト

| 区分 | 項目 | 理由 |
|---|---|---|
| BLOCKED | Microsoft Edge での表示確認 | 環境にEdgeがない。Chromium（Chrome系エンジン）のみで実施 |
| BLOCKED | 実際の GitHub Pages 公開環境での確認 | ネットワーク不可・リポジトリ未作成。サブパス配信のローカル再現のみ |
| NOT RUN | iPhone / Android 実機での確認 | 実機なし（画面幅のエミュレーションのみ） |
| NOT RUN | スクリーンリーダー（NVDA / VoiceOver 等）での読み上げ確認 | 未実施 |
| NOT RUN | 設定済みの Discord / フォームURLへの実際の遷移 | URL未確定（`target`・`rel` 属性の付与のみテスト済み） |
| NOT RUN | 全ページ・全幅の目視レビュー、Lighthouse | 目視確認はホーム（PC・320px）と参加方法（320px）のみ |

## 修正内容

1. 初回実行で FAIL 1件（ギャラリーの画像読み込み失敗時の「準備中」表示）。原因は、画像エラーが非同期で発生するのにテストが待たずに判定していた**テスト側の問題**。待機を追加して再実行し PASS（サイト側の修正なし）。
2. 目視確認でトップのヒーロー見出しが1文字だけ折り返す問題を発見。見出しサイズと `text-wrap: balance` を調整し、再撮影で解消を確認。
3. デザインを企業サイト調に刷新（CSSのみ変更）。変更後に自動テスト全件（145件）を再実行し、すべてPASS。目視確認はトップのPC幅のみ再実施。

## テスト詳細（自動テスト：すべて実施・結果は下表）

### 静的

| 結果 | テスト項目 | 備考 |
|---|---|---|
| PASS | ページ存在 index.html |  |
| PASS | index: lang=ja / h1が1つ / titleとdescriptionあり / img alt |  |
| PASS | index: id重複なし |  |
| PASS | index: 相対参照が全て存在（リンク切れなし） |  |
| PASS | index: ルート絶対パス(/…)の参照なし |  |
| PASS | index: 外部スクリプト/リソースを読み込まない |  |
| PASS | ページ存在 about.html |  |
| PASS | about: lang=ja / h1が1つ / titleとdescriptionあり / img alt |  |
| PASS | about: id重複なし |  |
| PASS | about: 相対参照が全て存在（リンク切れなし） |  |
| PASS | about: ルート絶対パス(/…)の参照なし |  |
| PASS | about: 外部スクリプト/リソースを読み込まない |  |
| PASS | ページ存在 plugins.html |  |
| PASS | plugins: lang=ja / h1が1つ / titleとdescriptionあり / img alt |  |
| PASS | plugins: id重複なし |  |
| PASS | plugins: 相対参照が全て存在（リンク切れなし） |  |
| PASS | plugins: ルート絶対パス(/…)の参照なし |  |
| PASS | plugins: 外部スクリプト/リソースを読み込まない |  |
| PASS | ページ存在 join.html |  |
| PASS | join: lang=ja / h1が1つ / titleとdescriptionあり / img alt |  |
| PASS | join: id重複なし |  |
| PASS | join: 相対参照が全て存在（リンク切れなし） |  |
| PASS | join: ルート絶対パス(/…)の参照なし |  |
| PASS | join: 外部スクリプト/リソースを読み込まない |  |
| PASS | ページ存在 news.html |  |
| PASS | news: lang=ja / h1が1つ / titleとdescriptionあり / img alt |  |
| PASS | news: id重複なし |  |
| PASS | news: 相対参照が全て存在（リンク切れなし） |  |
| PASS | news: ルート絶対パス(/…)の参照なし |  |
| PASS | news: 外部スクリプト/リソースを読み込まない |  |
| PASS | ページ存在 recruitment.html |  |
| PASS | recruitment: lang=ja / h1が1つ / titleとdescriptionあり / img alt |  |
| PASS | recruitment: id重複なし |  |
| PASS | recruitment: 相対参照が全て存在（リンク切れなし） |  |
| PASS | recruitment: ルート絶対パス(/…)の参照なし |  |
| PASS | recruitment: 外部スクリプト/リソースを読み込まない |  |
| PASS | ページ存在 rules-faq.html |  |
| PASS | rules-faq: lang=ja / h1が1つ / titleとdescriptionあり / img alt |  |
| PASS | rules-faq: id重複なし |  |
| PASS | rules-faq: 相対参照が全て存在（リンク切れなし） |  |
| PASS | rules-faq: ルート絶対パス(/…)の参照なし |  |
| PASS | rules-faq: 外部スクリプト/リソースを読み込まない |  |
| PASS | ページ存在 gallery.html |  |
| PASS | gallery: lang=ja / h1が1つ / titleとdescriptionあり / img alt |  |
| PASS | gallery: id重複なし |  |
| PASS | gallery: 相対参照が全て存在（リンク切れなし） |  |
| PASS | gallery: ルート絶対パス(/…)の参照なし |  |
| PASS | gallery: 外部スクリプト/リソースを読み込まない |  |
| PASS | ページ毎にtitle/descriptionが一意 |  |
| PASS | JS構文チェック main.js |  |
| PASS | JS構文チェック pages.js |  |
| PASS | JS構文チェック links.js |  |
| PASS | JS構文チェック data/news.js |  |
| PASS | JS構文チェック data/gallery.js |  |
| PASS | JS構文チェック data/plugins.js |  |
| PASS | CSSに prefers-reduced-motion 対応あり |  |
| PASS | CSSの括弧が対応している |  |

### レスポンシブ

| 結果 | テスト項目 | 備考 |
|---|---|---|
| PASS | 320px index: 横スクロールなし |  |
| PASS | 320px about: 横スクロールなし |  |
| PASS | 320px plugins: 横スクロールなし |  |
| PASS | 320px join: 横スクロールなし |  |
| PASS | 320px news: 横スクロールなし |  |
| PASS | 320px recruitment: 横スクロールなし |  |
| PASS | 320px rules-faq: 横スクロールなし |  |
| PASS | 320px gallery: 横スクロールなし |  |
| PASS | 390px index: 横スクロールなし |  |
| PASS | 390px about: 横スクロールなし |  |
| PASS | 390px plugins: 横スクロールなし |  |
| PASS | 390px join: 横スクロールなし |  |
| PASS | 390px news: 横スクロールなし |  |
| PASS | 390px recruitment: 横スクロールなし |  |
| PASS | 390px rules-faq: 横スクロールなし |  |
| PASS | 390px gallery: 横スクロールなし |  |
| PASS | タブレット820px index: 横スクロールなし |  |
| PASS | タブレット820px about: 横スクロールなし |  |
| PASS | タブレット820px plugins: 横スクロールなし |  |
| PASS | タブレット820px join: 横スクロールなし |  |
| PASS | タブレット820px news: 横スクロールなし |  |
| PASS | タブレット820px recruitment: 横スクロールなし |  |
| PASS | タブレット820px rules-faq: 横スクロールなし |  |
| PASS | タブレット820px gallery: 横スクロールなし |  |
| PASS | デスクトップ1440px index: 横スクロールなし |  |
| PASS | デスクトップ1440px about: 横スクロールなし |  |
| PASS | デスクトップ1440px plugins: 横スクロールなし |  |
| PASS | デスクトップ1440px join: 横スクロールなし |  |
| PASS | デスクトップ1440px news: 横スクロールなし |  |
| PASS | デスクトップ1440px recruitment: 横スクロールなし |  |
| PASS | デスクトップ1440px rules-faq: 横スクロールなし |  |
| PASS | デスクトップ1440px gallery: 横スクロールなし |  |

### コンソール

| 結果 | テスト項目 | 備考 |
|---|---|---|
| PASS | index: JSエラー/警告・リソース読込失敗なし |  |
| PASS | about: JSエラー/警告・リソース読込失敗なし |  |
| PASS | plugins: JSエラー/警告・リソース読込失敗なし |  |
| PASS | join: JSエラー/警告・リソース読込失敗なし |  |
| PASS | news: JSエラー/警告・リソース読込失敗なし |  |
| PASS | recruitment: JSエラー/警告・リソース読込失敗なし |  |
| PASS | rules-faq: JSエラー/警告・リソース読込失敗なし |  |
| PASS | gallery: JSエラー/警告・リソース読込失敗なし |  |

### ナビ

| 結果 | テスト項目 | 備考 |
|---|---|---|
| PASS | 現在のページに aria-current が付く（index） |  |
| PASS | PCでサイドバーが左側に表示される |  |
| PASS | 全ページでサイドバーのリンク構成が同一 |  |
| PASS | リンククリック遷移・戻る・進むが動作 |  |

### テーマ

| 結果 | テスト項目 | 備考 |
|---|---|---|
| PASS | 切り替えで data-theme が変わり aria-pressed が更新 |  |
| PASS | 選択がlocalStorageで他ページにも保持される |  |
| PASS | lightモード 本文コントラスト比 ≥ 4.5 |  |
| PASS | darkモード 本文コントラスト比 ≥ 4.5 |  |
| PASS | OSダーク設定のとき初期表示がダーク |  |
| PASS | localStorage利用不可でもエラーなく切り替え可能 |  |

### リンク

| 結果 | テスト項目 | 備考 |
|---|---|---|
| PASS | 未設定の外部リンクは href なし・aria-disabled・準備中表示 |  |
| PASS | 設定済みURLは有効化され target=_blank rel=noopener noreferrer |  |
| PASS | https以外（javascript:等）は無効のまま |  |

### コピー

| 結果 | テスト項目 | 備考 |
|---|---|---|
| PASS | 接続情報が未設定のとき、全てのコピーボタンが無効 |  |
| PASS | 未設定ボタンをクリックしてもクリップボードは変化しない |  |
| PASS | 未設定の項目に「準備中」が表示される |  |
| PASS | 設定済み項目のみボタン有効、未設定は無効のまま |  |
| PASS | 設定済みアドレスがクリップボードにコピーされる |  |
| PASS | コピー成功の通知が表示される |  |
| PASS | Clipboard API 非対応時は execCommand にフォールバック |  |

### FAQ

| 結果 | テスト項目 | 備考 |
|---|---|---|
| PASS | クリックで開閉し aria-expanded が連動 |  |
| PASS | キーボード（Enter/Space）で開閉できる |  |
| PASS | JS無効でも回答が閲覧できる（全文表示） |  |

### トップへ戻る

| 結果 | テスト項目 | 備考 |
|---|---|---|
| PASS | スクロール後に表示され、押すと先頭へ戻る |  |

### 空データ

| 結果 | テスト項目 | 備考 |
|---|---|---|
| PASS | news: データ空で「準備中/なし」表示、崩れなし |  |
| PASS | gallery: データ空で「準備中/なし」表示、崩れなし |  |
| PASS | plugins: データ空で「準備中/なし」表示、崩れなし |  |
| PASS | トップ: お知らせ空の表示・プラグイン準備中表示 |  |

### 未確定情報

| 結果 | テスト項目 | 備考 |
|---|---|---|
| PASS | トップのサーバー状況が「開設準備中」でプレイヤー数等がない |  |
| PASS | 全ページにIPアドレス形式・discord.gg URL・架空数値(オンライン○人)がない |  |

### お知らせ

| 結果 | テスト項目 | 備考 |
|---|---|---|
| PASS | 新しい順に表示される |  |
| PASS | 本文のHTMLは実行されず文字として表示（XSS対策） |  |
| PASS | キーワード検索・件数表示・該当なし表示・クリア |  |
| PASS | カテゴリ絞り込み |  |
| PASS | トップに最新3件を表示 |  |

### ギャラリー

| 結果 | テスト項目 | 備考 |
|---|---|---|
| PASS | カテゴリ絞り込み・全表示・aria-pressed |  |
| PASS | 画像の読み込み失敗・画像なしでも「準備中」表示でレイアウト維持 |  |

### プラグイン

| 結果 | テスト項目 | 備考 |
|---|---|---|
| PASS | 一覧・検索・カテゴリ絞り込み |  |
| PASS | コマンド表が表示される |  |
| PASS | スマホ幅でコマンド表があっても横スクロールなし |  |

### モバイルメニュー

| 結果 | テスト項目 | 備考 |
|---|---|---|
| PASS | 初期は閉じ、ボタンで開く（aria-expanded連動・フォーカス移動） |  |
| PASS | メニューボタンのタップ領域 ≥ 44px |  |
| PASS | 開いている間はTabフォーカスがメニュー内に留まる |  |
| PASS | Escapeで閉じ、フォーカスがボタンに戻る |  |
| PASS | メニュー外（オーバーレイ）クリックで閉じる |  |
| PASS | メニュー内リンクで遷移できる |  |
| PASS | PC幅へ拡大するとメニューが閉じ、サイドバーが常時表示 |  |

### アクセシビリティ

| 結果 | テスト項目 | 備考 |
|---|---|---|
| PASS | prefers-reduced-motion でアニメーションが停止 |  |

### ブラウザ

| 結果 | テスト項目 | 備考 |
|---|---|---|
| BLOCKED | Microsoft Edge での確認 | この環境にEdgeがありません |

## 実施方法メモ

- 幅 320 / 390 / 820 / 1440px で全8ページを読み込み、横スクロール有無を計測。
- コンソールのエラー・警告、HTTP 400以上、読み込み失敗リクエストを収集（1440px時）。
- お知らせ・ギャラリー・プラグイン・接続情報・リンクの「設定済み」状態は、テスト内でデータファイルを一時的に差し替えて検証（実ファイルは空のまま）。
- 静的検査：相対参照の存在確認、`/` 始まりの絶対パスの不使用、外部リソース非読み込み、id重複、h1の数、`lang`、title/descriptionの一意性。
