import discord
from discord.ext import tasks, commands
import os
import pymongo

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        """
        Checks if it is in a local machine
        """
        try:
            self.lol = os.environ['TEST']
            self.is_local = True
        except Exception:
            self.is_local = False

        """
        Mongo Db
        """
        self.mongoclient = os.environ['MONGOCLIENT']
        self.bot1 = pymongo.MongoClient(self.mongoclient)
        self.db = self.bot1.ihihihibot_db
        if self.is_local:
            self.prefixes = self.db.server_test_prefixes
        else:
            self.prefixes = self.db.server_prefixes
  
    
    @commands.group(aliases=['_help'])
    async def help(self, ctx):
        if not ctx.invoked_subcommand:
            cur = self.prefixes.find_one({'server_id':ctx.guild.id})
            prefix = cur.get('prefix')
            embed=discord.Embed(
            title=f'{self.bot.user.name} Support',
            timestamp = ctx.message.created_at,
            colour = discord.Colour.gold())

            embed.set_thumbnail(url='')
            if ctx.channel.is_nsfw():
                embed.add_field(name= f"Commands of {self.bot.user.name} are given below:",
                value = 
                f""" 
                1. Moderation Commands | `{prefix}help mod`\n 
                2. Fun Commands | `{prefix}help fun`\n
                3. Random Commands | `{prefix}help random`\n
                4. Magik Commands | `{prefix}help magik`\n
                5. Ask The Bot | `{prefix}help askthebot` \n
                6. Info Commands | `{prefix}help info` \n
                7. Config Commands | `{prefix}help config` \n
                8. Autoresponses | `{prefix}help autoresponse` \n 
                9. NSFW Commands | `{prefix}help nsfw` \n
                10. Other Commands | `{prefix}help other`\n
                """)
            else:
                embed.add_field(name= "Command categories are given below...",
                value = 
                f""" 
                1. Moderation Commands | `{prefix}help mod`\n 
                2. Fun Commands | `{prefix}help fun`\n
                3. Random Commands | `{prefix}help random`\n
                5. Ask The Bot | `{prefix}help askthebot` \n
                6. Info Commands | `{prefix}help info` \n
                7. Config Commands | `{prefix}help config` \n
                8. Autoresponses | `{prefix}help autoresponse` \n 
                9. Other Commands | `{prefix}help other`\n
                """)
            embed.add_field(
                name='‏', 
                value=f'‏Join our [support server](https://discord.gg/zKXZEs2N) | Invite [{self.bot.user.name}](https://discord.com/api/oauth2/authorize?client_id=767279203267379280&permissions=8&scope=bot)', inline=False)
            
            
            ##############################
            ## Didn't use it due to     ##
            ##    various reasons       ##
            ##############################
            """
            e = discord.Embed(title=f"**{self.bot.user.name} Command List!**", color=0x50C878)
            e.add_field(
                name=':scales: **Moderation**‎‏‏‎‎', 
                value=f'`{prefix}help mod`')
            e.add_field(
                name=':bowling: **Fun**', 
                value=f'`{prefix}help fun`')
            e.add_field(
                name=':dog: **Random**', 
                value=f'`{prefix}help random`')
            e.add_field(
                name=':camera: **Magik**', 
                value=f'`{prefix}help magik`')
            e.add_field(
                name=':v: **Info**', 
                value=f'`{prefix}help info`')
            e.add_field(
                name=':gear: **Config**', 
                value=f'`{prefix}help congig`')
            e.add_field(
                name=':computer: **Auto**', 
                value=f'`{prefix}help auto`')
            e.add_field(
                name=':smirk: **Ask Me**', 
                value=f'`{prefix}help askme`')
            e.add_field(
                name=':moneybag: Other‏‏‎‎', 
                value=f'`{prefix}help other`')

            if ctx.channel.is_nsfw():
                e.add_field(
                    name=':underage: NSFW‏‏‎‎', 
                    value=f'`{prefix}help nsfw`')
        
            e.add_field(
                name='‏', 
                value=f'‏Join our [support server](https://discord.gg/zKXZEs2N) | Invite [{self.bot.user.name}](https://discord.com/api/oauth2/authorize?client_id=767279203267379280&permissions=8&scope=bot)', inline=False)
            
            e.set_thumbnail(url= self.bot.user.avatar_url)
            e.set_footer(text = f'Requested by {ctx.author}', icon_url=self.bot.user.avatar_url)
            await ctx.send(embed=e)
            """
            ##############################
            ## Help commmand,But in a   ##
            ##    more compact way.     ##
            ##############################
           

            embed.set_footer(text = f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

    @help.command(aliases=['others', 'other', 'other commands', 'Others'])
    async def Other(self, ctx):
        cur = self.prefixes.find_one({'server_id':ctx.guild.id})
        prefix = cur.get('prefix')
        embed=discord.Embed(
        title="Other commands",
        description="All the other commands are listed below :",
        timestamp = ctx.message.created_at,
        colour = discord.Colour.gold())
        embed.add_field(
            name=f"gn | `{prefix}gn <user>`", 
            value="Tells 'Goodnight'", inline= False)
        embed.add_field(
            name=f"bye | `{prefix}bye <user>`", 
            value="Tells 'Good Bye Old Friend'", inline= False)
        embed.add_field(
            name=f"gg | `{prefix}gg <user>`", 
            value="Tells 'Good Game'", inline= False)
        embed.add_field(
            name=f"henlo | `{prefix}henlo <user>`", 
            value="Tells 'Hello'", inline= False)
        embed.add_field(
            name=f"say | `{prefix}say <user> <text>`", 
            value="Sends the text in mentioned user's DM!", inline= False)

        embed.set_footer(text=f'Requested by {ctx.author}')
        embed.set_thumbnail(url='')
        await ctx.send(embed=embed)


    @help.command(aliases=['moderation', 'moderation commands', 'mod'])
    async def Moderation(self, ctx):
        cur = self.prefixes.find_one({'server_id':ctx.guild.id})
        prefix = cur.get('prefix')
        embed= discord.Embed(
        title="Moderation commands",
        description="All the moderation commands are listed below :",
        timestamp = ctx.message.created_at,
        colour = discord.Colour.gold())
        embed.set_thumbnail(url='')

        embed.add_field(
            name=f"ban | `{prefix}ban <user> <reason>`",
            value="Bans the mentioned user.", inline= False)
        embed.add_field(
            name=f"kick | `{prefix}kick <user> <reason>`",
            value="Kicks the mentioned user.", inline= False)
        embed.add_field(
            name=f"warn | `{prefix}warn <user> <reason>`",
            value="Warns the mentioned user.", inline= False)
        embed.add_field(
            name=f"mute | `{prefix}mute <user> <time-in-minutes>(optional)`",
            value="Mutes the user | If used `mute <time>` mutes the user for specified time.")
        embed.add_field(
            name=f"purge | `{prefix}purge <user>(optional) <no-of-messages>`", 
            value="Deletes given number of messages if you have the desired permissions", inline= False)

        # embed.add_field(
        #     name=f"setwelcome | `{prefix}setwelcome <#channel>`", 
        #     value="Sets the channel as the welcomer channel.", inline= False)
        # embed.add_field(
        #     name=f"removewelcome | `{prefix}rwelcome <#channel>`", 
        #     value="Removes the channel as the welcomer channel.", inline= False)
        embed.add_field(
            name=f"nuke | `{prefix}nuke <#channel>`", 
            value="NUKES THE CHANNEL!", inline= False)    
        embed.set_footer(text=f'Requested by {ctx.author}')
        await ctx.send(embed=embed)


    @help.command(aliases=['fun'])
    async def FunCommands(self, ctx):
        cur = self.prefixes.find_one({'server_id':ctx.guild.id})
        prefix = cur.get('prefix')
        embed=discord.Embed(
        title="Fun commands",
        description="All the fun commands are listed below :",
        timestamp = ctx.message.created_at,
        colour = discord.Colour.gold())

        embed.set_thumbnail(url='')
        embed.add_field(
            name=f"slap | `{prefix}slap <user>`",
            value="slaps the mentioned person", inline= False)
        embed.add_field(
            name=f"kill | `{prefix}kill <user>`",
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
        embed.add_field(
            name=f"insult | `{prefix}insult <user>`",
            value="Insults the mentioned user", inline= False)
        embed.add_field(
            name=f"suk | `{prefix}suk <user>`", 
            value="Try it out", inline= False)

        embed.set_footer(text=f'Requested by {ctx.author}')
        await ctx.send(embed=embed)


    @help.command(aliases=['nsfw'])
    @commands.is_nsfw()
    async def NSFWCommands(self, ctx):
        cur = self.prefixes.find_one({'server_id':ctx.guild.id})
        prefix = cur.get('prefix')
        embed = discord.Embed(
        title = "NSFW Commands",
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
            name=f"reddit | `{prefix}r <subreddit-name>`", 
            value="Fetches image from any subreddit you want!", inline= False)
        embed.add_field(
            name=f"fakeperson | `{prefix}fakeperson`", 
            value="Gives you the image of person who doesn't exist in this world.", inline= False)
        embed.add_field(
            name=f"joke | `{prefix}joke`", 
            value="Gives you the WORST DAD JOKE!", inline= False)

        embed.set_footer(text=f'Requested by {ctx.author}')
        await ctx.send(embed=embed)

    @help.command(aliases = ['magik'])
    async def MagikCommands(self, ctx):
        cur = self.prefixes.find_one({'server_id':ctx.guild.id})
        prefix = cur.get('prefix')
        embed = discord.Embed(
        title = "Magik Commands",
        description = "All the magik commands are listed below :-",
        timestamp = ctx.message.created_at,
        colour = discord.Colour.gold())
        embed.set_thumbnail(url='')

        embed.add_field(
            name=f'{prefix}hitler | `{prefix}hitler <user>`',
            value="Adds the mentioned user's pfp in worse than hitler image.", inline= False)
        embed.add_field(
            name=f'{prefix}wanted | `{prefix}wanted <user>`',
            value="Adds the mentioned user's pfp in wanted image.", inline= False)
        
        embed.set_footer(text=f'Requested by {ctx.author}')
        await ctx.send(embed=embed)
    
    
    @help.command(aliases=['config'])
    async def settings(self, ctx):
        cur = self.prefixes.find_one({'server_id':ctx.guild.id})
        prefix = cur.get('prefix')
        embed = discord.Embed(
        title = "Config Commands",
        description = "Configure the bot according to your needs:",
        timestamp = ctx.message.created_at,
        colour = discord.Colour.gold())
        embed.set_thumbnail(url='')

        embed.add_field(
            name=f"prefix | `{prefix}prefix`",
            value="Gives you the prefix of the bot for this server.", inline= False)
        embed.add_field(
            name=f"changeprefix | `{prefix}changeprefix <new-prefix>`",
            value="Changes the prefix for this server.", inline= False)
        embed.add_field(
            name=f"addcommand | `{prefix}addcmd <command>`",
            value="Enables the command for the server if it is disabled.", inline= False)
        embed.add_field(
            name=f"removecommand | `{prefix}removecmd <command>`",
            value="Disables the command for the server if it is enabled.", inline= False)
        
        embed.set_footer(text=f'Requested by {ctx.author}')
        await ctx.send(embed=embed)
    
    @help.command(aliases=['autorspnse', 'autoresponses', 'auto'])
    async def autoresponse(self, ctx):
        cur = self.prefixes.find_one({'server_id':ctx.guild.id})
        prefix = cur.get('prefix')
        embed = discord.Embed(
        title = "Autoresponses",
        description = "Configure autoresponses according to your needs:",
        timestamp = ctx.message.created_at,
        colour = discord.Colour.gold())
        embed.set_thumbnail(url='')

        embed.add_field(
            name=f"f | `f`",
            value="Replies with 'f'", inline= False)
        embed.add_field(
            name=f"imagine | `imagine <text>`",
            value="Replies with 'f'", inline= False)
        embed.add_field(
            name=f"disable | `{prefix}disable <autoresponse>`",
            value="Replies with 'f'", inline= False)
        embed.add_field(
            name=f"disable | `{prefix}enable <autoresponse>`",
            value="Replies with 'f'", inline= False)

        embed.set_footer(text=f'Requested by {ctx.author}')
        await ctx.send(embed=embed)
    
    @help.command(aliases=['askme'])
    async def askthebot(self, ctx):
        cur = self.prefixes.find_one({'server_id':ctx.guild.id})
        prefix = cur.get('prefix')
        embed = discord.Embed(
        title = "Autoresponses",
        description = "Configure autoresponses according to your needs:",
        timestamp = ctx.message.created_at,
        colour = discord.Colour.gold())
        embed.set_thumbnail(url='')

        embed.add_field(
            name=f"gayrate | `{prefix}gayrate`", 
            value="WHY ARE YOU GAE?", inline= False)
        embed.add_field(
            name=f"waifu | `{prefix}waifu`", 
            value="You are my best waifu :heart_eyes:", inline= False)
        embed.add_field(
            name=f"anyone | `{prefix}anyone` | `{prefix}anyone <text>`",
            value="Chooses a random person in the server.", inline= False)

        
        await ctx.send(embed=embed)
    
    @help.command(aliases=['infos'])
    async def info(self, ctx):
        cur = self.prefixes.find_one({'server_id':ctx.guild.id})
        prefix = cur.get('prefix')
        embed = discord.Embed(
        title = "Info Commands",
        description = "Gives you the info!:",
        timestamp = ctx.message.created_at,
        colour = discord.Colour.gold())
        embed.set_thumbnail(url='')

        embed.add_field(
            name=f"whois | `{prefix}whois`", 
            value="Gives info of the mentioned user/ message author.", inline= False)
        embed.add_field(
            name=f"av | `{prefix}av <user>`", 
            value="Shows your/ mentioned user's avatar.", inline= False)
        embed.add_field(
            name=f"serverinfo | `{prefix}serverinfo`",
            value="Gives the info about current server.", inline= False)
        embed.add_field(
            name=f"botinfo | `{prefix}botinfo`",
            value="I will provide you my info.", inline= False)
        
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))
