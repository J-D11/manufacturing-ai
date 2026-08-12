#!/usr/bin/env bash
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

patterns=(
  "/U""sers/"
  '[[:alnum:]._%+-]+[@][[:alnum:].-]+\.[[:alpha:]]{2,}'
  "BEGIN ""(RSA|OPENSSH|EC|DSA|PRIVATE) KEY"
  "github""_pat_"
  "gh""[opsu]_[[:alnum:]_]+"
  "AI""za[[:alnum:]_-]+"
  "sk""-[[:alnum:]_-]{16,}"
)

for pattern in "${patterns[@]}"; do
  if git grep -nEI "$pattern" -- . ':!script/privacy_check.sh'; then
    echo "Privacy check failed: tracked content contains a private path, email, or credential-like value." >&2
    exit 1
  fi
done

echo "Privacy check passed."
