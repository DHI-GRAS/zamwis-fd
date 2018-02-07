setlocal enableextensions

if not defined EXPORT_DIR_SST exit /b -1 

call import\runscript.bat "/Import/ImportAndAppendTemporalRaster" importDir=%EXPORT_DIR_SST% "rasterName=Lake surface temperature (°C)" "datetimeFileMask=yyyyMMdd" "append=TRUE"

endlocal
