+++
title = "Nixar"
date = 2026-04-21T14:20:00+09:00
draft = false
summary = "Minimal Go web framework + Nix flake template"
description = "Go の最小 Web フレームワークと Nix flake のスタータをひとつにまとめた個人開発プロジェクト。"
featureimage = "https://opengraph.githubassets.com/ce1a09a5a63dd9739af23d7847c233a96ff37bbfb272964aff5a276184658c6c/tenelol/Nixar"
tags = ["Go", "Nix", "Framework"]
categories = ["Works"]
featured = true
repo = "https://github.com/tenelol/Nixar"
stack = ["Go", "Nix", "net/http", "HTML"]
highlight = "Go の最小構成フレームワークに `flake.nix` テンプレートを同梱し、開発開始までの摩擦を減らした。"
+++

`Go` と `Nix` を組み合わせた最小構成の Web フレームワークです。`net/http` ベースで小さく保ちつつ、ルーティング、ミドルウェア、JSON / HTML helper、静的ファイル配信を用意しています。

## URL

- [GitHub Repository](https://github.com/tenelol/Nixar)

## Overview

最小の Go Web フレームワークと、`nix flake init` で始められるテンプレートを同じ repo にまとめています。サンプルサーバーや NixOS module も含めて、試作から運用寄りの利用まで見通せる構成にしています。

## Focus

- 小さく始められる Web 実装の土台
- `Nix flake` を含めた再現性のある開発開始点
- フレームワーク自体を学習の足場にする設計

## Stack

- Go
- Nix
- `net/http`
- NixOS module
