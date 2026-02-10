@echo off
cd /d "%~dp0"
echo Starting FastAPI Server...
..\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
pause
