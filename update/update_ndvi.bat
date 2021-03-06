setlocal enableextensions

if not defined NDVI_DIR (exit /b -1)
if not defined EXPORT_DIR_NDVI (exit /b -1)

set "NDVI_FILE=%NDVI_DIR%\NDVI.nc"

set NDVI_EXTENT="18.375,36.55,-20.525,-8.975"

REM set DOWNLOAD_START="--startdate=20160101"
REM set DOWNLOAD_END="--enddate=20160201"
REM set NO_DELETE="--no-delete"

call activate fd

call flooddrought download_ndvi --extent %NDVI_EXTENT% %NDVI_FILE% %DOWNLOAD_START% %DOWNLOAD_END% %NO_DELETE%
call flooddrought update_longterm_statistics %NDVI_FILE%
call flooddrought calculate_ndvi_indices %NDVI_FILE%
call flooddrought save_timeslice_geotiff %NDVI_FILE% %EXPORT_DIR_NDVI%
call flooddrought save_timeslice_geotiff %NDVI_DIR%\indices\*anomaly*.nc %EXPORT_DIR_NDVI%\anomaly

endlocal