#!/bin/bash
# スケジュールタスクから呼ばれる自動 commit & push スクリプト
# Usage: ./auto_commit_push.sh [commit_message]

set -euo pipefail

BLOG_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$BLOG_DIR"

MSG="${1:-"auto: daily blog post $(date +%Y-%m-%d)"}"

git add -A

if git diff --cached --quiet; then
    echo "No changes to commit"
    exit 0
fi

git commit -m "$MSG"
git push origin main

echo "Pushed: $MSG"
