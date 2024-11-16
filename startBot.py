# Imports
import settings
import discord
import logging
import logging.handlers
import os
from discord.ext import commands


class IronBot(commands.Bot):
    def __init__(self, prefix, intents):
        super().__init__(command_prefix=f'{prefix}', intents=intents)
        # Bot Class automatically has commandTree

    async def setup_hook(self) -> None:
        # Load extensions, do more stuff ...
        print(f'=== Attempting to load extensions from cogs directory for bot: {self}...')
        await load_extensions(self)


async def load_extensions(bot):
    """Load extensions from cogs directory"""
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            extension = filename[:-3]
            try:
                await bot.load_extension(f'cogs.{extension}')
                print(f'\tSuccessfully loaded: {extension}')
            except Exception as ex:
                exc = f'{type(ex).__name__}: {ex}'
                print(f'\tFailed to load: {extension}\n\t\t{exc}')


def start():
    """Start Bot function"""
    # Bot Permissions
    intents = discord.Intents.default()
    intents.message_content = True
    intents.voice_states = True
    bot = IronBot("!", intents)

    print('=== Starting bot ...')

    @bot.event
    async def on_ready():
        print(f'=== Bot logged in as {bot.user} (ID: {bot.user.id})')
        logger.info(f"Bot logged in as {bot.user} (ID: {bot.user.id})")

    # Logging
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename='logs/logging.log', encoding='utf-8', mode='w')
    handlerNewer2 = logging.handlers.RotatingFileHandler(
        filename='logs/logging.log',
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
        print('enter discord_api_secret: ')
        discord_secret = input()
    bot.run(discord_secret, log_handler=None)

    # Use for more freedom in async loop ... (more async funcs to run...)
    # async with bot:
    #    # Setup Logger? I suppose...
    #    await bot.start(settings.DISCORD_API_SECRET)


if __name__ == '__main__':
    start()
