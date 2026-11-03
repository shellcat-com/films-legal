#!/usr/bin/env bash
# Rebuild assets/looks/<presetID>.png from the iOS app's own FilmLook math.
# Each PNG is a 33³ colour cube laid out as a 1089×33 strip: x = blue·33 + red,
# y = green (sRGB primaries + sRGB transfer, 8-bit). join.html applies it with
# WebGL (viewfinder + saved photo). Needs Xcode's swiftc and the app checkout.
#   APP=~/Camera scripts/looks/build.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
APP="${APP:-$HOME/Camera}"
S="$APP/Camera/Core"
TMP="$(mktemp -d)"
swiftc -O -o "$TMP/gen" "$ROOT/scripts/looks/stub.swift" "$S/FilmLook.swift" "$S/FilmLookLibrary.swift" "$S/LookStages.swift" "$ROOT/scripts/looks/gen-luts.swift"
"$TMP/gen" "$ROOT/assets/looks" 33
rm -f "$ROOT/assets/looks/stages.json"   # stage numbers are copied into join.html's LOOKS table by hand
rm -rf "$TMP"
echo "LUTs written to $ROOT/assets/looks"
