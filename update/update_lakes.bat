setlocal enableextensions

if not defined LAKES_DIR (exit /b -1)

set LAKE_NUMBERS="0317,0394,0414,0415"

call activate fd

call flooddrought pecad_lakes_to_csv --lake-numbers %LAKE_NUMBERS% %LAKES_DIR%

endlocal