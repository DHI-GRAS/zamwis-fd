set "DATA_DIR=%~dp0\data"
set "EXPORT_DIR=%DATA_DIR%\export"

set "NDVI_DIR=%DATA_DIR%\NDVI"
set "EXPORT_DIR_NDVI=%EXPORT_DIR%\NDVI"

call update\update_ndvi.bat && call import\import_ndvi.bat
