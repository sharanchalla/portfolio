@echo off
title Sharan Challa Portfolio Server
cd /d "%~dp0"
echo ===================================================
echo   Starting Sharan Challa Portfolio Website...
echo   Open in browser: http://127.0.0.1:5000
echo ===================================================
start http://127.0.0.1:5000
python app.py
pause
