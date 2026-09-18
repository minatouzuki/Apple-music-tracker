@echo off
setlocal
REM ============================================================
REM  Installs the Now Playing watcher to start automatically
REM  every time you log on to Windows. Runs silently -
REM  no terminal window.
REM  Run this file by double-clicking it (same folder as
REM  nowplaying.py).
REM ============================================================

for /f "delims=" %%i in ('where pythonw 2^>nul') do set PYW=%%i & goto :foundpyw
echo.
echo  Could not find pythonw.exe
echo  Reinstall Python from https://www.python.org/downloads/
echo  and tick "Add python.exe to PATH".
echo.
pause
exit /b 1
:foundpyw

for /f "delims=" %%i in ('where python 2^>nul') do set PY=%%i & goto :foundpy
echo.
echo  Could not find python.exe - reinstall Python with PATH enabled.
echo.
pause
exit /b 1
:foundpy

set SCRIPT=%~dp0nowplaying.py
set RELAY=267862fb-d72c-4114-b04e-200d2d7b0656

if not exist "%SCRIPT%" (
  echo.
  echo  nowplaying.py not found next to this file.
  echo  Keep install_autostart.bat in the same folder as nowplaying.py.
  echo.
  pause
  exit /b 1
)

echo  Checking for the 'winsdk' package...
"%PY%" -c "import winsdk" 2>nul
if %errorlevel% neq 0 (
  echo  Installing winsdk ^(one time, needs internet^)...
  "%PY%" -m pip install winsdk
  echo.
  "%PY%" -c "import winsdk" 2>nul
  if %errorlevel% neq 0 (
    echo  Couldn't install winsdk automatically.
    echo  Open a terminal and run:  pip install winsdk
    echo  Then run this installer again.
    echo.
    pause
    exit /b 1
  )
)
echo  winsdk is ready.
echo.
echo  Quick test - what's playing right now?
"%PY%" "%SCRIPT%" status
echo.

schtasks /create /tn "ItsukiNowPlaying" ^
  /tr "\"%PYW%\" \"%SCRIPT%\" watch --relay %RELAY%" ^
  /sc onlogon /f >nul 2>&1

if %errorlevel%==0 (
  echo  Installed! The watcher will now start automatically
  echo  every time you log on to Windows - no terminal needed.
  echo.
  echo  Starting it right now in the background...
  start "" "%PYW%" "%SCRIPT%" watch --relay %RELAY%
  echo  Done. Skip a track and watch WhatsApp. 
  echo.
) else (
  echo.
  echo  Couldn't create the scheduled task.
  echo  Right-click install_autostart.bat and choose
  echo  "Run as administrator", then try again.
  echo.
)
pause
