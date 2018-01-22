SETLOCAL ENABLEEXTENSIONS
SET PARENT=%~dp0

set LAKE_NUMBERS="0317,0394,0414,0415"

set "LAKES_DIR=%PARENT%\lakes"

call activate fd

call flooddrought pecad_lakes_to_csv --lake-numbers %LAKE_NUMBERS% %LAKES_DIR%

pause
