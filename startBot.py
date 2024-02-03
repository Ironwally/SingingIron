# This example requires the 'message_content' intent.
import os

# Imports
import settings
import discord
import logging
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
                print(f'\tFailed loading: {extension}\n\t\t{exc}')


def start():
    """Start Bot function"""
    # Bot Permissions
    intents = discord.Intents.default()
    intents.message_content = True
    bot = IronBot("!", intents)
    # Extensions already loaded via setup_hook

    print('=== Starting bot ...')

    @bot.event
    async def on_ready():
        print(f'=== Bot logged in as {bot.user} (ID: {bot.user.id})')
        logger.info(f"Bot logged in as {bot.user} (ID: {bot.user.id})")

    # Logging
    logger = settings.logging.getLogger("bot")
    bot.run(settings.DISCORD_API_SECRET, root_logger=True)

    # Use for more freedom in async loop ... (more async funcs to run...)
    # async with bot:
    #    # Setup Logger? I suppose...
    #    await bot.start(settings.DISCORD_API_SECRET)


if __name__ == '__main__':
    start()
