setlocal enableextensions

if not defined LAKES_DIR (exit /b -1)

call import\runscript.bat "/Import/ImportJASON" importDirectory=%LAKES_DIR% "spreadsheetPath=/Import/JASON"

endlocal