+++
title = "自宅 NixOS サーバーを公開するときに Cloudflare Tunnel と Tailscale をどう分けるか"
date = 2026-06-21T23:10:00+09:00
draft = false
summary = "自宅 NixOS サーバーを公開・運用するとき、Cloudflare Tunnel と Tailscale を同じ用途で混ぜず、公開用と管理用に分ける考え方を整理します。"
description = "自宅 NixOS サーバーを公開・運用するとき、Cloudflare Tunnel と Tailscale を公開用と管理用に分ける判断軸を整理します。"
tags = ["NixOS", "Cloudflare", "Tailscale", "Self-hosting"]
categories = ["Blog"]
+++

## 背景

自宅や小さな VPS で NixOS サーバーを運用するとき、最初に迷うのは「どこまでをインターネットに出すか」だと思う。

Cloudflare Tunnel を使えば、公開 IP や自宅回線のポート開放なしで HTTP サービスを外に出せる。Tailscale を使えば、SSH や管理画面を tailnet の中に閉じたまま扱える。どちらも便利なので、役割を決めないまま混ぜると、後から「この経路は誰に開いているのか」が分かりにくくなる。

自分の中では、まず次の分け方にするのが扱いやすい。

| 用途 | 使うもの | 理由 |
| --- | --- | --- |
| 公開したい Web サービス | Cloudflare Tunnel | public hostname と HTTP 入口を Cloudflare 側で管理しやすい |
| SSH / deploy / 管理画面 | Tailscale | tailnet の ACL と SSH policy で管理用経路を閉じやすい |
| NixOS の更新 | Tailscale 経由の SSH | `nixos-rebuild --target-host` の入口を public に出さずに済む |
| 直接ポート開放 | 原則避ける | 例外を増やすと運用の説明が難しくなる |

## Cloudflare Tunnel に寄せるもの

Cloudflare Tunnel は、`cloudflared` が Cloudflare 側へ outbound 接続を張り、その tunnel に public hostname を紐付ける構成になる。Cloudflare の docs でも、公開 IP なしでリソースを Cloudflare に接続する方式として説明されている。

この性質上、公開ブログ、小さな Web UI、Webhook endpoint のように「インターネットから HTTP で来てほしいもの」は Cloudflare Tunnel に寄せると考えやすい。

逆に、SSH や管理画面を何でも Tunnel で出すと、公開用の経路と管理用の経路が同じ場所に集まりすぎる。Cloudflare Access などで守る選択肢はあるが、最初の設計としては「公開 HTTP だけ」と決めておく方が見通しがよい。

参考:

- [Cloudflare Tunnel docs](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/)
- [Set up Cloudflare Tunnel](https://developers.cloudflare.com/tunnel/setup/)
- [Cloudflare Tunnel routing](https://developers.cloudflare.com/tunnel/routing/)

## Tailscale に寄せるもの

Tailscale は管理用の private network として扱う。SSH、deploy、監視の internal dashboard、DB の管理 UI など、普段は自分だけが触るものは tailnet 内に閉じる。

Tailscale SSH を使う場合、SSH の認証と認可を Tailscale 側で管理できる。さらに ACL / grants や tags を使うと、どの端末・どのユーザーがどのサーバーへ入れるかを宣言的に扱える。

ここで大事なのは、Tailscale を「便利な VPN」として雑に全許可しないことだと思う。サーバーには `tag:server`、管理端末には `tag:admin-device` のような役割を付け、SSH policy は必要な組み合わせだけにする。

参考:

- [Tailscale SSH](https://tailscale.com/docs/features/tailscale-ssh)
- [Tailscale ACLs](https://tailscale.com/docs/features/access-control/acls)
- [Tailscale policy file syntax](https://tailscale.com/docs/reference/syntax/policy-file)
- [Tailscale tags](https://tailscale.com/docs/features/tags)

## NixOS の remote deploy は Tailscale 経由にする

NixOS は remote deploy と相性がよい。`nixos-rebuild` には remote host へ切り替えるための `--target-host` があり、公式 NixOS Wiki でも remote host へ deploy する使い方が説明されている。

この SSH の入口を public Internet に出す必要はない。Tailscale 経由で名前解決できるなら、deploy 側は tailnet の中だけで完結できる。

```sh
nixos-rebuild switch \
  --flake .#server \
  --target-host user@server \
  --sudo
```

実際の運用では、local で build して target に送るのか、build host を別にするのかも決める必要がある。小さいサーバーなら local build、大きいサーバーなら remote build の方が楽なこともある。ここはハードウェアと cache の状況で変わる。

参考:

- [nixos-rebuild - Official NixOS Wiki](https://wiki.nixos.org/wiki/Nixos-rebuild)

## 最初の設計ルール

最初から複雑にしないなら、この4つだけ決める。

1. public hostname が必要な HTTP だけ Cloudflare Tunnel に出す。
2. SSH、deploy、管理画面は Tailscale に閉じる。
3. Tailscale ACL は全許可ではなく、tag と役割で分ける。
4. 例外的に public に出した管理系 endpoint は、理由と期限をメモする。

この分け方にしておくと、後から構成を見直すときに「これは公開面なのか、管理面なのか」を判断しやすい。

## 失敗しやすいところ

Cloudflare Tunnel と Tailscale の両方を入れると、接続経路は増える。便利になる一方で、障害時に「DNS なのか、Tunnel なのか、tailnet なのか、NixOS の service なのか」を切り分ける必要がある。

そのため、まずは1サービスずつ公開する。Tunnel に出すサービスは public hostname と backend port を控える。Tailscale 側は ACL と SSH policy の意図を残す。NixOS の module には「なぜこの port を listen しているのか」が分かる名前を付ける。

## まとめ

Cloudflare Tunnel と Tailscale は競合というより、役割が違う道具として分けると使いやすい。

Cloudflare Tunnel は public な HTTP 入口。Tailscale は private な管理経路。NixOS の remote deploy は Tailscale 側に寄せる。この3つを守るだけでも、自宅サーバーの公開と運用はかなり説明しやすくなる。

次にやるなら、この方針を NixOS module に落として、`cloudflared`、`tailscale`、対象 service の単位で「どの経路に出ているか」が分かる形にしておきたい。
