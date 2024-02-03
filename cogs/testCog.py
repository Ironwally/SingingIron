from typing import Optional, Literal

import discord
from discord.ext import commands
from discord import app_commands


class TestCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='check', description='Check/Test the bot')
    async def check(self, interaction: discord.Interaction):
        await interaction.response.send_message("Check successful!")


async def setup(bot):
    await bot.add_cog(TestCog(bot))