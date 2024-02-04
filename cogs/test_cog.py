from typing import Optional, Literal

import discord
from discord.ext import commands
from discord import app_commands


class Test_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='check', description='Check/Test the bot')
    @commands.is_owner()
    async def check(self, interaction: discord.Interaction):
        await interaction.response.send_message("Check successful!")


async def setup(bot):
    await bot.add_cog(Test_cog(bot))
