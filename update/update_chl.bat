setlocal enableextensions

if not defined CHL_DIR (exit /b -1)
if not defined EXPORT_DIR_CHL (exit /b -1)

set "CHL_FILE=%CHL_DIR%\CHL.nc"

set CHL_EXTENT="25,37,-20,-8"

REM set DOWNLOAD_START="--startdate=20160101"
REM set DOWNLOAD_END="--enddate=20160201"
REM set NO_DELETE="--no-delete"

call activate fd

call flooddrought download_chlorophyll --extent %CHL_EXTENT% %CHL_FILE% %DOWNLOAD_START% %DOWNLOAD_END% %NO_DELETE%
call flooddrought save_timeslice_geotiff %CHL_FILE% %EXPORT_DIR_CHL%

endlocal
