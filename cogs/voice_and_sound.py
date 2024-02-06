from typing import Optional, Literal

import discord
from discord.ext import commands
from discord import app_commands


class Voice_and_sound(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(description='join channel')
    async def join(self, ctx: commands.Context):
        voice = ctx.author.voice
        await voice.channel.connect()  # auto-sets good standard values and joins authors voicechannel

    @join.error
    async def author_not_in_voice(self, ctx: commands.Context, error):
        """When catching the error this way, we only get a general hybrid-command-error with a string like
        description. And I don't want to go down checking strings..."""
        if isinstance(error, commands.HybridCommandError):
            await ctx.send(f'Error joining voice channel. Maybe join a channel first.')

    @commands.hybrid_command(description='give me music')
    async def play(self, ctx: commands.Context):
        #self.bot.activity = discord.Spotify
        pass


async def setup(bot):
    await bot.add_cog(Voice_and_sound(bot))
