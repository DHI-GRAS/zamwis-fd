setlocal enableextensions

if not defined EXPORT_DIR_CHL exit /b -1 

call import\runscript.bat "/Import/ImportAndAppendTemporalRaster" importDir=%EXPORT_DIR_CHL% "rasterName=Chlorophyll (mg/ml)" "datetimeFileMask=yyyyMMdd" "append=TRUE"

endlocal
