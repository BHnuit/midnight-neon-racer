#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ -x "$ROOT/.venv/bin/python" ]]; then
  PY="$ROOT/.venv/bin/python"
elif [[ -x /tmp/ptest-venv/bin/python ]]; then
  PY=/tmp/ptest-venv/bin/python
else
  PY=python3
fi

if [[ -z "${PLAYWRIGHT_CHROMIUM:-}" ]]; then
  for c in \
    "$HOME/.cache/ms-playwright/chromium-1208/chrome-linux64/chrome" \
    "$HOME/.cache/ms-playwright/chromium-1169/chrome-linux64/chrome"
  do
    if [[ -x "$c" ]]; then
      export PLAYWRIGHT_CHROMIUM="$c"
      break
    fi
  done
fi

echo "using $PY  url=${RACER_URL:-https://racer.bhnuit.cn/}"
"$PY" tests/racer_test_physics.py
"$PY" tests/racer_test_ghost.py
"$PY" tests/racer_test_v3.py
