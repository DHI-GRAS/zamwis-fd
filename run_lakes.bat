set "DATA_DIR=%~dp0\data"

set "LAKES_DIR=%DATA_DIR%\lakes"

call %~dp0\update\update_lakes.bat && call %~dp0\import\import_lakes.bat
