#!/bin/bash
cd "$(dirname "$0")"
git push origin main
echo ""
echo "=== Push complete. You can close this window. ==="
read -p ""
