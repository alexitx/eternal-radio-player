#!/usr/bin/env bash

set -e

ROOT_DIR="$(cd "$(dirname "$0")/../" && pwd)"
DIST_DIR='pyinstaller-dist'
BUILD_DIR='pyinstaller-build'
SPEC_FILE='build.spec'

cd "$ROOT_DIR"

pyinstaller --distpath "$DIST_DIR" --workpath "$BUILD_DIR" -y --clean "$SPEC_FILE"
