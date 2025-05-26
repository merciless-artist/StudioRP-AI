#!/bin/bash

echo ""
echo " _____ _             _ _         ____        _       "
echo "/\  ___\ /\__  _\/\ \/\ \ /\  __-. /\ \ /\  __ \   "
echo "\ \___  \\\\/_/\ \/\ \ \_\ \\\ \ \/\ \\\ \ \\\ \ \/\ \  "
echo " \/\_____\  \ \_\ \ \_____\\\ \____- \ \_\\\ \_____\ "
echo "  \/_____/   \/_/  \/_____/ \/____/  \/_/ \/_____/ "
echo ""
echo " ⬩❖ ⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌ ⬩ ❖  ♡  ❖ ⬩⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌ ❖ ⬩"
echo "     𝐒𝐭𝐮𝐝𝐢𝐨 𝐑𝐏 𝐀𝐈 - https://discord.gg/the-studio "
echo "   18+ Creative Space for AI Roleplay, Music & Art"
echo " ⬩❖ ⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌ ⬩ ❖  ♡  ❖ ⬩⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌ ❖ ⬩"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Error: Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if character.json exists
if [ ! -f "character.json" ]; then
    echo "Creating character.json from template..."
    cp character_template.json character.json
    echo "Please edit character.json with your character's details."
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Creating .env from example..."
    cp .env.example .env
    echo "Please edit .env with your Discord token and ElectronHub API key."
fi

echo ""
echo " ⬩❖ ⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌ ⬩ ❖  ♡  ❖ ⬩⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌ ❖ ⬩"
echo "   Setup Complete! Your Studio Bot is ready!"
echo " ⬩❖ ⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌ ⬩ ❖  ♡  ❖ ⬩⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌⚌ ❖ ⬩"
echo ""
echo " Next steps:"
echo "   1. Edit character.json with your character's details"
echo "   2. Edit .env with your Discord token and ElectronHub API key"
echo "   3. Run: source venv/bin/activate"
echo "   4. Run: python app.py"
echo ""
echo " Join The Studio Discord: https://discord.gg/the-studio"
echo ""