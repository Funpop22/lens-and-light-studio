@echo off
echo ==========================================
echo    LENS ^& LIGHT STUDIO - GitHub Push
echo ==========================================
echo.

REM Ask for a commit message
set /p msg="Describe your changes (e.g. Updated gallery): "

echo.
echo Adding all changes...
git add .

echo Creating commit...
git commit -m "%msg%"

echo Pushing to GitHub...
git push https://Funpop22:YOUR_NEW_TOKEN_HERE@github.com/Funpop22/lens-and-light-studio.git main

echo.
echo ==========================================
echo  Done! Check github.com/Funpop22/lens-and-light-studio
echo ==========================================
pause
