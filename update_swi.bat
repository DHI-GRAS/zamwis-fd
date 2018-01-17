SETLOCAL ENABLEEXTENSIONS
SET PARENT=%~dp0

set SWI_EXTENT="18.3,36.5,-20.4,-8.9"

REM set DOWNLOAD_START="--startdate=20160101"
REM set DOWNLOAD_END="--enddate=20160201"

set "SWI_DIR=%PARENT%\SWI"
set "SWI_FILE=%SWI_DIR%\SWI.nc"

set "EXPORT_DIR=%PARENT%\export"
set "EXPORT_DIR_SWI=%EXPORT_DIR%\SWI"

call activate fd

call flooddrought download_swi --product SWI --extent %SWI_EXTENT% %SWI_FILE% %DOWNLOAD_START% %DOWNLOAD_END% --no-delete
call flooddrought update_longterm_statistics %SWI_FILE%
call flooddrought calculate_swi_indices %SWI_FILE%
call flooddrought save_timeslice_geotiff %SWI_FILE% %EXPORT_DIR_SWI%
call flooddrought save_timeslice_geotiff %SWI_DIR%\indices\*deviation*.nc %EXPORT_DIR_SWI%\deviation

pause
