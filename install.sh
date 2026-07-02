#!/bin/bash
# git-vibes install — 現在のリポジトリに pre-commit スタンプフックを入れる
set -euo pipefail

GIT_DIR="$(git rev-parse --git-dir 2>/dev/null)" || {
  echo "error: not inside a git repository" >&2
  exit 1
}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOK_PATH="$GIT_DIR/hooks/pre-commit"

if [[ -f "$HOOK_PATH" ]]; then
  echo "warning: $HOOK_PATH already exists. back up and overwrite? (y/N)"
  read -r ans
  [[ "$ans" == "y" || "$ans" == "Y" ]] || { echo "aborted"; exit 1; }
  cp "$HOOK_PATH" "$HOOK_PATH.bak.$(date +%s)"
fi

cat > "$HOOK_PATH" <<EOF
#!/bin/bash
python3 "$SCRIPT_DIR/stamp.py"
exit 0
EOF
chmod +x "$HOOK_PATH"
echo "installed: $HOOK_PATH -> $SCRIPT_DIR/stamp.py"
echo "try: git commit -m 'test' (or run 'python3 $SCRIPT_DIR/fortune.py' anytime)"
