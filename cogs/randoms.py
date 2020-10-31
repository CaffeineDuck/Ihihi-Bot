import discord
from discord.ext import commands, tasks
import random
import requests
import aiohttp
import os
import json
import praw

'''
Credentials for reddit praw authentication!
'''
reddit = praw.Reddit(client_id = os.environ['ID'],
				client_secret = os.environ['SECRET'],
				username = os.environ['REDDIT_USERNAME'],
				password = os.environ['PASSWORD'],
				user_agent = "Ihihihi")

"""
Reddit sender sends the embed by reading the links in the json!
"""
async def reddit_sender(self, subrd, ctx):
	with open('links.json') as json_file:
		main = []
		data = json.load(json_file)
		sub = data[subrd]
		for data_list in sub:
			main.append([data_list['Title'], data_list['Link']])

	datas = random.choice(main)
	link = datas[1]	
	embed = discord.Embed(title = datas[0],timestamp = ctx.message.created_at, colour = discord.Colour.blue())
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