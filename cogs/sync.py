from typing import Optional, Literal

import discord
from discord.ext import commands
from discord import app_commands


class SyncCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Sync Slash-Commands with Discord",
                      help="""
                            sync [s/c/r]
                            c -> copy global to guild and sync, 
                            r -> remove all commands from tree (and guild) and sync  
                            g -> sync globally
                            s/none -> only sync local guild
                            or
                            sync guild-id_1 guild-id_2 ...
                        """)
    @commands.guild_only()
    @commands.is_owner()
    async def sync(self, ctx: commands.Context, guilds: commands.Greedy[discord.Object],
                   spec: Optional[Literal["s", "c", "r", "g"]] = None) -> None:
        if not guilds:
            if spec == "c":
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "r":
                ctx.bot.tree.clear_commands(guild=ctx.guild)
                await ctx.bot.tree.sync(guild=ctx.guild)
                synced = []
            elif spec == "g":
                synced = await ctx.bot.tree.sync()
            else:
                synced = await ctx.bot.tree.sync(guild=ctx.guild)

            await ctx.send(
                f"Synced {len(synced)} commands {'globally' if spec == 'g' else 'to the current guild.'}"
            )
            return

        ret = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException:
                pass
            else:
                ret += 1

        await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

    @sync.error
    async def sync_error(self, error, interaction: discord.Interaction):
        if isinstance(error, commands.NotOwner):
            await interaction.response.send_message("Sorry! This command can currently only be used by the owner.")


async def setup(bot):
    await bot.add_cog(SyncCog(bot))
