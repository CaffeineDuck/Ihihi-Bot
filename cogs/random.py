import discord
from discord.ext import commands, tasks
import praw 
from decouple import config
import random
import requests
import aiohttp
import os
from itertools import cycle

try:
	password = os.environ['PASSWORD']
except Exception:
	password = config('PASSWORD')

reddit = praw.Reddit(client_id ='0KxXFz3MNhqqQg',
					 client_secret ='Pz-9kbsz3Uh8PpDGJ6I_51B19Lg',
					 username = 'Samrid_',
					 password = password,
					 user_agent = "python_praw")
				

subreddits = ['memes', 'cursedcomments', 'aww', 'ass', 'boobs', 'cumsluts', 'pussy', 'RealGirls']
linked = []

"""
Reddit grabber uses saves the links of from various subreddits to a text file
"""
@tasks.loop(seconds = 3600)
async def reddit_grabber():
	for subrd in subreddits:
		subreddit = reddit.subreddit(subrd)
		all_subs = [] 
		hot = subreddit.top(limit=50)
		for submission in hot:
			all_subs.append(submission)
		
		file = open(f"./links/{subrd}.txt","w+")
		for subs in all_subs:
			file.write(f"{str(subs.url)}\n")
		file.close()

reddit_grabber.start()

"""
Reddit sender sends the embed by reading the links in the .txt!
"""

async def reddit_sender(self, subrd, ctx, title):
	file = open(f"./links/{subrd}.txt","r")
	links = file.readlines()
	main_link = random.choice(links)
	embed = discord.Embed(title=str(title))
	embed.set_image(url=main_link)
	embed.set_footer(text=":) Reddit: Samrid_")
	await ctx.send(embed=embed)

class Random(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(aliases = ['memes'])
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def meme(self, ctx):
		sub = "memes"
		topic = "Meme For You! <3"

		await reddit_sender(self, sub, ctx, topic)
	
	@commands.command(aliases = ['cursedcomment', 'cursedcomments'])
	@commands.cooldown(1, 1, commands.BucketType.user)
	async def cursed(self, ctx):
		sub = "cursedcomments"
		topic = "Its Not Cursed, Its just you seeing it!"

		await reddit_sender(self, sub, ctx, topic)
	
	@commands.command(aliases = ['r'])
	@commands.cooldown(1, 1, commands.BucketType.user)
	async def reddit(self, ctx, sub = "memes"):
		topic = "Fuck You"
		subreddit = reddit.subreddit(sub)
		all_subs = [] 
		hot = subreddit.top(limit=50)
		for submission in hot:
			all_subs.append(submission)
		link = random.choice(all_subs)
		embed = discord.Embed(title = link.title)
		embed.set_image(url = link.url)
		await ctx.send(embed=embed)

	@commands.command(aliases = ['cute'])
	@commands.cooldown(1, 1, commands.BucketType.user)
	async def aww(self, ctx):
		sub = "aww"
		topic = "This may look nice but your face is ugly!"
		await reddit_sender(self, sub, ctx, topic)

	@commands.command(aliases = ['puppy', 'pup'])
	@commands.cooldown(1, 1, commands.BucketType.user)
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
	@commands.cooldown(1, 1, commands.BucketType.user)
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