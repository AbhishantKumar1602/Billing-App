@echo off
echo ========================================
echo  Building ThePhysioRehab ...
echo ========================================

:: Install ALL required dependencies
echo Installing required packages...
pip install pyinstaller openpyxl et_xmlfile jaraco.text jaraco.functools jaraco.context jaraco.classes more_itertools platformdirs --quiet

:: Verify openpyxl installed correctly
python -c "import openpyxl; print('[OK] openpyxl', openpyxl.__version__)"
if %errorlevel% neq 0 (
    echo ERROR: openpyxl failed to install. Cannot continue.
    pause
    exit /b 1
)

:: Clean previous builds
echo Cleaning old build files...
if exist build   rmdir /s /q build
if exist dist    rmdir /s /q dist

echo.
echo Building EXE (this may take 2-3 minutes)...
python -m PyInstaller THE_PHYSIOREHAB.spec

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Build failed. Check the output above.
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Done! Folder is in dist\ThePhysioRehab\
echo  Run:  dist\ThePhysioRehab\ThePhysioRehab.exe
echo ========================================
pause