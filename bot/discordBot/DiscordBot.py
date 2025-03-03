# Imports
import os
from discord.ext import commands


class DiscordBot(commands.Bot):
    def __init__(self, prefix, intents):
        super().__init__(command_prefix=f'{prefix}', intents=intents)
        # Bot Class automatically has commandTree

    async def setup_hook(self) -> None:
        # Load extensions, do more stuff ...
        print(f'=== Attempting to load extensions from cogs directory for bot: {self}...')
        await load_extensions(self)


async def load_extensions(bot):
    """Load extensions from cogs directory"""
    for filename in os.listdir('../cogs'):
        if filename.endswith('.py'):
            extension = filename[:-3]
            try:
                await bot.load_extension(f'cogs.{extension}')
                print(f'\tSuccessfully loaded: {extension}')
            except Exception as ex:
                exc = f'{type(ex).__name__}: {ex}'
                print(f'\tFailed to load: {extension}\n\t\t{exc}')