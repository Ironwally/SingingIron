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
                            s -> sync only, 
                            c -> copy global to guild and sync, 
                            r -> remove all commands from tree (and guild) and sync  
                            or
                            sync guild-id_1 guild-id_2 ...
                        """)
    @commands.guild_only()
    @commands.is_owner()
    async def sync(self, ctx: commands.Context, guilds: commands.Greedy[discord.Object],
                   spec: Optional[Literal["s", "c", "r"]] = None) -> None:
        if not guilds:
            if spec == "s":
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "c":
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "r":
                ctx.bot.tree.clear_commands(guild=ctx.guild)
                await ctx.bot.tree.sync(guild=ctx.guild)
                synced = []
            else:
                synced = await ctx.bot.tree.sync()

            await ctx.send(
                f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
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


async def setup(bot):
    await bot.add_cog(SyncCog(bot))
