@echo off
REM Windows batch file to run update_timestamps.py with default behavior
REM This script updates v= timestamps in the practice-songs-table and submitted-songs-table

echo Tuesday Ukes - Timestamp Updater
echo ===================================
echo.
echo Updating v= timestamps in index.html...
echo.

REM Change to the script directory
cd /d "%~dp0"

REM Run the Python script with default settings
python update_timestamps.py

echo.
if %ERRORLEVEL% EQU 0 (
    echo Update completed successfully!
) else (
    echo Update failed with error code %ERRORLEVEL%
)

echo.
echo Press any key to close...
pause >nul
