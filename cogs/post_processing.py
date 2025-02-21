import discord
from discord.ext import commands
from discord import app_commands
import os


class Post_processing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #cogs = app_commands.Group(name="cogs", description="Commands for loading, reloading and unloading cogs")

    @commands.group()
    async def cogs(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send("Group command not found")

    @cogs.command(description='Reload a cog')
    async def reload(self, ctx: commands.Context, cog: str = None):
        # Should be safe from code injection because of one-word-only argument. If not, lower code should fix.
        # if ctx.bot.get_cog(cog) is None: raise commands.BadArgument(
        #    "Error. This Cog does not exist or is not loaded.")
        if cog is None:
            # just reloads all cogs
            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    extension = filename[:-3]
                    try:
                        await ctx.bot.reload_extension(f'cogs.{extension}')
                        await ctx.send(f'\tSuccessfully reloaded: {extension}')
                    except Exception as ex:
                        exc = f'{type(ex).__name__}: {ex}'
                        await ctx.send(f'\tError reloading extension: {extension}')
            return
        cog = cog.lower()
        try:
            await self.bot.reload_extension(f'cogs.{cog}')
            await ctx.send(f"Reloaded cog: {cog}")
        except commands.ExtensionNotFound:
            await ctx.send(f"Cog: {cog} not found")
        except commands.BadArgument:
            await ctx.send("Error. Cog name does not exist.")
        except Exception as e:
            await ctx.send(f'Error: {e}')

    @cogs.command(description='List loaded cogs')
    async def list(self, ctx: commands.Context):
        extensions = (str(ex) for ex in self.bot.cogs.keys())
        await ctx.send(f"Loaded extensions:\t{', \t'.join(extensions)}")

    @cogs.command(description='load new extensions')
    async def load(self, ctx: commands.Context, cog: str = None):
        if cog:
            # load specified extensions
            pass
        else:
            # load all new extensions
            pass
        await ctx.send("extension post-loading not implemented jet.")


async def setup(bot):
    await bot.add_cog(Post_processing(bot))
