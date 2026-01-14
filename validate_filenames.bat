@echo off
REM Windows batch file to validate filenames for cross-platform compatibility
REM This script checks for problematic characters in music files

echo Tuesday Ukes - Filename Validator
echo ===================================
echo.
echo Checking music files for cross-platform compatibility...
echo.

REM Change to the script directory
cd /d "%~dp0"

REM Run the Python script with music file extensions
python validate_filenames.py --fix --extensions .pdf .chopro .cho

echo.
if %ERRORLEVEL% EQU 0 (
    echo ✅ All filenames are compatible!
) else (
    echo ❌ Issues found. Please review the output above.
    echo.
    echo To fix files, use:
    echo   git mv "old filename" "new filename"
    echo.
    echo Then update any HTML links that reference the renamed files.
)

echo.
echo Press any key to close...
pause >nul
