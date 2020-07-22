import discord
from discord.ext import commands

from typing import Optional, Union
from datetime import datetime, timedelta
from asyncio import TimeoutError, wait, FIRST_COMPLETED

from utils import utils, rest_api


class TopCharts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.time_ranges = ('month', 'year', 'alltime')

    async def topchart(
        self, ctx, chart, time_range, 
        member_ids=None, guild_id=None, channel_id=None, game=None,
    ):
        result = await rest_api.get_top(
            self.bot, 
            chart, 
            time_range,
            member_ids=member_ids,
            guild_id=guild_id,
            channel_id=channel_id,
            game=game,
        )
        return result

    @commands.group(
        description="This is a command group that shows you the top chart of something", 
        name="top", 
        aliases=['t'], 
        invoke_without_command=True,
    )
    async def top(self, ctx):
        if not ctx.command.invoked_subcommand:
            await ctx.invoke(self.bot.get_command("help"), "top")

    # Top postcounts
    @top.command(
        description="Shows you who posted the most in the current `month/year/alltime`",
        name="postcounts", 
        aliases=["pc",],
    )
    async def top_postcounts(
        self, ctx, channel: Optional[discord.TextChannel]=None, time_range="month"
    ):
        if time_range not in self.time_ranges:
            raise commands.BadArgument
        channel = channel.id if channel else channel
        top_chart = await rest_api.get_top(
            self.bot, 
            "postcounts", 
            time_range,
            guild_id=ctx.guild.id,
            channel_id=channel,
        )
        user_ids = [i["user_id"] for i in top_chart["results"]]
        postcounts = [i["sum_postcount"] for i in top_chart["results"]]
        user_ids, postcounts = zip(*[
            (i["user_id"], i["sum_postcount"]) for i in top_chart["results"]
        ])
        user_ids = [
            await utils.get_member_name(
                self.bot, ctx.guild, i
            ) for i in user_ids
        ]
        table = utils.format_columns(postcounts, user_ids)

        embed = discord.Embed(
            title=f"Top postcounts for {time_range}",
            color=ctx.author.color,
            description=f"`{table}`", 
        )
        message = await ctx.send(embed=embed)
        await message.add_reaction("⏩")
        await message.add_reaction("⏪")
        
        def check(payload):
            return all((
                payload.user_id == ctx.author.id,
                payload.message_id == message.id,
                str(payload.emoji) in ["⏩", "⏪"],
            ))

        """done, pending = await wait([
                    bot.wait_for('raw_reaction_add')
                    bot.wait_for('raw_reaction_remove')
                ], return_when=FIRST_COMPLETED)

        try:
            stuff = done.pop().result()
        except ...:
            # if any of the tasks died for any reason,
            #  the exception will be replayed here.

        for future in pending:
            future.cancel()  # we don't need these anymore"""

        while True:
            try:
                payload = await self.bot.wait_for(
                    "raw_reaction_add", timeout=20.0, check=check
                ) 
                if str(payload.emoji) == "⏩" and top_chart["next"]:
                    top_chart = await rest_api.send_get(
                        self.bot, 
                        top_chart["next"], 
                        guild_id=ctx.guild.id,
                        channel_id=channel,
                    )
                    user_ids = [i["user_id"] for i in top_chart["results"]]
                    postcounts = [i["sum_postcount"] for i in top_chart["results"]]
                    user_ids, postcounts = zip(*[
                        (i["user_id"], i["sum_postcount"]) for i in top_chart["results"]
                    ])
                    user_ids = [
                        await utils.get_member_name(
                            self.bot, ctx.guild, i
                        ) for i in user_ids
                    ]
                    table = utils.format_columns(postcounts, user_ids)
                    embed.description=f"`{table}`"
                    await message.edit(embed=embed)
                elif str(payload.emoji) == "⏪" and top_chart["previous"]:
                    top_chart = await rest_api.send_get(
                        self.bot, 
                        top_chart["previous"], 
                        guild_id=ctx.guild.id,
                        channel_id=channel,
                    )
                    user_ids = [i["user_id"] for i in top_chart["results"]]
                    postcounts = [i["sum_postcount"] for i in top_chart["results"]]
                    user_ids, postcounts = zip(*[
                        (i["user_id"], i["sum_postcount"]) for i in top_chart["results"]
                    ])
                    user_ids = [
                        await utils.get_member_name(
                            self.bot, ctx.guild, i
                        ) for i in user_ids
                    ]
                    table = utils.format_columns(postcounts, user_ids)
                    embed.description=f"`{table}`"
                    await message.edit(embed=embed)
            except TimeoutError:
                await message.clear_reactions()
                break


def setup(bot):
    bot.add_cog(TopCharts(bot))
