import discord
import pymongo

from discord import Embed
from discord.ext import commands
from discord.ext.commands import has_permissions

class AutoResponse(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        