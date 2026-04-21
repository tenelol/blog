+++
title = ".dotfiles"
date = 2026-04-21T14:22:00+09:00
draft = false
summary = "Personal dotfiles with denix"
description = "NixOS と nix-darwin を 1 つの flake で管理する、`denix` ベースの multi-host dotfiles。"
featureimage = "https://opengraph.githubassets.com/5c5d7e9c6fdbbe3eb12706b7d06917dcabf8d4d2b9a8af4b0d55be518d56a7f9/tenelol/.dotfiles"
tags = ["Nix", "dotfiles", "nix-darwin"]
categories = ["Works"]
featured = true
repo = "https://github.com/tenelol/.dotfiles"
stack = ["Nix", "nix-darwin", "Home Manager", "denix"]
highlight = "NixOS と macOS を単一 flake で扱い、host 差分を薄く保ったまま個人環境を継続運用している。"
+++

`denix` ベースで組んでいる個人用の multi-host dotfiles です。NixOS と `nix-darwin` を 1 つの flake で管理し、Home Manager は各 system に統合しています。

## URL

- [GitHub Repository](https://github.com/tenelol/.dotfiles)

## Overview

単なる設定置き場ではなく、複数ホストをどう分けるか、どこまで共通化するか、GUI / CLI をどう切り分けるかまで含めて継続運用している repo です。`hosts`、`modules`、`rices` を薄く保ち、`denix` の自動発見前提で構造を揃えています。

## Focus

- `nix-darwin` を含む multi-host 構成
- host 固有差分を `modules` 側へ寄せた薄い定義
- 個人利用に最適化しつつも再現性を崩さない運用

## Stack

- Nix
- nix-darwin
- Home Manager
- denix
