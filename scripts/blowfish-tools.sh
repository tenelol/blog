#!/usr/bin/env bash

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
config_dir="$repo_root/config/_default"

ja_language="$config_dir/languages.ja.toml"
en_language="$config_dir/languages.en.toml"
ja_menu="$config_dir/menus.ja.toml"
en_menu="$config_dir/menus.en.toml"

created_en_language=0
created_en_menu=0

cleanup() {
  if [[ -f "$en_language" ]]; then
    cp "$en_language" "$ja_language"
  fi

  if [[ -f "$en_menu" ]]; then
    cp "$en_menu" "$ja_menu"
  fi

  if [[ $created_en_language -eq 1 ]]; then
    rm -f "$en_language"
  fi

  if [[ $created_en_menu -eq 1 ]]; then
    rm -f "$en_menu"
  fi
}

trap cleanup EXIT

if [[ ! -f "$ja_language" ]]; then
  echo "Missing $ja_language" >&2
  exit 1
fi

if [[ ! -f "$ja_menu" ]]; then
  echo "Missing $ja_menu" >&2
  exit 1
fi

if [[ ! -f "$en_language" ]]; then
  cp "$ja_language" "$en_language"
  created_en_language=1
fi

if [[ ! -f "$en_menu" ]]; then
  cp "$ja_menu" "$en_menu"
  created_en_menu=1
fi

cd "$repo_root"

if command -v blowfish-tools >/dev/null 2>&1; then
  blowfish-tools "$@"
  exit $?
fi

if [[ "${1:-}" == "config" ]]; then
  shift
  nix shell nixpkgs#hugo -c npx blowfish-tools "$@"
  exit $?
fi

nix shell nixpkgs#hugo -c npx blowfish-tools "$@"
