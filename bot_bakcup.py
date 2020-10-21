import requests
import json
import discord
from discord.ext import commands, tasks
from discord.utils import get
import datetime
import random
import aiohttp
import praw
from PIL import Image
from io import BytesIO
from decouple import config
import pytz
import os


reddit = praw.Reddit(client_id ='0KxXFz3MNhqqQg',
					 client_secret ='Pz-9kbsz3Uh8PpDGJ6I_51B19Lg',
					 username = 'Samrid_',
					 password = config('PASSWORD'),
					 user_agent = "python_praw")

# subreddit = reddit.subreddit("memes")

# hot = subreddit.hot(limit=5)

# for submission in hot:
#     print(submission.title)

intents = discord.Intents.default()
intents.members = True

#Class For actual Bot management
#Variables
token = config('TOKEN')

#Declaring Prefix
client = commands.Bot(command_prefix=".", case_insensitive=True, intents=intents)


#Class to get the list of applicable members
class applicable_members:

    #Variables
    people = []
    role_name = "Mods"
    bots=[767279203267379280 ,270904126974590976, 751026843687321660]
    member={}

    def api(people, mee6API, member):

        #Gets the data from api
        result = requests.get(mee6API).json()

        #Gets specific data related to members
        players = result.get("players")

        #Loop to form dict of player and their xp
        for player in players:
            member[player.get("xp")] = player.get("id")

        #List of user-id of people illegible to get Mod role
        people = list(member.values())[:3]

        #Returns
        return(people)



