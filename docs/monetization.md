# ブログ収益化チェックリスト

この repo では、表示広告より先に、信頼できるレビュー・比較記事で収益化する。

## 計測

- Search Console verification は `config/_default/params.toml` の `params.verification.google` で設定できる。
- Google Analytics は `config/_default/hugo.toml` の `googleAnalytics` で設定できる。
- Umami は `config/_default/params.toml` の `params.umamiAnalytics.websiteid` で設定できる。
- `affiliate` / `affiliatecard` shortcode が出すリンクには `rel="sponsored noopener noreferrer"` と `data-monetization-*` 属性を付ける。
- `layouts/partials/extend-head-uncached.html` は、Umami / Google Analytics / Fathom のいずれかが設定されている場合に `affiliate_click` event を送る。

## 公開ルール

- placeholder の affiliate URL を公開しない。
- 収益リンクを含む記事では、記事上部に `{{< adnote >}}` を置く。
- affiliate link は、実際に使った、触った、または真面目に検討したものだけに使う。
- レビュー記事には欠点と向かないケースも書く。
- 継続的にメンテしない限り、固定価格の断言は避ける。

## コンテンツ軸

- NixOS and declarative infrastructure operations.
- Cloudflare, Tailscale, self-hosting, and home server operations.
- AI を使った開発ワークフロー。
- 開発者向けのデスク環境・入力デバイス。
