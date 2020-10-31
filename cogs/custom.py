import discord
from discord.ext import commands
import random

member = []

class custom(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.hugs = [
		'https://i.pinimg.com/originals/f2/80/5f/f2805f274471676c96aff2bc9fbedd70.gif',
		'https://media1.giphy.com/media/l2QDM9Jnim1YVILXa/source.gif',
		'https://i.pinimg.com/originals/a1/64/6c/a1646c77119633b484ba98fc90613f15.gif',
		'https://media1.tenor.com/images/977c0043ee29cdae790dc47507fcb91d/tenor.gif?itemid=12668474',
		'https://acegif.com/wp-content/uploads/anime-hug.gif'
		]
 
		self.pats = [
			'https://media1.tenor.com/images/d7c326bd43776f1e0df6f63956230eb4/tenor.gif?itemid=17187002',
			'https://media1.tenor.com/images/fb3e0b0f18188450bfded4a585de2b90/tenor.gif?itemid=8208759',
			'https://i.pinimg.com/originals/e3/e2/58/e3e2588fbae9422f2bd4813c324b1298.gif',
			'https://i.gifer.com/KJ42.gif',
			'https://thumbs.gfycat.com/BlushingDeepBlacknorwegianelkhound-small.gif'
		]
	
	@commands.command()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def gn(self, ctx, user: discord.Member = None):
		if not user:
			await ctx.send("Get Naked!")
		else:
			await ctx.send("Get Naked!" + user.mention)
	
	@commands.command()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def henlo(self, ctx, input=None):
		if not input:
			await ctx.send(f"Fuck you! {ctx.author.mention}")
		else:
			await ctx.send(f"Fuck you {input}!")
	
	@commands.command(aliases = ['bye'])
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def byy(self, ctx, *, input=None):
		if not input:
			await ctx.send("Lonenly ass, you are so lonely that you need a bot to say you goodbye! :nauseated_face: " + ctx.author.mention)
		else:
			await ctx.send(f"Goodbye Old Friend {input}")

	@commands.command()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def suk(self, ctx,user: discord.Member = None):
		if not user:
			await ctx.send(f"{ctx.author.mention} How alone can you be to not even find a person in discord for making him/her suck your dick virtually?")
		else:
			await ctx.send(f"{user.mention} Suck {ctx.author.mention}'s DICK!")
	
	@commands.command()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def gg(self, ctx, user: discord.Member = None):
		if not user:
			await ctx.send("Good Game Well Played")
		else:
			await ctx.send(f"Good Game Well Played {user.mention}")
	
	@commands.command()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def waifu(self, ctx, user: discord.Member = None):
		if not user:
			user = ctx.author

		waifu = random.randrange(1,10)

		if waifu == 1 or waifu == 2:
			emoji = ":face_vomiting:"
		elif waifu == 3 or waifu == 4:
			emoji = ":nauseated_face:"
		elif waifu == 5 or waifu == 6:
			emoji = ":cold_sweat:"
		elif waifu == 7:
			emoji = ":kissing:"
		elif waifu == 8:
			emoji = ":smirk:"
		elif waifu == 9:
			emoji = ":relaxed:"
		elif waifu == 10:
			emoji = ":heart_eyes:"

		rate = f"{user.mention}, You are {str(waifu)}/10 waifu! {emoji}"

		embed = discord.Embed(title = "Waifu Rate", description = rate, colour = discord.Colour.red())
		await ctx.send(embed=embed)
	
	@commands.command()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def muji(self, ctx, user: discord.Member = None):
		if not user:
			await ctx.send("Dherai bigris jatha muji!")
		else:
			await ctx.send(f"Dherai bigris jatha muji! {user.mention}")
	
	@commands.command()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def routine(self, ctx):
		image = "https://cdn.discordapp.com/attachments/766213304846647309/768311655306100766/routine.png"
		embed = discord.Embed(title="Routine")
		embed.set_image(url=image)
		embed.set_footer(text="I want to DIE!" )
		await ctx.send(embed=embed)

	@commands.command(aliases = ['gay','gayr8', 'gae'])
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def gayrate(self, ctx, user: discord.Member = None):
		if user == None:
			user = ctx.author
		gayr8 = random.randrange(1,100)
		rate = f"{user.mention}, You are {str(gayr8)}% Gay!"
		embed = discord.Embed(title = "Gay Rate", description = rate, colour = discord.Colour.green())
		await ctx.send(embed=embed)

	@commands.command()
	async def anyone(self, ctx,*, input = None):
		guild_members = ctx.guild.members
		members = [member for member in guild_members if not member.bot]
		member = random.choice(members)
		if input == None:
			await ctx.send(f"{member.mention} is the chosen one!")
		else:
			await ctx.send(f"{member.mention} is chosen to {input}")
		
	@commands.command()
	async def hug(self, ctx, member : discord.Member = None):
		if not member:
			embed = discord.Embed(description = f'{ctx.author.mention} got hugged!', color = discord.Color.green())
		else:
			embed = discord.Embed(description = f'{ctx.author.mention} hugged {member.mention}', color = discord.Color.green())
		random_link = random.choice(self.hugs)   
		embed.set_image(url = random_link)
		await ctx.send(embed = embed)
	
	@commands.command()
	async def pat(self, ctx, member : discord.Member = None):
		if not member:
			embed = discord.Embed(description = f'{ctx.author.mention} got patted!', color = discord.Color.green())
		else:
			embed = discord.Embed(description = f'{ctx.author.mention} pats {member.mention}', color = discord.Color.green())
		random_link = random.choice(self.pats)   
		embed.set_image(url = random_link)
		await ctx.send(embed = embed)

	@commands.command(aliases=['s'])
	@commands.has_permissions(kick_members = True)
	async def send(self, ctx, member : discord.Member, *, message = "No reason provided"):
		await member.send(message)
	
	
def setup(bot):
	bot.add_cog(custom(bot))