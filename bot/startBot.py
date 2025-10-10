# Imports
import discord
import logging
import logging.handlers
from pathlib import Path

from . import settings  # relative import so module resolves when run as package
from bot.discordBot.DiscordBot import DiscordBot


def start():
    """Start Bot function"""
    # Bot Permissions
    intents = discord.Intents.default()
    intents.message_content = True
    intents.voice_states = True
    bot = DiscordBot("!", intents)

    print('=== Starting bot ...')

    @bot.event
    async def on_ready():
        print(f'=== Bot logged in as {bot.user} (ID: {bot.user.id})')
        logger.info(f"Bot logged in as {bot.user} (ID: {bot.user.id})")

    # Logging
    logfile_path = Path(__file__).parent / 'discordBot' / 'logs' / 'logging.log'
    logfile_path.parent.mkdir(parents=True, exist_ok=True)
    if not logfile_path.exists():
        logfile_path.touch()
    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)
    handler = logging.handlers.RotatingFileHandler(
        filename=str(logfile_path),
        encoding='utf-8',
        maxBytes=32 * 1024 * 1024,  # 32 MiB
        backupCount=5,   # Rotate through 5 files
    )
    dt_fmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    # Discord API
    discord_secret = getattr(settings, 'DISCORD_API_SECRET', None)
    if discord_secret is None:
        discord_secret = input('Enter discord_api_secret: ').strip()
    bot.run(discord_secret, log_handler=None)

    # Use for more freedom in async loop ... (more async funcs to run...)
    # async with bot:
    #    # Setup Logger? I suppose...
    #    await bot.start(settings.DISCORD_API_SECRET)


if __name__ == '__main__':
    start()