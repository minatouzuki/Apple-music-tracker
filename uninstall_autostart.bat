@echo off
setlocal
REM ============================================================
REM  Removes the automatic startup of the Now Playing watcher.
REM  Double-click to run. (The copy already running keeps going
REM  until you reboot or end pythonw.exe in Task Manager.)
REM ============================================================

schtasks /delete /tn "ItsukiNowPlaying" /f >nul 2>&1

if %errorlevel%==0 (
  echo.
  echo  Autostart removed. Reboot (or end pythonw.exe in
  echo  Task Manager) to stop the copy that's running now.
  echo.
) else (
  echo.
  echo  No autostart task found - nothing to remove.
  echo.
)
pause
