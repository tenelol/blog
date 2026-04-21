+++
title = "GitHub と Zenn を起点に、このサイトで書いていくこと"
date = 2026-04-21T14:30:00+09:00
draft = false
summary = "GitHub の個人開発と Zenn の技術記事を、このサイトでどう見せていくかを整理したメモ。"
tags = ["GitHub", "Zenn", "NixOS", "Portfolio"]
categories = ["Site"]
+++

## 背景

このサイトは、ポートフォリオと個人ブログを無理なく同居させるために作っています。

最初から全部の方向性を固めるより、すでに公開している GitHub と Zenn を起点にした方が、何を見せたいかがぶれにくいと考えました。

## GitHub で見せたいもの

- [Nixar](https://github.com/tenelol/Nixar) は `Go` と `Nix` を組み合わせた最小構成の Web フレームワークです。
- [iniad-gdrive](https://github.com/tenelol/iniad-gdrive) は INIAD 向けの Google Drive import ラッパーです。
- [.dotfiles](https://github.com/tenelol/.dotfiles) では `denix` ベースの環境管理を続けています。

コードとして見せたいものは `Works` に寄せ、サイト内では何を作ったかと、どこが面白いかが短時間で伝わる形にしていきます。

## Zenn で書いているもの

- [NixOSをCloudflare Tunnel経由でサーバー化した話](https://zenn.dev/tenelol/articles/417a294de03c5c)
- [NixOSをTailscale経由でリモートデプロイ可能にした話](https://zenn.dev/tenelol/articles/91672b444d6547)

いま公開している記事は、個人サーバー運用やリモートデプロイのような、実際に手を動かして詰まったことをまとめた内容が中心です。自分で書いた技術記事は今後も Zenn に寄せる方針にしています。

## このサイトで書くもの

- AI を使った試行
- 個人的な制作記録
- 技術記事にする前段階の設計メモ

このサイト側は、技術記事の完成版というより、思考や試行の流れが見える場所として育てていきます。

## このサイトで増やすもの

- `Works` には実装物と役割、使った技術、改善した点を整理して追加する
- `Posts` には Zenn より短い設計メモ、AI 活用メモ、個人的な記録も積み上げる
- 外部サービスに分散している活動を、このサイトから一目で追えるようにする
