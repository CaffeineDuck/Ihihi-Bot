import discord
from discord.ext import commands
import praw 
from decouple import config
import random
import os

try:
	password = os.environ['PASSWORD']
except Exception:
	password = config('PASSWORD')

reddit = praw.Reddit(client_id ='0KxXFz3MNhqqQg',
					 client_secret ='Pz-9kbsz3Uh8PpDGJ6I_51B19Lg',
					 username = 'Samrid_',
					 password = password,
					 user_agent = "python_praw")


"""
Reddit sender sends the embed by reading the links in the .txt!
"""
linked = []

async def reddit_grabber(self, subrd, ctx):
	file = open(f"./links/.{subrd}.txt","r")
	links = file.readlines()
	main_link = random.choice(links)
	embed = discord.Embed(title="Enjoy :)", colour = discord.Colour.green())
	embed.set_image(url=main_link)
	embed.set_footer(text="BOII")
	if ".jpg" in str(main_link) or '.png' in str(main_link) or ".gif" in str(main_link):
		await ctx.send(embed=embed)
	else:
		await ctx.send(main_link)

class NSFWcommands(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	"""
	NSFW COMMANDS
	"""
	
	@commands.command()
	@commands.cooldown(1, 1, commands.BucketType.user)
	@commands.is_nsfw()
	async def ass(self, ctx):
		sub = "ass"
		await reddit_grabber(self, sub, ctx)
	
	@commands.command(aliases=['boobies', 'bobs'])
	@commands.cooldown(1, 1, commands.BucketType.user)
	@commands.is_nsfw()
	async def boobs(self, ctx):
		sub = "boobs"
		await reddit_grabber(self, sub, ctx)
	
	@commands.command(aliases = ['vagena'])
	@commands.cooldown(1, 1, commands.BucketType.user)
	@commands.is_nsfw()
	async def pussy(self, ctx):
		sub = "pussy"
		await reddit_grabber(self, sub, ctx)
	
	@commands.command(aliases = ['real_girls', 'nudes'])
	@commands.cooldown(1, 1, commands.BucketType.user)
	@commands.is_nsfw()
	async def real(self, ctx):
		sub = "RealGirls"
		await reddit_grabber(self, sub, ctx)
	
	@commands.command(aliases = ['cum', 'cumsluts'])
	@commands.cooldown(1, 1, commands.BucketType.user)
	@commands.is_nsfw()
	async def cumshot(self, ctx):
		sub = "cumsluts"
		await reddit_grabber(self, sub, ctx)

def setup(bot):
	bot.add_cog(NSFWcommands(bot))
