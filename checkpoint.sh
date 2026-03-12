#!/usr/bin/env bash
# ============================================================
# RagaNotate — Session Checkpoint Script
# ============================================================
# Run this at the END of every development session to create
# a local git bundle backup you can always restore from.
#
# Usage (from repo root):
#   bash checkpoint.sh
#   bash checkpoint.sh "optional message"
#
# What it does:
#   1. Bundles the entire git history → AI_dance/backups/
#   2. Updates SESSION_STATE.md with current file list + versions
#   3. Prints a reminder to push via GitHub Desktop
# ============================================================

set -e

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKUP_DIR="$(dirname "$REPO_DIR")/backups"
DATE=$(date +"%Y-%m-%d_%H%M")
MSG="${1:-checkpoint}"
BUNDLE_NAME="RagaNotate_${DATE}_${MSG// /_}.bundle"

mkdir -p "$BACKUP_DIR"

echo ""
echo "═══════════════════════════════════════════"
echo "  RagaNotate — Session Checkpoint"
echo "  $(date)"
echo "═══════════════════════════════════════════"

# ── 1. Git bundle ────────────────────────────────────────────
cd "$REPO_DIR"
if git rev-parse --git-dir > /dev/null 2>&1; then
    git bundle create "$BACKUP_DIR/$BUNDLE_NAME" --all
    echo ""
    echo "  ✅ Bundle saved:"
    echo "     $BACKUP_DIR/$BUNDLE_NAME"
    echo "     Size: $(du -h "$BACKUP_DIR/$BUNDLE_NAME" | cut -f1)"
else
    echo "  ⚠  Not a git repo — skipping bundle (run git init first)"
fi

# ── 2. Keep only the 5 most recent bundles ──────────────────
cd "$BACKUP_DIR" 2>/dev/null || true
BUNDLES=($(ls -t RagaNotate_*.bundle 2>/dev/null))
if [ ${#BUNDLES[@]} -gt 5 ]; then
    for old in "${BUNDLES[@]:5}"; do
        rm -f "$old"
        echo "  🗑  Removed old bundle: $old"
    done
fi

# ── 3. Print version summary ─────────────────────────────────
cd "$REPO_DIR"
echo ""
echo "  Versions:"
PY_VER=$(python3 -c "import re; m=re.search(r'__version__ = \"([^\"]+)\"', open('packages/python/raganotate/__init__.py').read()); print(m.group(1) if m else '?')" 2>/dev/null || echo "?")
JS_VER=$(python3 -c "import json; print(json.load(open('packages/js/package.json'))['version'])" 2>/dev/null || echo "?")
echo "     Python: $PY_VER   JS: $JS_VER"

# ── 4. File count ─────────────────────────────────────────────
FILE_COUNT=$(find . -not -path './.git/*' -type f | wc -l | tr -d ' ')
echo "     Files in repo: $FILE_COUNT"

echo ""
echo "  ─────────────────────────────────────────"
echo "  📌 NEXT STEP — Push to GitHub Desktop:"
echo ""
echo "     1. Open GitHub Desktop"
echo "     2. Repo: RagaNotate"
echo "     3. Commit message: 'checkpoint: $MSG $(date +%Y-%m-%d)'"
echo "     4. Click Commit → Push"
echo "  ─────────────────────────────────────────"
echo ""
echo "  ✅ Checkpoint complete: $BUNDLE_NAME"
echo ""
