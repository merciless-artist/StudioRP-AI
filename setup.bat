@echo off
color 0D
echo.
echo  _____ _             _ _         ____        _       
echo /\  ___\ /\__  _\/\ \/\ \ /\  __-. /\ \ /\  __ \   
echo \ \___  \\/_/\ \/\ \ \_\ \\ \ \/\ \\ \ \\ \ \/\ \  
echo  \/\_____\  \ \_\ \ \_____\\ \____- \ \_\\ \_____\ 
echo   \/_____/   \/_/  \/_____/ \/____/  \/_/ \/_____/ 
echo.
echo  ⬩❖ ⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌ ⬩ ❖  ♡  ❖ ⬩⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌ ❖ ⬩
echo      𝐒𝐭𝐮𝐝𝐢𝐨 𝐑𝐏 𝐀𝐈 - https://discord.gg/the-studio 
echo    18+ Creative Space for AI Roleplay, Music & Art
echo  ⬩❖ ⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌ ⬩ ❖  ♡  ❖ ⬩⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌ ❖ ⬩
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo  [ERROR] Python is not installed. Please install Python 3.8 or higher.
    echo  Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo  [*] Python detected!
echo.

REM Create virtual environment
echo  [*] Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo  [*] Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo  [*] Installing dependencies...
pip install -r requirements.txt

REM Check if character.json exists
if not exist character.json (
    echo.
    echo  [*] Creating character.json from template...
    copy character_template.json character.json
    echo  [!] Please edit character.json with your character's details.
)

REM Check if .env exists
if not exist .env (
    echo.
    echo  [*] Creating .env from example...
    copy .env.example .env
    echo  [!] Please edit .env with your Discord token and ElectronHub API key.
)

echo.
echo  ⬩❖ ⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌ ⬩ ❖  ♡  ❖ ⬩⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌ ❖ ⬩
echo    Setup Complete! Your Studio Bot is ready!
echo  ⬩❖ ⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌ ⬩ ❖  ♡  ❖ ⬩⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌ ❖ ⬩
echo.
echo  Next steps:
echo    1. Edit character.json with your character's details
echo    2. Edit .env with your Discord token and ElectronHub API key
echo    3. Run: venv\Scripts\activate.bat
echo    4. Run: python app.py
echo.
echo  Join The Studio Discord: https://discord.gg/the-studio
echo.
pause