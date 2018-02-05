set "DATA_DIR=%~dp0\data"
set "EXPORT_DIR=%DATA_DIR%\export"

set "SWI_DIR=%DATA_DIR%\SWI"
set "EXPORT_DIR_SWI=%EXPORT_DIR%\SWI"

call update\update_swi.bat && call import\import_swi.bat
