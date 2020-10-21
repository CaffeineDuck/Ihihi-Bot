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
			await ctx.send("Lonenly ass, you are lonely that you need goodnight from a bot! " + ctx.author.mention)
		else:
			await ctx.send("Goodbye Old Friend " + input)
	
	@commands.command()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def waifu(self, ctx,user: discord.Member = None):
		waifu = str(random.randrange(1,10))
		if user == None:
			await ctx.send(ctx.author.mention + " You are " + waifu + "/10 waifu!")
		else:
			await ctx.send(user + " is " + waifu + "/10 waifu!")
	
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
		waifu = str(random.randrange(1,10))
		if user == None:
			await ctx.send(ctx.author.mention + " You are " + waifu + "/10 waifu!")
		else:
			await ctx.send(input + " is " + waifu + "/10 waifu!")


def setup(bot):
	bot.add_cog(custom(bot))