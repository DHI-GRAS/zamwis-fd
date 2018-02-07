set "DATA_DIR=%~dp0\data"
set "EXPORT_DIR=%DATA_DIR%\export"

set "TRMM_DIR=%DATA_DIR%\TRMM"
set "EXPORT_DIR_TRMM=%EXPORT_DIR%\TRMM"

call %~dp0\update\update_trmm.bat && call %~dp0\import\import_trmm.bat