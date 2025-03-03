# Imports
import settings
import discord
import logging
import logging.handlers

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
    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)
    filename = 'discordBot/logs/logging.log'
    handler = logging.FileHandler(filename=filename, encoding='utf-8', mode='w')
    handlerNewer2 = logging.handlers.RotatingFileHandler(
        filename=filename,
        encoding='utf-8',
        maxBytes=32 * 1024 * 1024,  # 32 MiB
        backupCount=5,   # Rotate through 5 files
    )
    dt_fmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    discord_secret = settings.DISCORD_API_SECRET
    if discord_secret is None:
        print('Enter discord_api_secret: ')
        discord_secret = input()
    bot.run(discord_secret, log_handler=None)

    # Use for more freedom in async loop ... (more async funcs to run...)
    # async with bot:
    #    # Setup Logger? I suppose...
    #    await bot.start(settings.DISCORD_API_SECRET)


if __name__ == '__main__':
    start()