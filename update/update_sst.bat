setlocal enableextensions

if not defined SST_DIR (exit /b -1)
if not defined EXPORT_DIR_SST (exit /b -1)

set "SST_FILE=%SST_DIR%\SST.nc"

set SST_EXTENT="25,37,-20,-8"

REM set DOWNLOAD_START="--startdate=20160101"
REM set DOWNLOAD_END="--enddate=20160201"
REM set NO_DELETE="--no-delete"

call activate fd

call flooddrought download_sst --extent %SST_EXTENT% %SST_FILE% %DOWNLOAD_START% %DOWNLOAD_END% %NO_DELETE%
call flooddrought save_timeslice_geotiff %SST_FILE% %EXPORT_DIR_SST%

endlocal
