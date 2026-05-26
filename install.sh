#!/usr/bin/env bash
set -e
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Installing Fern-Multi from $ROOT"

for dep in python3 bash nmap; do
  if ! command -v "$dep" >/dev/null 2>&1; then
    echo "Error: $dep is required but not installed."
    exit 1
  fi
done

chmod +x "$ROOT/Fern-Multi/Fern-Multi-tool.py"
chmod +x "$ROOT/Fern-Multi/HTTP_SERV/HTTP_SERV.py"
find "$ROOT/Fern-Multi" -type f \( -name '*.sh' -o -name '*.py' \) -exec chmod +x {} +

echo
if [ -f "$ROOT/README.md" ]; then
  echo "Installation complete."
  echo "Run the tool with:"
  echo "  python3 \"$ROOT/Fern-Multi/Fern-Multi-tool.py\""
else
  echo "Installation complete."
fi
