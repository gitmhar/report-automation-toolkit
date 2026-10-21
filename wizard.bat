@echo off
echo ========================================
echo    REPORTING AUTOMATION TOOLKIT
echo ========================================

cd /d "%~dp0"

call .venv\Scripts\activate.bat

echo.
echo Launching Interactive Wizard
echo -----------------------------------------

python -m src.sales-reporting.wizard

echo.
echo ==============================================
echo Execution finished. You can close this window.
echo ==============================================
pause