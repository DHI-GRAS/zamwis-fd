SETLOCAL ENABLEEXTENSIONS
SET PARENT=%~dp0

set NDVI_EXTENT="18.375,36.55,-20.525,-8.975"
set SWI_EXTENT="18.3,36.5,-20.4,-8.9"
set TRMM_EXTENT="18.375,36.5,-20.25,-8.875"

REM set DOWNLOAD_START="--startdate=20160101"
REM set DOWNLOAD_END="--enddate=20160201"

set "NDVI_DIR=%PARENT%\NDVI"
set "SWI_DIR=%PARENT%\SWI"
set "TRMM_DIR=%PARENT%\TRMM"

set "NDVI_FILE=%NDVI_DIR%\NDVI.nc"
set "SWI_FILE=%SWI_DIR%\SWI.nc"
set "TRMM_FILE=%TRMM_DIR%\TRMM.nc"

set "EXPORT_DIR=%PARENT%\export"
set "EXPORT_DIR_NDVI=%EXPORT_DIR%\NDVI"
set "EXPORT_DIR_SWI=%EXPORT_DIR%\SWI"
set "EXPORT_DIR_TRMM=%EXPORT_DIR%\TRMM"

call activate fd

call flooddrought download_ndvi --extent %NDVI_EXTENT% %NDVI_FILE% %DOWNLOAD_START% %DOWNLOAD_END% --no-delete
call flooddrought update_longterm_statistics %NDVI_FILE%
call flooddrought calculate_ndvi_indices %NDVI_FILE%
call flooddrought save_timeslice_geotiff %NDVI_FILE% %EXPORT_DIR_NDVI%
call flooddrought save_timeslice_geotiff %NDVI_FILE%\indices\*anomaly*.nc %EXPORT_DIR_NDVI%\anomaly

call flooddrought download_swi --product SWI --extent %SWI_EXTENT% %SWI_FILE% %DOWNLOAD_START% %DOWNLOAD_END% --no-delete
call flooddrought update_longterm_statistics %SWI_FILE%
call flooddrought calculate_swi_indices %SWI_FILE%
call flooddrought save_timeslice_geotiff %SWI_FILE% %EXPORT_DIR_SWI%
call flooddrought save_timeslice_geotiff %SWI_DIR%\indices\*deviation*.nc %EXPORT_DIR_SWI%\deviation

call flooddrought download_trmm --extent %TRMM_EXTENT% %TRMM_FILE% %DOWNLOAD_START% %DOWNLOAD_END% --no-delete
call flooddrought save_spi_stats %TRMM_FILE%
call flooddrought calculate_rainfall_indices %TRMM_FILE%
call flooddrought save_timeslice_geotiff %TRMM_FILE% %EXPORT_DIR_TRMM%
call flooddrought save_timeslice_geotiff %TRMM_DIR%\indices\*_1_month*.nc %EXPORT_DIR_TRMM%\1_month
call flooddrought save_timeslice_geotiff %TRMM_DIR%\indices\*_3_month*.nc %EXPORT_DIR_TRMM%\3_month
call flooddrought save_timeslice_geotiff %TRMM_DIR%\indices\*_6_month*.nc %EXPORT_DIR_TRMM%\6_month

pause
