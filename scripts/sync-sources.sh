#!/usr/bin/env bash
# sources.txt에 등록된 study repo들을 docs/<name>/ 아래로 동기화한다.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DOCS_DIR="$ROOT_DIR/docs"
WORK_DIR="$(mktemp -d)"
trap 'rm -rf "$WORK_DIR"' EXIT

while IFS='|' read -r name url nav_title; do
  [[ -z "$name" || "$name" == \#* ]] && continue

  target="$DOCS_DIR/$name"
  clone_dir="$WORK_DIR/$name"

  git clone --depth 1 "$url" "$clone_dir"

  rm -rf "$target"
  mkdir -p "$target"
  rsync -a \
    --exclude='.venv/' --exclude='__pycache__/' --exclude='node_modules/' \
    --exclude='.git/' --exclude='*.pyc' \
    "$clone_dir/chapters" "$target/" 2>/dev/null || true
  rsync -a "$clone_dir/assets" "$target/" 2>/dev/null || true
  [[ -f "$clone_dir/GLOSSARY.md" ]] && cp "$clone_dir/GLOSSARY.md" "$target/GLOSSARY.md"
  [[ -f "$clone_dir/README.md" ]] && cp "$clone_dir/README.md" "$target/README.md"

  echo "synced $name <- $url"
done < "$ROOT_DIR/sources.txt"

python3 "$ROOT_DIR/scripts/wrap_code_files.py" "$DOCS_DIR"
