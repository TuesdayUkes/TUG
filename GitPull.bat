@echo off
if not "%CONHOST_LAUNCHED%"=="1" (
    set CONHOST_LAUNCHED=1
    start "GitPull" conhost.exe cmd.exe /c "%~f0"
    exit
)
mode con: cols=50 lines=30
cd c:\users\PC\TUG
if errorlevel 1 goto error

git pull
if errorlevel 1 goto error

pip install pipx
if errorlevel 1 goto error

pipx install genlist-butler --force
if errorlevel 1 goto error

genlist music ukulele-song-archive.html
if errorlevel 1 goto error

echo.
color 0A
echo ===================================
echo SUCCESS: All operations completed!
echo ===================================
color
pause
exit /b 0

:error
echo.
color 4F
echo ========================================
echo ERROR: Operation failed!
echo ========================================
echo Please check the error message above
echo ========================================
color
pause
exit /b 1
