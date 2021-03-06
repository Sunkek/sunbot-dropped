"""Miscellaneous commands"""

import discord
from discord.ext import commands

from datetime import datetime

from utils import rest_api, helpers


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='ping', 
        description='Checks the delay between your message and bot response. Good for testing if the bot works.',
    )
    async def ping(self, ctx):
        desc = f'Latency {self.bot.latency:.5f}s'
        embed = discord.Embed(
            title='Pong!', 
            description=desc, 
            colour=ctx.author.color
            )
        await ctx.send(embed=embed)
        
    @commands.command(
        description="`info <member=you>` - shows information about the user.", 
        name='info',
        aliases = ["i"]
    )
    async def info(self, ctx, target: discord.Member=None):
        target = target or ctx.author
        embed = discord.Embed(
            color=target.color
        )
        # Avatar
        embed.set_author(name=str(target), icon_url=target.avatar_url)
        # Known info from database
        info = await rest_api.get_user_info(
            self.bot, 
            target.id
        )
        # Account creation date
        created = target.created_at
        ago = helpers.format_seconds((datetime.utcnow() - created).total_seconds())
        created = datetime.strftime(created, "%Y-%m-%d %H:%M:%S")
        embed.add_field(
            name=f'Account created', 
            value=f"{created}\n({ago} ago)"
        )
        # Server join date
        joined = target.joined_at
        ago = helpers.format_seconds((datetime.utcnow() - joined).total_seconds())
        joined = datetime.strftime(joined, "%Y-%m-%d %H:%M:%S")
        embed.add_field(
            name=f'Joined {ctx.guild.name}', 
            value=f"{joined}\n({ago} ago)"
        )
        result = [f'Avatar: [link]({target.avatar_url})']
        for key, value in info.items():
            if key == 'steam' and value:
                value = f'[link](https://steamcommunity.com/profiles/{value})'
            elif key == 'birthday' and value:
                value = datetime.strptime(value, "%Y-%m-%d").strftime("%d/%m/%Y")
            key = helpers.format_info_key(key)
            if value: 
                result.append(f'{key}: {value}')
        embed.add_field(
            name=f'Info', 
            value='\n'.join(result),
            inline=False
        )        

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Misc(bot))