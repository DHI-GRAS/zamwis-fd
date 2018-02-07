setlocal enableextensions

if not defined ET_DIR (exit /b -1)
if not defined EXPORT_DIR_ET (exit /b -1)

set "ET_FILE=%ET_DIR%\ET.nc"

set ET_EXTENT="16.325,38.675,-21.725,-7.775"

REM set DOWNLOAD_START="--startdate=20160101"
REM set DOWNLOAD_END="--enddate=20160201"

call activate fd

call flooddrought download_et --extent %ET_EXTENT% %ET_FILE% %DOWNLOAD_START% %DOWNLOAD_END%
call flooddrought update_monthly_statistics %ET_FILE%
call flooddrought save_timeslice_geotiff %ET_FILE% %EXPORT_DIR_ET%

endlocal