class samrid_bot:

	@client.event
	async def on_ready():
		print("Bot is ready")
				
	@client.event
	async def on_message(message):

		#Checks If the messager isn't bot
		if message.author.bot == True:
			pass
		else:
			#Response to imagine
			if "imagine" == message.content.split()[0]:
				await message.channel.send("I can't even " + message.content +", bro!")

			#Response to f
			elif "f" == message.content.lower():
				await message.channel.send("f")
			
			#Response to no u
			elif "no u" == message.content.lower():
				await message.channel.send("no u")
			
			#Response to .hello there
			elif ".hello there" == message.content.lower() or "hello there" == message.content.lower():
				await message.channel.send("General Kenobi")
			
			#Response to shh
			elif "shh" == message.content.lower().split()[0] or ".shh" == message.content.lower().split()[0]:
				await message.channel.send(":shushing_face:")

			elif ".test" == message.content:
				await message.channel.send(message)
				await message.channel.send(message.author)
			
		#Send the message to command processor 
		await client.process_commands(message)
			

	
	@client.command()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def waifu(ctx,input=None):
		waifu = str(random.randrange(1,10))
		if input == None:
			await ctx.send(ctx.author.mention + " You are " + waifu + "/10 waifu!")
		else:
			await ctx.send(input + " is " + waifu + "/10 waifu!")
	
	@client.command()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def suk(ctx,input=None):
		if input == None:
			await ctx.send(ctx.author.mention + " How alone can you be to not even find a person in discord for making him/her suck your dick virtually?")
		else:
			await ctx.send(input + " Suck " + ctx.author.mention + "'s Dick!")
	
	@client.command()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def gg(ctx, input=None):
		if input == None:
			await ctx.send("Good Game Well Played")
		else:
			await ctx.send("Good Game Well Played "+input)

	@client.command()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def henlo(ctx, input=None):
		if input == None:
			await ctx.send("Fuck you! " + ctx.author.mention)
		else:
			await ctx.send("Fuck you! " + input )
	
	@client.command()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def byy(ctx, input=None):
		if input == None:
			await ctx.send("Lonenly ass, you are lonely that you need goodnight from a bot! " + ctx.author.mention)
		else:
			await ctx.send("Goodbye Old Friend " + input)
	
	#Removed Help Command
	client.remove_command('help')

	#ERRORS
	@client.event
	async def on_command_error(ctx, error):
		if isinstance(error, commands.NSFWChannelRequired):
			image = "https://i.imgur.com/oe4iK5i.gif"
			embed = discord.Embed(title="NSFW not allowed here", description = "Use NSFW commands in a NSFW marked channel (look in channel settings, dummy")
			embed.set_image(url=image)
			embed.set_footer(text="GOTO NSFW CHANNEL DUMBASS" )
			await ctx.send(embed=embed)
		elif isinstance(error, commands.RoleNotFound):
			await ctx.send("Role not found!")
		elif isinstance(error, commands.MissingRequiredArgument):
			await ctx.send("Please add the missing arguments!")
		elif isinstance(error, commands.CommandInvokeError):
			await ctx.send(error)
		elif isinstance(error, commands.CommandOnCooldown):
			await ctx.send(f"Wait for a while dumbass! {ctx.author.mention} {error}.")
		else:
			raise error


	#ROUTINE 
	@client.command()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def routine(ctx):
		image = "https://cdn.discordapp.com/attachments/766213304846647309/768311655306100766/routine.png"
		embed = discord.Embed(title="Routine")
		embed.set_image(url=image)
		embed.set_footer(text="I want to DIE!" )
		await ctx.send(embed=embed)
	
	#test
	@client.command()
	@commands.cooldown(1, 30, commands.BucketType.user)
	async def test(ctx):
		image = "https://media0.giphy.com/media/W5C9c8nqoaDJWh34i6/giphy.gif"
		embed = discord.Embed(title="Routine")
		embed.set_image(url=image)
		embed.set_footer(text="I want to DIE!" )
		await ctx.send(embed=embed)
		
	
	#OOF
	@client.command()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def oof(ctx):
		image = "https://cdn.discordapp.com/attachments/766213304846647309/768001025989935124/oof.jpg"
		embed = discord.Embed(title="OOOOOOOFFF")
		embed.set_image(url=image)
		embed.set_footer(text="Sucks To Be you!" )
		await ctx.send(embed=embed)
		

	
	@client.command()
	@commands.cooldown(1, 5, commands.BucketType.user)
	#Random Fox Generator
	async def fox(ctx):
		async with aiohttp.ClientSession() as cs:
			async with cs.get ("https://randomfox.ca/floof/") as r:
				data = await r.json()
				image = data.get("image")
		embed = discord.Embed(title="What does the fox say?")
		embed.set_image(url=image)
		embed.set_footer(text="https://randomfox.ca")
		await ctx.send(embed=embed)
	
	@client.command()
	@commands.cooldown(1, 5, commands.BucketType.user)
	#Random dog Generator
	async def dog(ctx):
		async with aiohttp.ClientSession() as cs:
			async with cs.get ("https://dog.ceo/api/breeds/image/random") as r: 
				data = await r.json()
				image = data.get("message")
		embed = discord.Embed(title="Henlo")
		embed.set_image(url=image)
		embed.set_footer(text="https://dog.ceo/")
		await ctx.send(embed=embed)

	@client.command(aliases = ['memes', 'funny'])
	@commands.cooldown(1, 5, commands.BucketType.user)
	#Memes Sender
	async def meme(ctx):
		subreddit = reddit.subreddit("memes")
		all_subs = [] 
		hot = subreddit.hot(limit=50)

		for submission in hot:
			all_subs.append(submission)
		
		random_sub = random.choice(all_subs)

		name = random_sub.title
		link = random_sub.url

		embed = discord.Embed(title=name)
		embed.set_image(url=link)

		await ctx.send(embed=embed)
	
	@client.command()
	@commands.cooldown(1, 5, commands.BucketType.user)
	@commands.is_nsfw()
	#Memes Sender
	async def ass(ctx):
		
		subreddit = reddit.subreddit("ass")
		all_subs = [] 
		hot = subreddit.hot(limit=100)

		for submission in hot:
			all_subs.append(submission)
		
		random_sub = random.choice(all_subs)

		name = random_sub.title
		link = random_sub.url

		embed = discord.Embed(title=name)
		embed.set_image(url=link)
		
		await ctx.send(embed=embed)

	@client.command(aliases=['boobies', 'bobs'])
	@commands.cooldown(1, 5, commands.BucketType.user)
	@commands.is_nsfw()
	async def boobs(ctx):
		
		subreddit = reddit.subreddit("boobs")
		all_subs = [] 
		hot = subreddit.hot(limit=100)

		for submission in hot:
			all_subs.append(submission)
		
		random_sub = random.choice(all_subs)

		name = random_sub.title
		link = random_sub.url

		embed = discord.Embed(title=name)
		embed.set_image(url=link)
		
		await ctx.send(embed=embed)
	
	@client.command(aliases=['r'], pass_context=True)
	async def reddit(ctx, subrd="memes"):
		
		subreddit = reddit.subreddit(subrd)
		all_subs = [] 
		hot = subreddit.hot(limit=100)

		for submission in hot:
			all_subs.append(submission)
		
		random_sub = random.choice(all_subs)

		name = random_sub.title
		link = random_sub.url

		embed = discord.Embed(title=name)
		embed.set_image(url=link)
		
		await ctx.send(embed=embed)
	
	@client.command()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def cursed(ctx):
		
		subreddit = reddit.subreddit('cursedcomments')
		all_subs = [] 
		hot = subreddit.hot(limit=100)

		for submission in hot:
			all_subs.append(submission)
		
		random_sub = random.choice(all_subs)

		name = random_sub.title
		link = random_sub.url

		embed = discord.Embed(title=name)
		embed.set_image(url=link)
		
		await ctx.send(embed=embed)
	
	@client.command(aliases = ['vagena'])
	@commands.cooldown(1, 5, commands.BucketType.user)
	@commands.is_nsfw()
	async def pussy(ctx):
		
		subreddit = reddit.subreddit("pussy")
		all_subs = [] 
		hot = subreddit.hot(limit=100)

		for submission in hot:
			all_subs.append(submission)
		
		random_sub = random.choice(all_subs)

		name = random_sub.title
		link = random_sub.url

		embed = discord.Embed(title=name)
		embed.set_image(url=link)
		
		await ctx.send(embed=embed)
	
	@client.command(aliases = ['real_girls', 'nudes'])
	@commands.cooldown(1, 5, commands.BucketType.user)
	@commands.is_nsfw()
	async def real(ctx):
		
		subreddit = reddit.subreddit("RealGirls")
		all_subs = [] 
		hot = subreddit.hot(limit=100)

		for submission in hot:
			all_subs.append(submission)
		
		random_sub = random.choice(all_subs)

		name = random_sub.title
		link = random_sub.url

		embed = discord.Embed(title=name)
		embed.set_image(url=link)
		
		await ctx.send(embed=embed)
	
	
	@client.command(aliases = ['cum', 'cumsluts'])
	@commands.cooldown(1, 5, commands.BucketType.user)
	@commands.is_nsfw()
	async def cumshot(ctx):
		subreddit = reddit.subreddit("cumsluts")
		all_subs = [] 
		hot = subreddit.hot(limit=100)

		for submission in hot:
			all_subs.append(submission)
		
		random_sub = random.choice(all_subs)

		name = random_sub.title
		link = random_sub.url

		embed = discord.Embed(title=name)
		embed.set_image(url=link)
		
		await ctx.send(embed=embed)
	
	@client.command()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def wanted(ctx, user: discord.Member = None):
		if user == None:
			user = ctx.author
		
		wanted = Image.open('Images/wanted.jpg')
		asset = user.avatar_url_as(size=128)
		data = BytesIO(await asset.read())
		pfp = Image.open(data)
		pfp = pfp.resize((395, 395))
		wanted.paste(pfp, (269,451))
		wanted.save("wanted.png")
		await ctx.send(file = discord.File("wanted.png"))
	
	@client.command()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def hitler(ctx, user: discord.Member = None):
		if user == None:
			user = ctx.author
		
		wanted = Image.open('Images/hitler.jpg')
		asset = user.avatar_url_as(size=128)
		data = BytesIO(await asset.read())
		pfp = Image.open(data)
		pfp = pfp.resize((194, 194))
		wanted.paste(pfp, (56,56))
		wanted.save("hitler.png")
		await ctx.send(file = discord.File("hitler.png"))

	@client.command(aliases=['user', 'info'])
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def whois(ctx, user: discord.Member = None):
		if user == None:
			user = ctx.author

		embed = discord.Embed(title = f"{user.name}#{user.discriminator}", description = user.mention, colour = discord.Color.blue())
		mentions = [role.mention for role in user.roles]
		no_of_roles = len(mentions)
		roles = str(mentions).replace('[', '').replace(']','').replace("\'",'').replace(',','')
		created_at = user.created_at.strftime("%b %d, %Y")
		joined_at = user.joined_at.strftime("%b %d, %Y")
		nepal_time = pytz.timezone("Asia/Kathmandu")
		time_now = ctx.message.created_at.astimezone(nepal_time)
		message_created = time_now.strftime("%H:%M %p")
		

		embed.add_field(name= "**Joined**", value = joined_at  , inline = True)
		embed.add_field(name= "**Registered**", value = created_at  , inline = True)
		embed.add_field(name= f"**Roles**[{no_of_roles}]", value = roles  , inline = False)
		embed.set_thumbnail(url=user.avatar_url)
		embed.set_footer(text = f"ID: {user.id} • Today at {message_created}")
		await ctx.send(embed=embed)
		
	@client.command()
	async def mod(ctx):
		#Variables
		mee6API = "https://mee6.xyz/api/plugins/levels/leaderboard/"+str(ctx.guild.id)+"?limit=999&page=0"
		people = applicable_members.api(applicable_members.people, mee6API, applicable_members.member)
		person = ctx.author.id
		prsn = ctx.author
		role_name = applicable_members.role_name
		peopless =[]

		# role_member = client.role_name.members
		for user in people:
			users = await client.fetch_user(user)
			peopless.append(users)
		
		#Checks if the person if applicable to get the role        
		if str(person) in people:
			role = discord.utils.get(ctx.guild.roles, name=role_name)
			await prsn.add_roles(role)
			print(str(prsn) + " Has Been given Mod Role")
			await ctx.send(ctx.author.mention + " Has been given mod role!")
		elif str(person) != people:
			await ctx.send("Get into the top 3 first motherfucker! " + ctx.author.mention)

		#remove the roles of people who aren't applicable
		for member in list(ctx.guild.members):
			if member in peopless:
				pass
			else:
				role = discord.utils.get(ctx.guild.roles, name=role_name)
				await member.remove_roles(role)
	
	@client.command()
	async def gn(ctx, user: discord.Member = None):
		if user == None:
			await ctx.send("Get Naked!")
		else:
			await ctx.send("Get Naked!" + user.mention)
		
				
		# for cogs in cogss:
		# 	client.load_extension(cogs)

	client.run(token)
	
