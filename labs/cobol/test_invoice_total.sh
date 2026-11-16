#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")"
tmp_dir=$(mktemp -d)
trap 'rm -r "$tmp_dir"' EXIT HUP INT TERM
cobc -x -free -o "$tmp_dir/invoice-total" invoice_total.cbl
actual=$(printf '100.00\n10\n' | "$tmp_dir/invoice-total")
[ "$actual" = 'TOTAL=110.00' ] || { printf 'Unexpected result: %s\n' "$actual"; exit 1; }
if printf '%s\n' 'abc' '10' | "$tmp_dir/invoice-total" > "$tmp_dir/error"; then
  echo 'Invalid input was accepted' >&2
  exit 1
fi
echo 'COBOL invoice checks passed'
