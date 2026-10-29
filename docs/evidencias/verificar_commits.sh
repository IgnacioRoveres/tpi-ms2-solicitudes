#!/usr/bin/env bash
# Corre el golden master (tests de caracterizacion actuales) contra el
# programa de cada commit, desde estado-inicial hasta HEAD.
# Uso: bash docs/evidencias/verificar_commits.sh
set -u
raiz=$(git rev-parse --show-toplevel)
tmp=$(mktemp -d)
printf "| Commit | Mensaje | Golden master |\n| --- | --- | --- |\n"
for c in $(git rev-list --reverse estado-inicial^..HEAD); do
  git -C "$raiz" worktree add -q --detach "$tmp/$c" "$c" >/dev/null 2>&1
  res=$(cd "$raiz" && SGSA_PROGRAMA="$tmp/$c/sistema.py" python3 -m pytest -q -p no:cacheprovider tests/caracterizacion 2>&1 | tail -1)
  printf "| %s | %s | %s |\n" "$(git log -1 --format=%h "$c")" "$(git log -1 --format=%s "$c")" "$res"
  git -C "$raiz" worktree remove --force "$tmp/$c"
done
rm -rf "$tmp"
