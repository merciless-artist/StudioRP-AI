import discord
from discord.ext import commands
import aiohttp
import json
import asyncio
import os
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Memory interface
from abc import ABC, abstractmethod

class MemoryInterface(ABC):
    """Abstract base class for memory systems"""
    
    @abstractmethod
    async def get_memories(self, user_id: int, limit: int = 20) -> List[Dict]:
        pass
    
    @abstractmethod
    async def add_memory(self, user_id: int, role: str, content: str) -> None:
        pass
    
    @abstractmethod
    async def clear_memories(self, user_id: int) -> None:
        pass


class LocalMemory(MemoryInterface):
    """Local JSON file storage for fps.ms compatibility"""
    
    def __init__(self, character_name: str = "bot"):
        self.character_name = character_name.lower().replace(" ", "_")
        self.memory_file = f"memories_{self.character_name}.json"
        self.memories: Dict[int, List] = self._load_memories()
    
    def _load_memories(self) -> Dict[int, List]:
        """Load memories from JSON file"""
        try:
            with open(self.memory_file, 'r') as f:
                data = json.load(f)
                return {int(k): v for k, v in data.items()}
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _save_memories(self) -> None:
        """Save memories to JSON file"""
        data = {str(k): v for k, v in self.memories.items()}
        with open(self.memory_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    async def get_memories(self, user_id: int, limit: int = 20) -> List[Dict]:
        if user_id not in self.memories:
            return []
        return self.memories[user_id][-limit:]
    
    async def add_memory(self, user_id: int, role: str, content: str) -> None:
        if user_id not in self.memories:
            self.memories[user_id] = []
        
        self.memories[user_id].append({"role": role, "content": content})
        
        if len(self.memories[user_id]) > 50:
            self.memories[user_id] = self.memories[user_id][-50:]
        
        self._save_memories()
    
    async def clear_memories(self, user_id: int) -> None:
        if user_id in self.memories:
            self.memories[user_id] = []
            self._save_memories()


# Bot class
class StudioBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.reactions = True
        intents.members = True
        intents.presences = True
        
        super().__init__(
            command_prefix='!',
            intents=intents,
            help_command=None
        )
        
        self.character_file = os.getenv('CHARACTER_FILE', 'character.json')
        self.character_data = self.load_character_data()
        self.mode = "chat"
        self.session = None
        self.memory_system = LocalMemory(self.character_data['profile']['name'])
        
    def load_character_data(self):
        """Load character data from JSON file"""
        try:
            with open(self.character_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Character file {self.character_file} not found. Using template.")
            with open('character_template.json', 'r', encoding='utf-8') as f:
                return json.load(f)
    
    def save_character_data(self):
        """Save character data to JSON file"""
        with open(self.character_file, 'w', encoding='utf-8') as f:
            json.dump(self.character_data, f, indent=2, ensure_ascii=False)
    
    async def setup_hook(self):
        """Initialize the HTTP session and load commands"""
        self.session = aiohttp.ClientSession()
        await self.add_cog(CharacterCommands(self))
        logger.info(f"{self.character_data['profile']['name']} bot is starting up...")
        
    async def close(self):
        """Clean up when bot shuts down"""
        if self.session:
            await self.session.close()
        await super().close()
        
    async def on_ready(self):
        logger.info(f'{self.character_data["profile"]["name"]} is online!')
        await self.change_presence(activity=discord.Game(name="in The Studio"))
        
    async def on_message(self, message):
        if message.author == self.user:
            return
            
        # Ignore messages in spoiler tags
        if message.content.startswith('||') and message.content.endswith('||'):
            return
            
        await self.process_commands(message)
        
        # Check for custom commands
        for cmd in self.character_data.get('knowledge', {}).get('commands', []):
            if message.content.lower() == cmd['command']:
                await message.reply(cmd['response'])
                return
        
        # Respond to mentions or DMs
        if self.user.mentioned_in(message) or isinstance(message.channel, discord.DMChannel):
            content = message.content.replace(f'<@{self.user.id}>', '').strip()
            
            if content.startswith('!'):
                return
                
            await self.generate_response(message, content)
    
    def build_system_prompt(self, user_data: Dict = None):
        """Build system prompt from character data"""
        char = self.character_data
        profile = char['profile']
        personality = char['personality']
        knowledge = char.get('knowledge', {})
        
        mode_instructions = ""
        if self.mode == "chat":
            mode_instructions = f"""
You are currently in CHAT MODE. In this mode:
- Speak in first person as {profile['name']}
- Be conversational and natural
- Keep messages relatively short unless the conversation requires more
- Stay true to your speech patterns
"""
        else:
            mode_instructions = f"""
You are currently in ROLEPLAY MODE. In this mode:
- Write in third person narrative style
- Use "quotes for dialogue" and *italics for thoughts/actions*
- Create immersive scenes with your responses
"""
        
        
        # Build user info if available
        user_info = ""
        if user_data and char.get('user_info', {}).get('name'):
            ui = char['user_info']
            user_info = f"\n\nUSER INFORMATION:\n"
            if ui.get('name'): user_info += f"- Name: {ui['name']}\n"
            if ui.get('age'): user_info += f"- Age: {ui['age']}\n"
            if ui.get('pronouns'): user_info += f"- Pronouns: {ui['pronouns']}\n"
            if ui.get('info'): user_info += f"- Additional: {ui['info']}\n"
        
        return f"""{char.get('ai_system_preset', '')}

You are {profile['name']} ({profile['username']}) from The Studio Discord server.
Also known as: {', '.join(profile.get('aka_alias_nickname', []))}

APPEARANCE: {profile.get('appearance', '')}

BACKSTORY: {personality.get('short_backstory', '')}

PERSONALITY TRAITS: {', '.join(personality.get('traits', []))}
TONE: {personality.get('tone', 'natural')}

LIKES: {', '.join(personality.get('likes', []))}
DISLIKES: {', '.join(personality.get('dislikes', []))}

HISTORY: {personality.get('history', '')}

KNOWLEDGE:
- General: {knowledge.get('general', '')}
- World Lore: {knowledge.get('worldlore', '')}
- Habits: {knowledge.get('habits', '')}

RELATIONSHIPS:
{self._format_relationships(knowledge.get('relationships', {}))}

CONVERSATIONAL GOALS:
{personality.get('conversation_goals', '')}

{mode_instructions}

{user_info}

CURRENT CONTEXT:
- Server: The Studio (18+ creative space for music and art)
- Current mode: {self.mode}

Remember to stay true to your character while being helpful and engaging."""

    def _format_relationships(self, relationships: Dict) -> str:
        """Format relationships dictionary into readable text"""
        if not relationships:
            return "No established relationships"
        return "\n".join([f"- {name}: {desc}" for name, desc in relationships.items()])

    async def generate_response(self, message, content):
        """Generate AI response using ElectronHub API"""
        try:
            async with message.channel.typing():
                user_id = message.author.id
                recent_history = await self.memory_system.get_memories(user_id, limit=20)
                
                # Build user data for personalization
                user_data = {
                    'name': message.author.display_name,
                    'id': user_id
                }
                
                system_prompt = self.build_system_prompt(user_data)
                
                messages = [{"role": "system", "content": system_prompt}]
                messages.extend(recent_history)
                messages.append({"role": "user", "content": content})
                
                # Try primary model first
                response = await self.call_electronhub_api(messages)
                
                if response:
                    await self.memory_system.add_memory(user_id, "user", content)
                    await self.memory_system.add_memory(user_id, "assistant", response)
                    
                    await self.send_long_message(message, response)
                    
                    # Add reactions for feedback
                    sent_message = await message.channel.fetch_message(message.channel.last_message_id)
                    await sent_message.add_reaction('🔄')  # Regenerate
                    await sent_message.add_reaction('❤️')  # Good response
                    await sent_message.add_reaction('💔')  # Bad response
                    
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            await message.reply("*Something went wrong. Try again?*")
    
    async def call_electronhub_api(self, messages, use_fallback=False):
        """Make API call to OpenAI-compatible endpoint"""
        model_config = self.character_data.get('language_model', {})
        
        # Get API configuration
        api_type = model_config.get('api_type', 'electronhub')
        api_url = model_config.get('api_url', os.getenv('API_URL', 'https://api.electronhub.top'))
        api_key = model_config.get('api_key', os.getenv('API_KEY'))
        
        # Support legacy ElectronHub config
        if not api_key and 'electron_hub_proxy_key' in model_config:
            api_key = model_config['electron_hub_proxy_key']
        
        model = model_config.get('fallback_model' if use_fallback else 'selected_model', 'gpt-3.5-turbo')
        
        # Ensure proper URL format
        if not api_url.endswith('/v1/chat/completions'):
            api_url = api_url.rstrip('/') + '/v1/chat/completions'
        
        url = api_url
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": model,
            "messages": messages,
            "temperature": 0.8,
            "max_tokens": 1000,
            "top_p": 0.9,
            "frequency_penalty": 0.1,
            "presence_penalty": 0.1
        }
        
        try:
            async with self.session.post(url, headers=headers, json=data) as response:
                if response.status == 200:
                    result = await response.json()
                    return result['choices'][0]['message']['content'].strip()
                elif response.status == 429 and not use_fallback:
                    # Rate limit - try fallback model
                    logger.warning(f"Rate limit hit, trying fallback model")
                    return await self.call_electronhub_api(messages, use_fallback=True)
                else:
                    error_text = await response.text()
                    logger.error(f"API Error: {response.status} - {error_text}")
                    if not use_fallback and model_config.get('fallback_model'):
                        logger.info("Trying fallback model...")
                        return await self.call_electronhub_api(messages, use_fallback=True)
                    return None
        except Exception as e:
            logger.error(f"API call failed: {e}")
            if not use_fallback and model_config.get('fallback_model'):
                logger.info("Trying fallback model due to exception...")
                return await self.call_electronhub_api(messages, use_fallback=True)
            return None
    
    async def send_long_message(self, message, content):
        """Split long messages for Discord's character limit"""
        if len(content) <= 2000:
            await message.reply(content)
        else:
            chunks = []
            current_chunk = ""
            
            sentences = content.split('. ')
            for sentence in sentences:
                if len(current_chunk + sentence + '. ') > 1900:
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                        current_chunk = sentence + '. '
                    else:
                        chunks.append(sentence[:1900] + '...')
                        current_chunk = '...' + sentence[1900:] + '. '
                else:
                    current_chunk += sentence + '. '
            
            if current_chunk:
                chunks.append(current_chunk.strip())
            
            for i, chunk in enumerate(chunks):
                if i == 0:
                    await message.reply(chunk)
                else:
                    await message.channel.send(chunk)
                await asyncio.sleep(0.5)
    
    async def on_reaction_add(self, reaction, user):
        """Handle reaction-based feedback"""
        if user == self.user:
            return
            
        message = reaction.message
        if message.author != self.user:
            return
            
        emoji = str(reaction.emoji)
        
        if emoji == '🔄':
            # Regenerate response
            async for msg in message.channel.history(limit=10, before=message):
                if msg.author != self.user and (self.user.mentioned_in(msg) or isinstance(message.channel, discord.DMChannel)):
                    content = msg.content.replace(f'<@{self.user.id}>', '').strip()
                    await message.delete()
                    await self.generate_response(msg, content)
                    break
                    
        elif emoji == '❤️':
            logger.info(f"Positive feedback for {self.character_data['profile']['name']}")
            
        elif emoji == '💔':
            logger.info(f"Negative feedback for {self.character_data['profile']['name']}")


class CharacterCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='mode')
    async def switch_mode(self, ctx, mode: str = None):
        """Switch between chat and rp modes"""
        if mode not in ['chat', 'rp']:
            await ctx.reply("Usage: !mode [chat/rp]")
            return
            
        self.bot.mode = mode
        if mode == 'rp':
            response = "📖 Roleplay mode enabled - I'll respond in third person narrative style."
        else:
            response = "💬 Chat mode enabled - Let's talk normally!"
        await ctx.reply(response)
    
    @commands.command(name='character')
    @commands.has_permissions(administrator=True)
    async def edit_character(self, ctx, section: str = None, field: str = None, *, value: str = None):
        """Edit character data (Admin only)"""
        if not section:
            embed = discord.Embed(
                title="Character Editor",
                description="Use `!character <section> <field> <value>` to edit",
                color=discord.Color.blue()
            )
            embed.add_field(name="Sections", value="profile, personality, knowledge, language_model", inline=False)
            embed.add_field(name="Example", value="`!character profile name New Name`", inline=False)
            await ctx.reply(embed=embed)
            return
        
        try:
            if section in self.bot.character_data and field:
                if value:
                    # Handle list fields
                    if field in ['traits', 'likes', 'dislikes', 'aka_alias_nickname']:
                        self.bot.character_data[section][field] = [v.strip() for v in value.split(',')]
                    else:
                        self.bot.character_data[section][field] = value
                    self.bot.save_character_data()
                    await ctx.reply(f"✅ Updated {section}.{field}")
                else:
                    current = self.bot.character_data[section].get(field, "Not set")
                    await ctx.reply(f"Current value of {section}.{field}: {current}")
        except Exception as e:
            await ctx.reply(f"❌ Error: {str(e)}")
    
    
    @commands.command(name='show')
    async def show_character(self, ctx, section: str = None):
        """Show character information"""
        char = self.bot.character_data
        
        if not section:
            profile = char['profile']
            personality = char['personality']
            
            embed = discord.Embed(
                title=profile['name'],
                description=personality.get('short_backstory', 'No backstory'),
                color=discord.Color.purple()
            )
            embed.add_field(name="Username", value=profile.get('username', 'Not set'), inline=True)
            embed.add_field(name="Tone", value=personality.get('tone', 'natural'), inline=True)
            embed.add_field(name="Mode", value=self.bot.mode, inline=True)
            embed.add_field(name="Traits", value=", ".join(personality.get('traits', [])) or "None", inline=False)
            embed.add_field(name="Model", value=char.get('language_model', {}).get('selected_model', 'Not set'), inline=True)
            await ctx.reply(embed=embed)
        else:
            if section in char:
                embed = discord.Embed(
                    title=f"{section.title()} Section",
                    color=discord.Color.blue()
                )
                
                section_data = char[section]
                for key, value in section_data.items():
                    if isinstance(value, list):
                        value = ", ".join(value) or "Empty"
                    elif isinstance(value, dict):
                        value = f"{len(value)} entries"
                    else:
                        value = str(value)[:100] + "..." if len(str(value)) > 100 else str(value)
                    
                    embed.add_field(name=key.replace('_', ' ').title(), value=value, inline=False)
                
                await ctx.reply(embed=embed)
            else:
                await ctx.reply(f"Section '{section}' not found. Available: profile, personality, knowledge, language_model")
    
    @commands.command(name='init')
    async def send_initial_message(self, ctx):
        """Send the character's initial message"""
        initial = self.bot.character_data['profile'].get('initial_message', '')
        if initial:
            await ctx.send(initial)
        else:
            await ctx.reply("No initial message set for this character.")
    
    @commands.command(name='reset_memory')
    async def reset_memory(self, ctx):
        """Reset your conversation history with the bot"""
        user_id = ctx.author.id
        await self.bot.memory_system.clear_memories(user_id)
        await ctx.reply("🧹 Your conversation history has been reset!")
    
    @commands.command(name='model')
    @commands.has_permissions(administrator=True)
    async def change_model(self, ctx, model: str = None):
        """Change the AI model (Admin only)"""
        if not model:
            current = self.bot.character_data.get('language_model', {}).get('selected_model', 'Not set')
            fallback = self.bot.character_data.get('language_model', {}).get('fallback_model', 'Not set')
            await ctx.reply(f"Current model: {current}\nFallback model: {fallback}")
            return
        
        self.bot.character_data['language_model']['selected_model'] = model
        self.bot.save_character_data()
        await ctx.reply(f"✅ Model changed to: {model}")


# Run the bot
if __name__ == "__main__":
    bot = StudioBot()
    token = os.getenv('DISCORD_TOKEN')
    
    if not token:
        logger.error("No Discord token found! Set DISCORD_TOKEN in .env file")
    else:
        bot.run(token)