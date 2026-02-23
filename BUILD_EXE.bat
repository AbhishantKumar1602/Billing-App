@echo off
title Build EXE - Billing App
color 0A

echo.
echo  ============================================
echo   BUILD BILLING APP AS .EXE
echo  ============================================
echo.

echo  Installing PyInstaller...
pip install pyinstaller --quiet

echo  Building EXE (this may take 1-2 minutes)...
echo.

pyinstaller --noconfirm --onefile --windowed ^
  --name "BillingApp" ^
  --add-data "billing.db;." ^
  billing_app.py

echo.
echo  ============================================
echo   DONE! EXE is in the "dist" folder.
echo  ============================================
echo.
pause
