+++
title = "Neovim と macSKK の Ctrl-J 問題を skkeleton に逃がした話"
date = 2026-05-26T18:22:20+09:00
draft = true
summary = "Neovim で Ctrl-J を使いたくて macSKK の入力ソース制御を試した結果、IME 状態と辞書まわりを壊しかけたので skkeleton に分離した記録。"
description = "Neovim、macSKK、macOS の入力ソース切り替えが衝突したときの症状、原因、最終的に skkeleton へ逃がした対応をまとめます。"
tags = ["Neovim", "SKK", "macOS", "Nix"]
categories = ["Blog"]
+++

## 背景

Neovim では `Ctrl-J` を下方向のウィンドウ移動に使っている。

ところが macSKK を使っていると、`Ctrl-J` が SKK 側のひらがな切り替えとして扱われてしまい、Neovim のキーマップまで届かないことがあった。やりたかったのは単純で、Neovim の中では `Ctrl-J` を普通に使い、日本語も必要なときだけ打てるようにすることだった。

## 何が起きたか

最初は macOS の入力ソースを Neovim のモードに合わせて切り替える方向で試した。

insert mode に入ったら macSKK の英字、normal mode に戻ったら別の入力ソース、toggleterm でも同じように切り替える、という形にした。

一見よさそうに見えたが、実際にはかなり不安定だった。

- `Ctrl-J` が期待通り Neovim に届かない
- `きょう` を打とうとすると `きょ` が消えて `u` だけ残る
- 普通の語句が変換できなくなる
- macOS の入力ソース一覧に macSKK の項目が大量に出る
- 再起動しないと日本語入力自体が戻らない状態になる

この時点で、Neovim の設定だけの問題ではなく、macSKK や macOS の入力ソース状態まで巻き込んでいた。

## 原因

大きな原因は、Neovim 側から macSKK を細かく制御しようとしすぎたことだった。

`macism` で insert、normal、terminal の出入りごとに macSKK の入力ソースを強制的に選び直していた。SKK は変換途中の状態を持つ IME なので、その最中に入力ソースを切り替えると内部状態が壊れやすい。

`きょう` の途中で `u` だけ残るような症状は、この入力ソース切り替えが変換中のローマ字入力を途中でリセットしていたのが原因だと思う。

さらに悪かったのは、macSKK の辞書や plist まわりまで Nix activation から触ろうとしたことだった。macSKK の GUI が想定している設定形式や内部状態とずれると、変換品質そのものが壊れる。普通の単語が変換できなくなったのは、このあたりを自動化しすぎた影響が大きい。

## 対応

最終的には、Neovim の中で macSKK を使うのをやめた。

Neovim にフォーカスがある間は macOS の入力ソースを `ABC` に固定する。これで `Ctrl-J` は macSKK に奪われず、Neovim のキーマップとして処理できる。

日本語入力は Neovim 内の `skkeleton` に任せることにした。`skkeleton` は denops 上で動く SKK 実装で、Neovim の insert mode、cmdline、terminal mode から使える。

いまの構成では、`<C-\>` で `skkeleton` を toggle する。

- normal mode の `Ctrl-J` は下方向移動
- toggleterm の `Ctrl-J` もウィンドウ移動
- 日本語入力は `<C-\>` で `skkeleton` を有効化
- macOS 側の IME は Neovim 中では `ABC`
- Neovim からフォーカスが外れたら、元の入力ソースへ戻す

辞書は Neovim 側では Nix の `SKK-JISYO.L` を使う。macSKK の辞書設定とは分けた。

## 学び

IME は状態を持つので、エディタのモード遷移と同期して外から頻繁に切り替えるのは危ない。

特に SKK のように、ローマ字入力、変換途中、候補選択、ユーザー辞書更新が絡むものは、外部ツールで入力ソースを叩くと簡単に壊れる。

今回の教訓はかなり単純だった。

- Neovim 内の問題は、できるだけ Neovim 内で閉じる
- OS IME の辞書や plist は automation で触らない
- macOS の入力ソース制御は最小限にする
- `Ctrl-J` のような制御キーは IME に渡さない設計にする

macSKK は macOS 全体の日本語入力として使い、Neovim 内では `skkeleton` を使う。この分離が一番安定した。

## まとめ

最初は macSKK の英字モードをうまく使えば解決すると思っていた。

でも実際には、Neovim のモード切り替えと macSKK の内部状態を同期させるのはかなり無理があった。結果として、`Ctrl-J` 問題だけでなく、日本語入力そのものや辞書設定まで不安定になった。

最終的には、Neovim 内では macOS IME を `ABC` に固定し、日本語入力は `skkeleton` に分離する形にした。OS の IME を無理に操作するより、責務を分けた方が安定する。
