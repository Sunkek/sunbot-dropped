"""This cog sends custom emoji usage to the database."""

import discord
from discord.ext import commands
from datetime import datetime

import re

from utils import rest_api

class TrackEmoji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # I don't want to save info about DMs and webhooks
        if message.guild and message.guild.get_member(message.author.id):
            if self.bot.settings.get(message.guild.id, {}).get("track_emotes"):
                """<:Warframe:702046236085321789>"""
                p = re.compile("<:[\w]:[\d]>")
                emoji = p.match(message.content)
                if emoji:
                    print(emoji)
                    """await rest_api.add_emotes(
                        self.bot, 
                        guild_id=message.guild.id,
                        channel_id=message.channel.id,
                        user_id=message.author.id,
                        postcount=1,
                        attachments=len(message.attachments),
                        words=len(message.content.split()),
                        period=datetime.now().strftime("%Y-%m-%d")
                    )"""
        

def setup(bot):
    bot.add_cog(TrackEmoji(bot))