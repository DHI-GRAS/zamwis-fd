setlocal enableextensions

if not defined TRMM_DIR (exit /b -1)
if not defined EXPORT_DIR_TRMM (exit /b -1)

set "TRMM_FILE=%TRMM_DIR%\TRMM.nc"

set TRMM_EXTENT="18.375,36.5,-20.25,-8.875"

REM set DOWNLOAD_START="--startdate=20160101"
REM set DOWNLOAD_END="--enddate=20160201"
REM set NO_DELETE="--no-delete"

call activate fd

call flooddrought download_trmm --extent %TRMM_EXTENT% %TRMM_FILE% %DOWNLOAD_START% %DOWNLOAD_END% %NO_DELETE%
call flooddrought save_spi_stats %TRMM_FILE%
call flooddrought calculate_rainfall_indices %TRMM_FILE%
call flooddrought save_timeslice_geotiff %TRMM_FILE% %EXPORT_DIR_TRMM%
call flooddrought save_timeslice_geotiff %TRMM_DIR%\indices\*_1_month*.nc %EXPORT_DIR_TRMM%\1_month
call flooddrought save_timeslice_geotiff %TRMM_DIR%\indices\*_3_month*.nc %EXPORT_DIR_TRMM%\3_month
call flooddrought save_timeslice_geotiff %TRMM_DIR%\indices\*_6_month*.nc %EXPORT_DIR_TRMM%\6_month

endlocal