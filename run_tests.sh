#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$PROJECT_ROOT/.venv"

if [[ ! -d "$VENV_DIR" ]]; then
  echo "Virtual environment not found at $VENV_DIR" >&2
  exit 1
fi

source "$VENV_DIR/bin/activate"

PYTHONPATH="$PROJECT_ROOT" pytest -q || {
  echo "Tests failed" >&2
  exit 1
}

echo "All tests passed"
exit 0


