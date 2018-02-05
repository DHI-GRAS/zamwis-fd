setlocal enableextensions

if not defined SWI_DIR (exit /b -1)
if not defined EXPORT_DIR_SWI (exit /b -1)

setlocal "SWI_FILE=%SWI_DIR%\SWI.nc"

setlocal SWI_EXTENT="18.3,36.5,-20.4,-8.9"

REM setlocal DOWNLOAD_START="--startdate=20160101"
REM setlocal DOWNLOAD_END="--enddate=20160201"
REM setlocal NO_DELETE="--no-delete"

call activate fd

call flooddrought download_swi --product SWI --extent %SWI_EXTENT% %SWI_FILE% %DOWNLOAD_START% %DOWNLOAD_END% %NO_DELETE%
call flooddrought update_longterm_statistics %SWI_FILE%
call flooddrought calculate_swi_indices %SWI_FILE%
call flooddrought save_timeslice_geotiff %SWI_FILE% %EXPORT_DIR_SWI%
call flooddrought save_timeslice_geotiff %SWI_DIR%\indices\*deviation*.nc %EXPORT_DIR_SWI%\deviation
