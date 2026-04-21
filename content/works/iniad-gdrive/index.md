+++
title = "iniad-gdrive"
date = 2026-04-21T14:25:00+09:00
draft = false
summary = "INIAD-oriented Google Drive import wrapper for gdrive and mygdrive"
description = "INIAD の Google Drive から授業資料や課題ファイルをローカルへ取り込むための CLI。"
featureimage = "https://opengraph.githubassets.com/f725e4e6d9d6381c1a2fa6401510496e7f09d340c6389eb63fd4f3c782c45d34/tenelol/iniad-gdrive"
tags = ["JavaScript", "CLI", "INIAD"]
categories = ["Works"]
featured = true
repo = "https://github.com/tenelol/iniad-gdrive"
stack = ["Node.js", "Google Drive API", "CLI", "OAuth"]
highlight = "学内 Drive の取得手順を `setup` / `auth` / `doctor` / `search` / `import` に整理し、曖昧な手作業を CLI に落とし込んだ。"
+++

INIAD 向けに、Google Drive からの取得作業を扱いやすくする import ラッパーです。URL、file ID、query のどこからでも始められるようにし、授業資料フォルダを起点に安全に絞り込めるようにしています。

## URL

- [GitHub Repository](https://github.com/tenelol/iniad-gdrive)

## Overview

Google の desktop OAuth loopback flow を使い、学内向けの Drive import を CLI としてまとめたプロジェクトです。初回セットアップ、認証、疎通確認、検索、ファイル取り込みまでを分けて、AI エージェントや普段の CLI 利用からつなげやすい形にしています。

## Focus

- `gdrive` / `mygdrive` の操作を目的別にまとめる
- 学内向けの運用を CLI に落とし込む
- 手動作業のばらつきを減らして再利用しやすくする

## Stack

- Node.js
- Google Drive API
- OAuth
- CLI
