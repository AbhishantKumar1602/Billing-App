@echo off
echo ========================================
echo  Building billing_final.exe ...
echo ========================================

:: Install PyInstaller
echo Installing PyInstaller...
pip install pyinstaller

:: Run PyInstaller via python -m (works even if pyinstaller not in PATH)
echo.
echo Building EXE...
python -m PyInstaller --onefile --windowed --name "BillingApp" THE PHYSIOREHAB.py

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Build failed. Check the output above for details.
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Done! EXE is in the dist\ folder.
echo ========================================
pause