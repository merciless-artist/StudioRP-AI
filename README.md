🔹---💠---🔹🔹---💠---🔹🔹---💠---🔹

# Studio Bot Template
A flexible Discord bot template for creating AI-powered character bots using any OpenAI-compatible API (ElectronHub, OpenAI, OpenRouter, Groq, local LLMs, etc.).

🔹---💠---🔹
## Features
- 💠 AI-powered responses using any OpenAI-compatible API
- 💠 Local memory system for conversation history
- 💠 Automatic fallback model support
- 💠 Extensive character customization through JSON
- 💠 Chat and roleplay modes
- 💠 In-Discord character editing (admin only)
- 💠 Custom commands per character

🔹---💠---🔹
## Setup
### I usually host my bots with fps.ms because it is either free or super cheap to run a server there in python or js. They require your app to be called `app.py` 


1. **Clone this template**
   ```bash
   git clone <repository-url>
   cd studio-bot-template
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your character**
   - Copy `character_template.json` to `character.json`
   - Edit `character.json` with your character's details

4. **Set up environment variables**
   Create a `.env` file:
   ```env
   DISCORD_TOKEN=your_discord_bot_token
   CHARACTER_FILE=character.json
   API_URL=https://api.provider.whatever
   API_KEY=your_api_key
   ```

5. **Run the bot**
   ```bash
   python app.py
   ```

## Character Configuration

The `character.json` file contains all character data:

### Profile Section
```json
"profile": {
  "username": "character_username",
  "name": "Character Display Name",
  "aka_alias_nickname": ["Nick1", "Nick2"],
  "appearance": "Physical description",
  "initial_message": "Greeting message"
}
```

### Personality Section
```json
"personality": {
  "short_backstory": "Brief background",
  "traits": ["trait1", "trait2"],
  "tone": "How they speak",
  "likes": ["thing1", "thing2"],
  "dislikes": ["thing1", "thing2"],
  "history": "Detailed history",
  "conversation_goals": "What they aim for in chats"
}
```

### Language Model Settings
```json
"language_model": {
  "api_type": "electronhub",
  "api_url": "https://api.provider.whatever",
  "api_key": "your-key",
  "selected_model": "gpt-4o",
  "fallback_model": "gemini-pro-latest"
}
```

### Supported API Providers

Check `api_examples.json` for configuration examples:
- **ElectronHub** - Default, great for roleplay
- **OpenAI** - Direct ChatGPT/GPT-4 access
- **OpenRouter** - Access to many models
- **Groq** - Fast inference
- **Local LLMs** - Ollama, LM Studio, etc.
- **Together AI** - Open source models
- **Anyscale** - Scalable endpoints
- **Perplexity** - With web search

## Commands

### User Commands
- `@bot <message>` - Chat with the bot
- `!mode [chat/rp]` - Switch between chat and roleplay modes
- `!show [section]` - Display character information
- `!init` - Send the character's initial message
- `!reset_memory` - Clear your conversation history

### Admin Commands
- `!character <section> <field> <value>` - Edit character data
- `!model <model_name>` - Change the AI model

## Custom Commands

Add custom commands in the character JSON:
```json
"commands": [
  {
    "command": "!special",
    "description": "Does something special",
    "response": "Special response text"
  }
]
```

## Memory System

The bot maintains conversation history per user:
- Stores last 50 messages per user
- Saves to local JSON files
- Can be cleared with `!reset_memory`

## Model Fallback

If the primary model fails or hits rate limits, the bot automatically switches to the fallback model specified in the configuration.

## Deployment

### Local/VPS
1. Install Python 3.8+
2. Follow setup instructions above
3. Use a process manager like PM2 or systemd

### fps.ms Hosting
1. Upload all files to your fps.ms server
2. Install dependencies via SSH
3. Set environment variables in the fps.ms panel
4. Start the bot

## Customization

### Adding New Features
1. Create new commands in the `CharacterCommands` cog
2. Add new sections to the character JSON structure
3. Extend the `build_system_prompt` method for new behaviors

### Changing Memory Systems
Implement the `MemoryInterface` abstract class to create custom memory backends (Redis, PostgreSQL, etc.)

## Support

For issues or questions:
- Check existing character examples in the `examples/` folder
- Review the Discord.py documentation
- Check your API provider's documentation
- See `api_examples.json` for different provider configurations

## License

Creative Commons - feel free to use this template for your own bots!

🔹---💠---🔹🔹---💠---🔹🔹---💠---🔹
