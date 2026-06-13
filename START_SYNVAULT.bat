@echo off
start "SYNVAULT JSON Backend" "%~dp0BACKEND\RUN_BACKEND.cmd"
timeout /t 3 >nul
start "" "http://127.0.0.1:8000"
