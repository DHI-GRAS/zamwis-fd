set "DATA_DIR=%~dp0\data"

set "LAKES_DIR=%DATA_DIR%\lakes"

call update\update_lakes.bat && call import\import_lakes.bat
