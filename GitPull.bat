@echo off
if not "%CONHOST_LAUNCHED%"=="1" (
    set CONHOST_LAUNCHED=1
    start "GitPull" conhost.exe cmd.exe /c "%~f0"
    exit
)
mode con: cols=50 lines=30
cd c:\users\PC\TUG
if errorlevel 1 goto error

for /f %%H in ('git rev-parse HEAD') do set "HEAD_BEFORE=%%H"

git pull
if errorlevel 1 goto error

for /f %%H in ('git rev-parse HEAD') do set "HEAD_AFTER=%%H"

if "%HEAD_BEFORE%"=="%HEAD_AFTER%" if not exist .genlist-stale (
    echo.
    color 0A
    echo =============================================
    echo Git already up to date. Skipping remaining steps.
    echo =============================================
    color
    pause
    exit /b 0
)

rem Mark output as stale before touching anything.
rem If power dies anywhere below, next run will retry.
type nul > .genlist-stale

pip install pipx
if errorlevel 1 goto error

pipx install genlist-butler --force
if errorlevel 1 goto error

genlist music ukulele-song-archive.html
if errorlevel 1 goto error

del .genlist-stale

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
