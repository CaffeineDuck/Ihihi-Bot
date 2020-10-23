import discord
from discord.ext import commands
import praw 
from decouple import config
import random
import os

reddit = praw.Reddit(client_id ='0KxXFz3MNhqqQg',
					 client_secret ='Pz-9kbsz3Uh8PpDGJ6I_51B19Lg',
					 username = 'Samrid_',
					 password = os.environ['PASSWORD'],
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

class NSFWcommands(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	"""
	NSFW COMMANDS
	"""
	
	@commands.command()
	@commands.cooldown(1, 5, commands.BucketType.user)
	@commands.is_nsfw()
	async def ass(self, ctx):
		sub = "ass"
		await reddit_grabber(self, sub, ctx)
	
	@commands.command(aliases=['boobies', 'bobs'])
	@commands.cooldown(1, 5, commands.BucketType.user)
	@commands.is_nsfw()
	async def boobs(self, ctx):
		sub = "boobs"
		await reddit_grabber(self, sub, ctx)
	
	@commands.command(aliases = ['vagena'])
	@commands.cooldown(1, 5, commands.BucketType.user)
	@commands.is_nsfw()
	async def pussy(self, ctx):
		sub = "pussy"
		await reddit_grabber(self, sub, ctx)
	
	@commands.command(aliases = ['real_girls', 'nudes'])
	@commands.cooldown(1, 5, commands.BucketType.user)
	@commands.is_nsfw()
	async def real(self, ctx):
		sub = "RealGirls"
		await reddit_grabber(self, sub, ctx)
	
	@commands.command(aliases = ['cum', 'cumsluts'])
	@commands.cooldown(1, 5, commands.BucketType.user)
	@commands.is_nsfw()
	async def cumshot(self, ctx):
		sub = "cumsluts"
		await reddit_grabber(self, sub, ctx)

def setup(bot):
	bot.add_cog(NSFWcommands(bot))
