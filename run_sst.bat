set "DATA_DIR=%~dp0\data"
set "EXPORT_DIR=%DATA_DIR%\export"

set "SST_DIR=%DATA_DIR%\SST"
set "EXPORT_DIR_SST=%EXPORT_DIR%\SST"

call update\update_sst.bat && call import\import_sst.bat
