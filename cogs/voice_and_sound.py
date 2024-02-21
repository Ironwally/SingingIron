import logging
from typing import Optional, Literal

import discord
from yt_dlp import YoutubeDL
from discord.ext import commands
from discord import app_commands
import validators


class Voice_and_sound(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.loop = False

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
        await ctx.send('Joined voice channel.')

    @join.error
    async def join_error(self, ctx: commands.Context, error):
        """When catching the error this way, we only get a general hybrid-command-error with a string like
        description. And I don't want to go down checking strings..."""
        logging.error(f'Error while executing join: {error}')
        await ctx.send('An error occured. Please check logger for more info.')
        return

    @commands.hybrid_command(description='disconnect bot from voice channel \n short: dis',
                             aliases=['dis'])
    async def disconnect(self, ctx: commands.Context, force: Optional[Literal["f"]] = None):
        """Disconnect bot from voice channel"""
        force = True if force is not None else False
        if ctx.voice_client and ctx.voice_client.is_connected():
            await ctx.voice_client.disconnect(force=force)
        else:
            await ctx.send('Not connected to voice channel.')

    def play_next(self, ctx: commands.Context):
        """Get next song and invoke it"""
        if self.loop:
            ctx.invoke(ctx.bot.get_command('play'))
        else:
            # Invoke next song, when implemented
            pass

    @commands.hybrid_command(description='give me music')
    async def play(self, ctx: commands.Context, *, search):
        """Play a song in the voice channel"""

        def format_selector(cntx):
            """ Select best audio quality"""

            # formats are already sorted worst to best
            formats = cntx['formats'][::-1]

            # find compatible audio extension
            audio_ext = {'mp4': 'm4a', 'webm': 'webm'}

            # vcodec='none' means there is no video
            # filter vcodec
            def notvideo(vformat):
                return vformat['vcodec'] == 'none'

            formats_no_videos = list(filter(notvideo, formats))
            return formats_no_videos[0]  # We assume that the top is the best choice. (is audio and best, so...)

        if search is None:
            await ctx.send('Please provide a name or url')

        # Connect to voice channel if not already
        voice_client = ctx.voice_client
        if voice_client is None:
            await ctx.invoke(ctx.bot.get_command('join'))
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

            # Equalizer...
            # more post processing...

            if voice_client.is_playing():
                voice_client.stop()

            voice_client.play(post_processed, after=self.play_next(ctx))

            # -> Implement Queue mit/und Database

    @play.error
    async def play_error(self, ctx: commands.Context, error):
        logging.error(f'Error while executing play: {error}')
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Missing search_term or url')
        else:
            print(f'Error while executing play: {error}')
            await ctx.send('An error occured. Please check logger for more info.')
            return

    @commands.hybrid_command(description='stop the music')
    async def stop(self, ctx: commands.Context):
        """Stop music"""
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send('Music stopped.')
        else:
            await ctx.send('No music currently playing.')

    @commands.hybrid_command(description='pause music',
                             aliases=['p'])
    async def pause(self, ctx: commands.Context):
        """Pause music"""
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send('Music paused.')
        else:
            await ctx.send('No music currently playing.')

    @commands.hybrid_command(description='resume paused music',
                             aliases=['re'])
    async def resume(self, ctx: commands.Context):
        """Resume music"""
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send('Music resumed.')
        else:
            await ctx.send('Music is not paused')

    @commands.hybrid_command(description='Loop the playing song',
                             aliases=['l'])
    async def loop(self, ctx: commands.Context):
        """Loop the playing song"""
        if self.loop:
            self.loop = False
            await ctx.send('Song looping deactivated.')
        else:
            self.loop = True
            await ctx.send('Looping current song.')
        # Looping implemented via play_next function bool
        # Implement via looping in current song in database?


async def setup(bot):
    await bot.add_cog(Voice_and_sound(bot))
