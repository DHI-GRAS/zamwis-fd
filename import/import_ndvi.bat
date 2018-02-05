setlocal enableextensions

if not defined EXPORT_DIR_NDVI exit /b -1 

call import\runscript.bat "/Import/ImportAndAppendTemporalRaster" importDir=%EXPORT_DIR_NDVI% "rasterName=Normalized Difference Vegetation Index (NDVI)" "datetimeFileMask=yyyyMMdd" "append=TRUE"
call import\runscript.bat "/Import/ImportAndAppendTemporalRaster" importDir=%EXPORT_DIR_NDVI%\anomaly "rasterName=Vegetation anomaly" "datetimeFileMask=yyyyMMdd" "append=TRUE"
