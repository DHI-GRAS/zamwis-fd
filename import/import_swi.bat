setlocal enableextensions

if not defined EXPORT_DIR_SWI exit /b -1 

call import\runscript.bat "/Import/ImportAndAppendTemporalRaster" importDir=%EXPORT_DIR_SWI% "rasterName=swi" "datetimeFileMask=yyyyMMdd" "append=TRUE"
call import\runscript.bat "/Import/ImportAndAppendTemporalRaster" importDir=%EXPORT_DIR_SWI%\deviation "rasterName=swi_dev" "datetimeFileMask=yyyyMMdd" "append=TRUE"

endlocal
