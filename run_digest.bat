@echo off
rem Runs the daily digest. Used by Windows Task Scheduler; output is appended to digestRun.log.
cd /d "%~dp0"
echo ==== %date% %time% ==== >> digestRun.log
"C:\Users\Crow104\anaconda3\python.exe" physicsRSSreaderMain.py >> digestRun.log 2>&1
