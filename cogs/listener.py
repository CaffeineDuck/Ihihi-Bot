import discord
from discord.ext import commands
import os
import json
from PIL import Image, ImageDraw, ImageOps
from io import BytesIO
import pymongo
import asyncio

"""
Checks if it is in a local machine
"""
try:
    os.environ['TEST']
    is_local = True
except Exception:
    is_local = False

class events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        """
        Mongo Db
        """
        self.mongoclient = os.environ['MONGOCLIENT']
        self.bot_mongo = pymongo.MongoClient(self.mongoclient)
        self.db = self.bot_mongo.ihihihibot_db
        """
        As I host my bot, i have a testing bot and a main bot so it 
        fetches the prefix from database according to where its hosted!
        """
        if is_local:
            self.prefixes = self.db.server_test_prefixes
        else:
            self.prefixes = self.db.server_prefixes
        self.defualt_prefix = "."


    @commands.Cog.listener()
    async def on_member_join(self, member):
        
        data  = self.prefixes.find_one({'server_id' : member.guild.id})
        try:
            channel = data['welcome_channel']
        except Exception:
            return
        try:
            message = data['custom_message']
        except Exception:
            message = None

        if not channel:
            return

        channel = self.bot.get_channel(channel)

        avatar = member.avatar_url_as(format=None,static_format='png',size=1024)
        await avatar.save('./Other/Images/Manipulation/Avatar.png')
        im = Image.open(r'./Other/Images/Manipulation/Avatar.png').convert('RGB')
        im = im.resize((120, 120));
        bigsize = (im.size[0] * 3, im.size[1] * 3)
        mask = Image.new('L', bigsize, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(im.size, Image.ANTIALIAS)
        im.putalpha(mask)

        output = ImageOps.fit(im, mask.size, centering=(10, 10))
        output.putalpha(mask)
        output.save('./Other/Images/Manipulation/output.png')

        background = Image.open('./Other/Images/Manipulation/welcome.png').convert('RGB')
        background.paste(im, (149, 12), im)
        background.save('./Other/Images/Manipulation/overlap.png')
        await channel.send(file = discord.File("./Other/Images/Manipulation/overlap.png"))

        a = list(str(len(member.guild.members)))
        if '1' in a[-1]:
            ending = 'ˢᵗ'
        elif '2' in a[-1]:
            ending = 'ⁿᵈ'
        elif '3' in a[-1]:
            ending = 'ʳᵈ'
        else:
            ending = 'ᵗʰ'

        if not message or message.lower() == "None" or message.lower =="None":
            await channel.send(f'{member.mention} Welcome to **{member.guild.name}**. You are our {len(member.guild.members)}{ending} member!')
        else:
            await channel.send(f'{member.mention} {message}')

        """
        It updates the database whenever it joins a new guild!
        """
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        if self.prefixes.count_documents({'server_id' : guild.id}) == 0:
                perfix_data = {
                    'server_id' : guild.id,
                    'prefix' : self.defualt_prefix,
                    'server_name' : guild.name,
                    'welcome_channel': None,
                    'custom_message': None,
                }
                self.prefixes.insert_one(perfix_data)
                star()
                print(f"Prefix for server id {guild.id} has been created!")
                star()

def setup(bot):
    bot.add_cog(events(bot))