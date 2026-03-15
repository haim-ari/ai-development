#!/usr/bin/env bash
# Sets up a new repo with the same base environment as ai-developers.
# Usage: ../ai-developers/init-repo.sh

set -e
BASE_DIR="$(cd "$(dirname "$0")" && pwd)"

for f in devbox.json devbox.lock .envrc .gitignore .env.example check_setup.py requirements.in requirements.txt; do
  cp "$BASE_DIR/$f" .
done

echo "Done. Run: direnv allow"
