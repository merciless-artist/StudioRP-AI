@echo off
color 0D
echo.
echo  ⬩❖ ⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌ ⬩ ❖  ♡  ❖ ⬩⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌ ❖ ⬩
echo      𝐒𝐭𝐮𝐝𝐢𝐨 𝐁𝐨𝐭 - Starting up...
echo  ⬩❖ ⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌ ⬩ ❖  ♡  ❖ ⬩⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌ ❖ ⬩
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Start the bot
python app.py

pause