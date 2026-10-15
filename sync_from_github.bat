@echo off
chcp 65001 >nul
echo ========================================================
echo 🚀 [YT_vaibhavsisinty] Synchronisation locale avec GitHub
echo ========================================================
cd /d "%~dp0"

git fetch origin main
git pull origin main --rebase

echo.
echo ✅ Synchronisation terminée ! Fichiers à jour dans :
echo    %CD%
echo.
pause
