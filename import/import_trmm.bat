setlocal enableextensions

if not defined EXPORT_DIR_TRMM (exit /b -1)

call import\runscript.bat "/Import/ImportAndAppendTemporalRaster" importDir=%EXPORT_DIR_TRMM% "rasterName=Rainfall (mm day-1)" "datetimeFileMask=yyyyMMdd" "append=TRUE"
call import\runscript.bat "/Import/ImportAndAppendTemporalRaster" importDir=%EXPORT_DIR_TRMM%\1_month "rasterName=spi1m" "datetimeFileMask=yyyyMMdd" "append=TRUE"
call import\runscript.bat "/Import/ImportAndAppendTemporalRaster" importDir=%EXPORT_DIR_TRMM%\3_month "rasterName=spi3m" "datetimeFileMask=yyyyMMdd" "append=TRUE"
call import\runscript.bat "/Import/ImportAndAppendTemporalRaster" importDir=%EXPORT_DIR_TRMM%\6_month "rasterName=spi6m" "datetimeFileMask=yyyyMMdd" "append=TRUE"

endlocal