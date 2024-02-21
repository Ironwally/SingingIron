import json
import logging
from typing import Optional, Literal

import discord
from yt_dlp import YoutubeDL
from discord.ext import commands
from discord import app_commands
import validators


class music_shortcuts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(description='I like creampuffs now... Nom Nom Nom'
                                         '\nbling bang bang bong')
    async def bling(self, ctx: commands.Context):
        """I like creampuffs now... Nom Nom Nom \n bling bang bang bong"""
        ictx = ctx
        ictx.command = ctx.bot.get_command('play')
        print('now invoking command play, with arguments')
        await ctx.invoke(ctx.bot.get_command('play'), search='https://www.youtube.com/watch?v=210R0ozmLwg')

    @bling.error
    async def bling_error(self, ctx: commands.Context, error):
        """When catching the error this way, we only get a general hybrid-command-error with a string like
        description. And I don't want to go down checking strings..."""
        logging.error(f'Error while executing bling: {error}')
        await ctx.send('An Error occured. Check logger for more info.')
        return


async def setup(bot):
    await bot.add_cog(music_shortcuts(bot))
