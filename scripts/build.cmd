@echo off

setlocal

set "ROOT_DIR=%~dp0\..\"
set "DIST_DIR=pyinstaller-dist"
set "BUILD_DIR=pyinstaller-build"
set "SPEC_FILE=build.spec"

cd /d "%ROOT_DIR%"

pyinstaller --distpath "%DIST_DIR%" --workpath "%BUILD_DIR%" -y --clean "%SPEC_FILE%"
