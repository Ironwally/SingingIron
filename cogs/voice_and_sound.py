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
        try:
            await voice.channel.connect()  # auto-sets good standard values and joins authors voicechannel
        except commands.CommandInvokeError:
            await ctx.send('Error joining voice channel. Join a channel first.')

    #@join.error
    #async def author_not_in_voice(self, error, ctx: commands.Context):
    #    print(f'error: {error}')
    #    if isinstance(error, commands.HybridCommandError):
    #        await ctx.send(f'Error joining channel: {error}')


async def setup(bot):
    await bot.add_cog(Voice_and_sound(bot))
