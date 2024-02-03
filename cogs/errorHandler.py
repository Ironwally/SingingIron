from typing import Optional, Literal

import discord
from discord.ext import commands
from discord import app_commands


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener(name='NotOwner')
    async def on_command_error(self, error, interaction: discord.Interaction):
        if isinstance(error, commands.NotOwner):
            await interaction.response.send_message("Sorry! This command can only be run by an admin of the bot")
            print(f"Error occured! {error}")


async def setup(bot):
    await bot.add_cog(ErrorHandler(bot))
