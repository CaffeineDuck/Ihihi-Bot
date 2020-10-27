import discord
from discord.ext import commands, tasks
import praw 
from decouple import config
import random
import requests
import aiohttp
import os
from itertools import cycle
import json

try:
	password = os.environ['PASSWORD']
except Exception:
	password = config('PASSWORD')

reddit = praw.Reddit(client_id ='0KxXFz3MNhqqQg',
					 client_secret ='Pz-9kbsz3Uh8PpDGJ6I_51B19Lg',
					 username = 'Samrid_',
					 password = password,
					 user_agent = "python_praw")
				

subreddits = ['memes', 'cursedcomments', 'aww', 'ass', 'boobs', 'cumsluts', 'pussy', 'RealGirls', 'porngifs', 'creampie', 'creampiegifs']
linked = []

"""
Reddit grabber uses saves the links of from various subreddits to a text file
"""
@tasks.loop(seconds = 3600)
async def reddit_grabber():
	data = {}
	for subrd in subreddits:
		subreddit = reddit.subreddit(subrd)
		data[subrd] = [] 
		hot = subreddit.hot(limit=100)
		for submission in hot:
			data[subrd].append({
				'Title': submission.title,
				'Link': submission.url
			})
	with open('.links.txt', 'w+') as outfile:
		json.dump(data, outfile)

reddit_grabber.start()

"""
Reddit sender sends the embed by reading the links in the .txt!
"""
async def reddit_sender(self, subrd, ctx):
	with open('.links.txt') as json_file:
		main = []
		data = json.load(json_file)
		sub = data[subrd]
		for data_list in sub:
			main.append([data_list['Title'], data_list['Link']])

	datas = random.choice(main)
	link = datas[1]	
	embed = discord.Embed(title = datas[0], colour = discord.Colour.blue())
	embed.set_image(url = link)
	embed.set_footer(text=f"Requested by {ctx.author}!")
	if ".jpg" in str(link) or '.png' in str(link) or ".gif" in str(link[-4:-1]):
		await ctx.send(embed=embed)
	elif ".gifv" in str(link):
		await ctx.send(link)
	else:
		await reddit_sender(self, subrd, ctx)
	return


class Random(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(aliases = ['memes'])
	@commands.cooldown(1, 1, commands.BucketType.user)
	async def meme(self, ctx):
		sub = "memes"
		await reddit_sender(self, sub, ctx)
	
	@commands.command(aliases = ['cursedcomment', 'cursedcomments'])
	@commands.cooldown(1, 1, commands.BucketType.user)
	async def cursed(self, ctx):
		sub = "cursedcomments"
		await reddit_sender(self, sub, ctx)

	@commands.command(aliases = ['r'])
	@commands.cooldown(1, 1, commands.BucketType.user)
	async def reddit(self, ctx, sub = "memes"):
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
		await reddit_sender(self, sub, ctx)

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