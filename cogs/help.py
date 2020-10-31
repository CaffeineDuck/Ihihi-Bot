from discord.ext import commands
import discord
import os
import pymongo

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        """
        Checks if it is in a local machine
        """
        try:
            print(os.environ['TEST'])
            self.is_local = True
        except Exception:
            self.is_local = False

        """
        Mongo Db
        """
        self.mongoclient = os.environ['MONGOCLIENT']
        self.bot = pymongo.MongoClient(self.mongoclient)
        self.db = self.bot.ihihihibot_db
        if self.is_local:
            self.prefixes = self.db.server_test_prefixes
        else:
            self.prefixes = self.db.server_prefixes
  
    
    @commands.group(aliases=['_help'])
    async def help(self, ctx):
        if not ctx.invoked_subcommand:
            cur = self.prefixes.find_one({'server_id':ctx.guild.id})
            prefix = cur.get('prefix')
            server_name = cur.get('server_name')
            embed=discord.Embed(
            title=f'My Prefix for {server_name} is `{prefix}`',
            timestamp = ctx.message.created_at,
            colour = discord.Colour.gold())

            embed.set_thumbnail(url='')
            if ctx.channel.is_nsfw():
                embed.add_field(name= "Command categories are given below...",
                value = 
                f""" 
                1. Moderation Commands | `{prefix}help mod`\n 
                2. Fun Commands | `{prefix}help fun`\n
                3. Random Commands | `{prefix}help random`\n
                4. Other Commands | `{prefix}help other`\n
                5. NSFW Commands | `{prefix}help nsfw` \n
                """)
            else:
                embed.add_field(name= "Command categories are given below...",
                value = 
                f""" 
                1. Moderation Commands | `{prefix}help mod`\n 
                2. Fun Commands | `{prefix}help fun`\n
                3. Random Commands | `{prefix}help random`\n
                4. Other Commands | `{prefix}help other`\n
                """)
            embed.set_footer(text=f'Example: {prefix}help mod | Requested by {ctx.author}', icon_url='')
            await ctx.send(embed=embed)

    @help.command(aliases=['others', 'other', 'other commands', 'Others'])
    async def Other(self, ctx):
        cur = self.prefixes.find_one({'server_id':ctx.guild.id})
        prefix = cur.get('prefix')
        embed=discord.Embed(
        title="Other commands",
        description="All the other commands are listed below :-",
        timestamp = ctx.message.created_at,
        colour = discord.Colour.gold())
        embed.add_field(
            name=f"av | `{prefix}av <user>`", value="Shows your/ mentioned user's avatar.", inline= False)
        embed.add_field(
            name=f"gn | `{prefix}gn <user>`", value="Tells 'Goodnight'", inline= False)
        embed.add_field(
            name=f"bye | `{prefix}bye <user>`", value="Tells 'Good Bye Old Friend'", inline= False)
        embed.add_field(
            name=f"gg | `{prefix}gg <user>`", value="Tells 'Good Game'", inline= False)
        embed.add_field(
            name=f"henlo | `{prefix}henlo <user>`", value="Tells 'Hello'", inline= False)
        embed.add_field(
            name=f"say | `{prefix}say <user> <text>`", value="Sends the text in mentioned user's DM!", inline= False)

        embed.set_footer(text=f'Requested by {ctx.author}')
        embed.set_thumbnail(url='')
        await ctx.send(embed=embed)

    @help.command(aliases=['moderation', 'moderation commands', 'mod'])
    async def Moderation(self, ctx):
        cur = self.prefixes.find_one({'server_id':ctx.guild.id})
        prefix = cur.get('prefix')
        embed= discord.Embed(
        title="Moderation commands",
        description="All the moderation commands are listed below :-",
        timestamp = ctx.message.created_at,
        colour = discord.Colour.gold())

        embed.set_thumbnail(url='')
        embed.add_field(
            name=f"whois | `{prefix}whois`", 
            value="Gives info of the mentioned user/ message author.", inline= True)
        embed.add_field(
            name=f"ban | `{prefix}ban <user> <reason>`",
            value="Bans the mentioned user.", inline= False)
        embed.add_field(
            name=f"kick | `{prefix}kick <user> <reason>`",
            value="Kicks the mentioned user.", inline= False)
        embed.add_field(
            name=f"serverinfo | `{prefix}serverinfo`",
            value="Gives the info about current server.", inline= False)
        embed.add_field(
            name=f"warn | `{prefix}warn <user> <reason>`",
            value="Warns the mentioned user.", inline= False)
        embed.add_field(
            name=f"mute | `{prefix}mute <user> <time-in-minutes>`",
            value="Mutes the user | If used `mute <time>` mutes the user for specified time.")
        embed.add_field(
            name=f"purge | `{prefix}purge <no-of-messages>`", 
            value="Deletes give number of messages if you have the desired permissions", inline= False)
        embed.set_footer(text=f'Requested by {ctx.author}')
        await ctx.send(embed=embed)


    @help.command(aliases=['fun'])
    async def FunCommands(self, ctx):
        cur = self.prefixes.find_one({'server_id':ctx.guild.id})
        prefix = cur.get('prefix')
        embed=discord.Embed(
        title="Fun commands",
        description="All the fun commands are listed below :-",
        timestamp = ctx.message.created_at,
        colour = discord.Colour.gold())

        embed.set_thumbnail(url='')
        embed.add_field(
            name=f"slap | `{prefix}slap <user>`",
            value="slaps the mentioned person", inline= False)
        embed.add_field(
            name=f"kills | `{prefix}kill <user>`",
            value="kills the mentioned person", inline= False)
        embed.add_field(
            name=f"lick | `{prefix}lick <user>`",
            value="licks the mentioned person", inline= False)
        embed.add_field(
            name=f"hug | `{prefix}hug <user>`", 
            value="hugs the mentioned person", inline= False)
        embed.add_field(
            name=f"pat | `{prefix}pat <user>`",
            value="pats the mentioned person", inline= False)
        embed.set_footer(text=f'Requested by {ctx.author}')
        await ctx.send(embed=embed)


    @help.command(aliases=['nsfw'])
    @commands.is_nsfw()
    async def NSFWCommands(self, ctx):
        cur = self.prefixes.find_one({'server_id':ctx.guild.id})
        prefix = cur.get('prefix')
        embed = discord.Embed(
        title = "Custom Commands",
        description = "All the nsfw commands are listed below :-",
        timestamp = ctx.message.created_at,
        colour = discord.Colour.gold()
        )
        embed.set_thumbnail(url='')
        embed.add_field(
            name=f"ass | `{prefix}ass`", 
            value="Gives you a nice booty pic", inline= False)
        embed.add_field(
            name=f"pussy | `{prefix}pussy`", 
            value="Just some random cat pics :smirk:", inline= False)
        embed.add_field(
            name=f"creampie | `{prefix}pie`", 
            value="Just some cream in that pussy!", inline= False)
        embed.add_field(
            name=f"boobs | `{prefix}boobs`", 
            value="Big Boobies", inline= False)
        embed.add_field(
            name=f"Real | `{prefix}real`", 
            value="Sick of pornstars? Use this command!", inline= False)
        embed.add_field(
            name=f"Porn | `{prefix}porn`", 
            value="Want some porn?", inline= False)
        embed.add_field(
            name=f"Pieg | `{prefix}pieg`", 
            value="Hmm Some Gifs for that pie", inline= False)
        embed.add_field(
            name=f"Hentai | `{prefix}hentai`", 
            value="Who says porn is the best?", inline= False)
        embed.add_field(
            name=f"cum | `{prefix}cum`", 
            value="Want some cumsluts?", inline= False)
        embed.set_footer(text=f'Requested by {ctx.author}')
        await ctx.send(embed=embed)
    
    @help.command(aliases = ['random'])
    async def RandomCommands(self, ctx):
        cur = self.prefixes.find_one({'server_id':ctx.guild.id})
        prefix = cur.get('prefix')
        embed = discord.Embed(
        title = "Random Commands",
        description = "All the random commands are listed below :-",
        timestamp = ctx.message.created_at,
        colour = discord.Colour.gold()
        )
        embed.set_thumbnail(url='')
        embed.add_field(
            name=f"meme | `{prefix}meme`", 
            value="Sends you a good meme!", inline= False)
        embed.add_field(
            name=f"cursed | `{prefix}cursed`", 
            value="Is it cursed or is it you?", inline= False)
        embed.add_field(
            name=f"aww | `{prefix}aww`", 
            value="awwwwwwwwwwww", inline= False)
        embed.add_field(
            name=f"dog | `{prefix}dog`", 
            value="If you don't like dogs, you can go and die!", inline= False)
        embed.add_field(
            name=f"fox | `{prefix}fox`", 
            value="What does the fox say?", inline= False)
        embed.add_field(
            name=f"gayrate | `{prefix}gayrate`", 
            value="WHY ARE YOU GAE?", inline= False)
        embed.add_field(
            name=f"waifu | `{prefix}waifu`", 
            value="You are my best waifu :heart_eyes:", inline= False)
        embed.add_field(
            name=f"reddit | `{prefix}r <subreddit-name>`", 
            value="Fetches image from any subreddit you want!", inline= False)
        embed.set_footer(text=f'Requested by {ctx.author}')
        await ctx.send(embed=embed)
    
def setup(bot):
    bot.add_cog(Help(bot))
