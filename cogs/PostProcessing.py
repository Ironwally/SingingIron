import discord
from discord.ext import commands
from discord import app_commands
import os


class PostProcessing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    cogs = app_commands.Group(name="cogs", description="Commands for loading, reloading and unloading cogs")

    @cogs.command(description='Reload a cog')
    async def reload(self, interaction: discord.Interaction, cog: str):
        try:
            if not cog in [cogg[:-3] for cogg in os.listdir('./cogs')]: raise commands.BadArgument(
                "Error. Cog name does not exist.")
            await self.bot.reload_extension(f'cogs.{cog}')
            await interaction.response.send_message(f"Reloaded cog: {cog}")
        except commands.ExtensionNotLoaded:
            await interaction.response.send_message(f"Cog: {cog} could not be reloaded")
        except commands.ExtensionNotFound:
            await interaction.response.send_message(f"Cog: {cog} not found")
        except commands.BadArgument:
            await interaction.response.send_message("Error. Cog name does not exist.")
        except Exception as e:
            await interaction.response.send_message(f"An error occurred while reloading cog {cog}: {e}")

    @cogs.command(description='List loaded cogs')
    async def list(self, interaction: discord.Interaction):
        extensions = (str(ex) for ex in self.bot.cogs.keys())
        await interaction.response.send_message(f"Loaded extensions:\t{", \t".join(extensions)}")

    @cogs.command(description='load new extensions')
    async def load(self, interaction: discord.Interaction, cog: str = None):
        if cog:
            # load specified extensions
            pass
        else:
            # load all new extensions
            pass
        await interaction.response.send_message("extension post-loading not implemented jet.")


async def setup(bot):
    await bot.add_cog(PostProcessing(bot))
