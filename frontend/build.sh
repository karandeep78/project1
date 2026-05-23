#!/usr/bin/env sh
set -e
cd "$(dirname "$0")"
rm -rf static
cp -r ../static ./static
if [ -n "$PHISH_API_URL" ]; then
  printf '%s\n' "window.PHISH_API_URL = '${PHISH_API_URL}';" > js/config.js
fi
