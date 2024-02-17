import json
from typing import Optional, Literal

import discord
from yt_dlp import YoutubeDL
from discord.ext import commands
from discord import app_commands
import validators


class Voice_and_sound(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(description='join channel')
    async def join(self, ctx: commands.Context):
        if ctx.author.voice is None:
            await ctx.send('You need to be in a channel to use this command!')
            return

        channel = ctx.author.voice.channel
        # Get or create voice client for guild
        voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        if voice_client is None:
            voice_client = await channel.connect()
        else:
            # noinspection PyUnresolvedReferences
            await voice_client.move_to(channel)

    @commands.hybrid_command(description='give me music')
    async def play(self, ctx: commands.Context, *, search):
        """Play a song in the voice channel"""

        def format_selector(ctx):
            """ Select best audio quality"""

            # formats are already sorted worst to best
            formats = ctx['formats'][::-1]

            # find compatible audio extension
            audio_ext = {'mp4': 'm4a', 'webm': 'webm'}

            # vcodec='none' means there is no video
            # filter vcodec
            def notvideo(format):
                return format['vcodec'] == 'none'

            formats_no_videos = list(filter(notvideo, formats))
            return formats_no_videos[0]  # We assume that the top is the best choice. (is audio and best, so...)

        if search is None:
            await ctx.send('Please provide a name or url')

        # Connect to voice channel if not already
        voice_client = ctx.voice_client
        if voice_client is None:
            ictx = ctx
            ictx.command = ctx.bot.get_command('join')
            await ctx.bot.invoke(ictx)
            voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        await ctx.send('Fetching...')

        ydl_opts = {
            'format': 'm4a/bestaudio/best',  # Preffered format and fallbacks
            # help(yt-dlp.postprocessors) for list of available postprocessors and their arguments
            'postprocessors': [{  # Extract audio using ffmpeg
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'm4a',
            }]
        }

        ydl_opts = {
            'format': 'm4a/bestaudio',
        }

        with YoutubeDL(ydl_opts) as ydl:
            # Get Youtube url
            if validators.url(search):
                info = ydl.extract_info(search, download=False)
                video = info
            else:
                info = ydl.extract_info("ytsearch: " + search, download=False)
                video = info['entries'][0]

            await ctx.send(f'Playing {video['title']} by {video['channel']}!')

            # Play sound from url using ffmpeg
            ffmpeg_opts = {'before_options': '-reconnect 1 -reconnect_streamed 1',
                           'options': '-vn'}

            best_format = format_selector(video)
            url = best_format['url']
            source = discord.FFmpegPCMAudio(source=url, **ffmpeg_opts)
            post_processed = discord.PCMVolumeTransformer(source, volume=0.2)
            voice_client.play(post_processed)

    @commands.hybrid_command(description='stop the music')
    async def stop(self, ctx: commands.Context):
        """Stop music"""
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send('Music stopped.')
        else:
            await ctx.send('No music currently playing.')

    @commands.hybrid_command(description='pause music')
    async def pause(self, ctx: commands.Context):
        """Pause music"""
        if not ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send('Music paused.')
        else:
            await ctx.send('No music currently playing.')

    @commands.hybrid_command(description='resume paused music')
    async def resume(self, ctx: commands.Context):
        """Resume music"""
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send('Music resumed.')
        else:
            await ctx.send('No music paused.')

    @commands.hybrid_command(description='disconnect bot from voice channel \n short: !dis',
                             aliases=['dis'])
    async def disconnect(self, ctx: commands.Context, force: Optional[Literal["f"]] = None):
        """Disconnect bot from voice channel"""
        force = True if force is not None else False
        if ctx.voice_client and ctx.voice_client.is_connected():
            await ctx.voice_client.disconnect(force=force)
        else:
            await ctx.send('Not connected to voice channel.')

    @play.error
    async def no_search_term_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Missing search_term or url')
            return

    @join.error
    async def voice_join_error(self, ctx: commands.Context, error):
        """When catching the error this way, we only get a general hybrid-command-error with a string like
        description. And I don't want to go down checking strings..."""
        await ctx.send(error)
        return


async def setup(bot):
    await bot.add_cog(Voice_and_sound(bot))
