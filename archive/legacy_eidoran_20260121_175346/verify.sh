#!/usr/bin/env bash
set -euo pipefail

# Eidoran repo integrity check.
# Verifies SHA-256 hashes listed in RELEASES.md against files in the current directory.
# Works on Linux/macOS (requires bash + either sha256sum or shasum).

cd "$(dirname "$0")"

# Collect checksum lines (ignore comments/blank lines).
mapfile -t lines < <(grep -E '^[0-9a-f]{64}  ' RELEASES.md || true)

if [[ "${#lines[@]}" -eq 0 ]]; then
  echo "No checksum lines found in RELEASES.md"
  exit 2
fi

# Prefer sha256sum if available.
if command -v sha256sum >/dev/null 2>&1; then
  printf "%s
" "${lines[@]}" | sha256sum -c -
  exit 0
fi

# Fallback to shasum (macOS).
if command -v shasum >/dev/null 2>&1; then
  status=0
  while IFS= read -r line; do
    hash="${line%%  *}"
    file="${line#*  }"
    if [[ ! -f "$file" ]]; then
      echo "$file: MISSING"
      status=1
      continue
    fi
    got="$(shasum -a 256 "$file" | awk '{print $1}')"
    if [[ "$got" == "$hash" ]]; then
      echo "$file: OK"
    else
      echo "$file: FAILED"
      echo "  expected: $hash"
      echo "  got:      $got"
      status=1
    fi
  done < <(printf "%s
" "${lines[@]}")
  exit $status
fi

echo "No sha256 tool found. Install 'coreutils' (sha256sum) or use macOS 'shasum'."
exit 2
