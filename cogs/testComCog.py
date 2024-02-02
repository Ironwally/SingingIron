from typing import Optional, Literal

import discord
from discord.ext import commands
from discord import app_commands


class TestCogCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='ping', description='test the bot')
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("ping returned!")

    @commands.command()
    async def nohybrid(self, ctx: commands.Context):
        await ctx.send("Test Successful!")

    @commands.hybrid_command(name='hybridcommand')
    async def hybrid(self, ctx: commands.Context):
        await ctx.send("Hybrid Command!")


async def setup(bot):
    await bot.add_cog(TestCogCog(bot))
