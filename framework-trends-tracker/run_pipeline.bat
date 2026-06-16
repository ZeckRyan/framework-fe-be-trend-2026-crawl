@echo off
pushd "%~dp0"

echo ============================================
echo  Framework Trends Tracker - Pipeline Runner
echo ============================================
echo.
echo Select data sources:
echo   1. All sources (default)
echo   2. GitHub + NPM + PyPI (crawl only)
echo   3. Stack Overflow survey only
echo   4. GitHub + Stack Overflow
echo   5. Custom (comma-separated)
echo.
set /p choice="Enter choice (1-5): "

if "%choice%"=="2" (
    set SOURCES=github,npm,pypi
) else if "%choice%"=="3" (
    set SOURCES=stackoverflow
) else if "%choice%"=="4" (
    set SOURCES=github,stackoverflow
) else if "%choice%"=="5" (
    set /p SOURCES="Enter sources (comma-separated, e.g. github,npm,stackoverflow): "
) else (
    set SOURCES=all
)

echo.
echo Running pipeline with sources: %SOURCES%
echo ---
python -m scraper.main_pipeline --sources %SOURCES%
echo ---
python -m scraper.data_processor
echo ---
python -m reports_internal.generate_report
pause
