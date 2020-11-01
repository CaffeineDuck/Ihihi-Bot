from discord.ext import commands
import discord
from utils.Personal import fun, jokes, facts
import random
import requests

class funcommands(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.hugs =  fun.hugs
		self.pats = fun.pats
		self.kills = fun.kills
		self.slaps = fun.slaps
		self.licks = fun.licks
		self.jokes = jokes.jokes_list
		self.facts = facts.facts_list
	
	
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
	
	@commands.command()
	async def kill(self, ctx, member : discord.Member = None):
		if not member:
			embed = discord.Embed(description = f'{ctx.author.mention} is a murdurer!', color = discord.Color.red())
		else:
			embed = discord.Embed(description = f'{ctx.author.mention} KILLED {member.mention}', color = discord.Color.red())
		random_link = random.choice(self.kills)   
		embed.set_image(url = random_link)
		await ctx.send(embed = embed)
	
	@commands.command()
	async def slap(self, ctx, member : discord.Member = None):
		if not member:
			embed = discord.Embed(description = f'{ctx.author.mention} slapped!', color = discord.Color.red())
		else:
			embed = discord.Embed(description = f'{ctx.author.mention} slapped {member.mention}', color = discord.Color.red())
		random_link = random.choice(self.slaps)   
		embed.set_image(url = random_link)
		await ctx.send(embed = embed)

	@commands.command()
	async def lick(self, ctx, member : discord.Member = None):
		if not member:
			embed = discord.Embed(description = f'{ctx.author.mention} got licked.', color = discord.Color.red())
		else:
			embed = discord.Embed(description = f'{ctx.author.mention} licked {member.mention}', color = discord.Color.red())
		random_link = random.choice(self.licks)   
		embed.set_image(url = random_link)
		await ctx.send(embed = embed)
	
	@commands.command()
	async def insult(self, ctx, member: discord.Member = None):
		if not member:
			member = ctx.message.author
		joke = requests.get("https://evilinsult.com/generate_insult.php?lang=en&type=txt")
		await ctx.send(f'{member.mention} {joke.text}')
	
	@commands.command()
	async def joke(self, ctx):
		_joke = random.choice(self.jokes)
		await ctx.send(_joke)
	
	@commands.command()
	async def fact(self, ctx):
		_fact = random.choice(self.facts)
		await ctx.send(_fact)

def setup(bot):
	bot.add_cog(funcommands(bot))