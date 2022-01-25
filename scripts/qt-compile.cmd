@echo off

setlocal

set "ROOT_DIR=%~dp0\..\"

cd /d "%ROOT_DIR%"

pyside6-uic --from-imports -o "eternal_radio_player/gui/generated/main_window.py" "resources/gui/main-window.ui"
pyside6-rcc -o "eternal_radio_player/gui/generated/resources_rc.py" "resources/gui/resources.qrc"
