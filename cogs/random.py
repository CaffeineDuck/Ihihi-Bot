import discord
from discord.ext import commands
import praw 
from decouple import config
import random
import requests
import aiohttp

reddit = praw.Reddit(client_id ='0KxXFz3MNhqqQg',
					 client_secret ='Pz-9kbsz3Uh8PpDGJ6I_51B19Lg',
					 username = 'Samrid_',
					 password = config('PASSWORD'),
					 user_agent = "python_praw")
				
"""
Reddit grabber uses praw to grab the image from a specified subreddit
"""
async def reddit_grabber(self, subrd, ctx):
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

class Random(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(aliases = ['memes'])
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def meme(self, ctx):
		sub = "memes"
		await reddit_grabber(self, sub, ctx)
	
	@commands.command(aliases = ['cursedcomment', 'cursedcomments'])
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def cursed(self, ctx):
		sub = "cursedcomments"
		await reddit_grabber(self, sub, ctx)
	
	@commands.command(aliases = ['r'])
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def reddit(self, ctx, sub = "memes"):
		await reddit_grabber(self, sub, ctx)

	@commands.command(aliases = ['cute'])
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def aww(self, ctx):
		sub = "aww"
		await reddit_grabber(self, sub, ctx)

	@commands.command(aliases = ['puppy', 'pup'])
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def dog(self, ctx):
		async with aiohttp.ClientSession() as cs:
			async with cs.get ("https://dog.ceo/api/breeds/image/random") as r: 
				data = await r.json()
				image = data.get("message")
		embed = discord.Embed(title="Henlo")
		embed.set_image(url=image)
		embed.set_footer(text="https://dog.ceo/")
		await ctx.send(embed=embed)
	
	@commands.command(aliases = ['foxy'])
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def fox(self, ctx):
		async with aiohttp.ClientSession() as cs:
			async with cs.get ("https://randomfox.ca/floof/") as r:
				data = await r.json()
				image = data.get("image")
		embed = discord.Embed(title="What does the fox say?")
		embed.set_image(url=image)
		embed.set_footer(text="https://randomfox.ca")
		await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(Random(bot))