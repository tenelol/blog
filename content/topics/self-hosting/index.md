+++
title = "自宅サーバー / Cloudflare / Tailscale"
date = 2026-06-21T23:00:00+09:00
draft = false
description = "自宅サーバー公開、Cloudflare Tunnel、Tailscale、リモート運用に関する記事の入口。"
summary = "自宅サーバー公開、Cloudflare Tunnel、Tailscale、リモート運用に関する記事の入口。"
tags = ["Self-hosting", "Cloudflare", "Tailscale"]
categories = ["Topic"]
+++

自宅サーバー公開、Cloudflare Tunnel、Tailscale、リモート運用に関する記事の入口です。

## 最初に読む

- [自宅 NixOS サーバーを公開するときに Cloudflare Tunnel と Tailscale をどう分けるか](/posts/nixos-cloudflare-tailscale-access-design/)

## Zenn に置いている関連記事

- [NixOSをCloudflare Tunnel経由でサーバー化した話](https://zenn.dev/tenelol/articles/417a294de03c5c)
- [NixOSをTailscale経由でリモートデプロイ可能にした話](https://zenn.dev/tenelol/articles/91672b444d6547)

## 判断軸

- public に見せる HTTP は Cloudflare Tunnel に寄せる
- 管理用 SSH と deploy は Tailscale に寄せる
- 直接ポート開放は最後の手段にする
