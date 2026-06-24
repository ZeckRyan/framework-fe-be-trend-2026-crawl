@echo off
cd /d "%~dp0"
echo === Staging files ===
git add -A
echo === Committing ===
git commit -m "feat: Framework Trends Tracker - 18 frameworks with SO 2025 integration, orbit hero dashboard, and Makefile"
echo === Pushing to GitHub ===
git push -u origin main
echo === Done ===
pause
