set "DATA_DIR=%~dp0\data"
set "EXPORT_DIR=%DATA_DIR%\export"

set "CHL_DIR=%DATA_DIR%\CHL"
set "EXPORT_DIR_CHL=%EXPORT_DIR%\CHL"

call %~dp0\update\update_chl.bat && call %~dp0\import\import_chl.bat
