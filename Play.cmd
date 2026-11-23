@echo off
setlocal
pushd "%~dp0" || exit /b 1
where py.exe >nul 2>&1
if errorlevel 1 goto python
py -3 play.py %*
goto done
:python
python play.py %*
:done
set "result=%errorlevel%"
if not "%result%"=="0" pause
popd
exit /b %result%
