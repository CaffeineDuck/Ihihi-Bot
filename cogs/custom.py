import discord
from discord.ext import commands
import random

class custom(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def gn(self, ctx, user: discord.Member = None):
		if user == None:
			await ctx.send("Get Naked!")
		else:
			await ctx.send("Get Naked!" + user.mention)
	
	@commands.command()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def henlo(self, ctx, input=None):
		if input == None:
			await ctx.send("Fuck you! " + ctx.author.mention)
		else:
			await ctx.send("Fuck you! " + input )
	
	@commands.command(aliases = ['bye'])
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def byy(self, ctx, input=None):
		if input == None:
			await ctx.send("Lonenly ass, you are so lonely that you need a bot to say you goodbye! :nauseated_face: " + ctx.author.mention)
		else:
			await ctx.send("Goodbye Old Friend " + input)

	@commands.command()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def suk(self, ctx,user: discord.Member = None):
		if user == None:
			await ctx.send(ctx.author.mention + " How alone can you be to not even find a person in discord for making him/her suck your dick virtually?")
		else:
			await ctx.send(user.mention + " Suck " + ctx.author.mention + "'s Dick!")
	
	@commands.command()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def gg(self, ctx, user: discord.Member = None):
		if user == None:
			await ctx.send("Good Game Well Played")
		else:
			await ctx.send("Good Game Well Played "+user.mention)
	
	@commands.command()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def waifu(self, ctx, user: discord.Member = None):
		if user == None:
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
		if user == None:
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
	
	@commands.command()
	async def bobotest(self, ctx):
		await ctx.send(".help")

	@commands.command(aliases = ['gay','gayr8', 'gae'])
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def gayrate(self, ctx, user: discord.Member = None):
		if user == None:
			user = ctx.author
		gayr8 = random.randrange(1,100)
		rate = f"{user.mention}, You are {str(gayr8)}% Gay!"
		embed = discord.Embed(title = "Gay Rate", description = rate, colour = discord.Colour.green())
		await ctx.send(embed=embed)


def setup(bot):
	bot.add_cog(custom(bot))