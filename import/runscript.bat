@echo off
setlocal
set path=%DHIDSS%;%path%
cd %~dp0

set bat=runscript.py
set log=runscript.log

SHIFT
echo started %DATE% %TIME%
ipy64.exe "%bat%" %* 
echo finished %DATE% %TIME%

endlocal