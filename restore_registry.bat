@echo off
echo Restoring registry keys that may have caused system instability...
echo.

REM Remove the registry keys we added
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer" /v NoShutdown /f 2>nul
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer" /v NoLogoff /f 2>nul
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer" /v NoSleep /f 2>nul
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer" /v NoHibernate /f 2>nul

echo Registry keys removed.
echo.
echo Please restart your computer for changes to take effect.
echo.
pause
