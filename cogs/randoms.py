import discord
from discord.ext import commands, tasks

import requests
import aiohttp
import random
import os
import time
import asyncpraw

from utils.Personal.cached_reddit import RedditPostCacher
 
reddit = asyncpraw.Reddit(client_id = os.environ['ID'],
                    client_secret = os.environ['SECRET'],
                    user_agent = 'Ihihi Bot')

class Random(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		
		self.subreddits = ('meme', 'aww', 'cursedcomments')
		self.cache = RedditPostCacher(self.subreddits, './Other/cache/Randoms.pickle')
		self.cache.cache_posts.start()
	
	async def _reddit_sender(self, ctx, subrd: str, title: str):
		"""Fetches from reddit and sends results

			Parameters
			----------
			ctx : discord.ext.commands.Context
					The invocation context
			subrd : str
					The subreddit to fetch from
			title : str
					The title to use in the embed
		"""
		# Gets the data from reddit!
		submission = await self.cache.get_random_post(subrd)

		# Sends the embed!
		embed = discord.Embed(title=title, timestamp=ctx.message.created_at, color = discord.Colour.gold())
		embed.set_image(url=submission)
		embed.set_footer(text=f'Requested by {ctx.author}')
		await ctx.send(embed=embed)

	@commands.command(aliases = ['memes'])
	@commands.cooldown(1, 1, commands.BucketType.user)
	async def meme(self, ctx):
		await self._reddit_sender(ctx, "meme", "Memes for you <3")
	
	@commands.command(aliases = ['cursedcomment', 'cursedcomments'])
	@commands.cooldown(1, 1, commands.BucketType.user)
	async def cursed(self, ctx):
		await self._reddit_sender(ctx, "cursedcomments", "This isn't cursed its you!")

	@commands.command(aliases = ['cute'])
	@commands.cooldown(1, 1, commands.BucketType.user)
	async def aww(self, ctx):
		await self._reddit_sender(ctx, "aww", "This is cute but YOU AREN'T!")

	@commands.command(aliases = ['reddit','subreddit'])
	async def r(self, ctx, subred = 'memes'):
		try:#checks for subreddit
			subreddit = await reddit.subreddit(subred)
			all_subs = []
	
			async for submissions in subreddit.top(limit=50):
				all_subs.append(submissions)
		
			random_subs = random.choice(all_subs)
			name = random_subs.title
			url = random_subs.url
	
			embed = discord.Embed(title = name)
			embed.set_image(url = url)
			embed.set_footer(text = f'Requested by: {ctx.author}')
			await ctx.send(embed = embed)
		except:#if not sends this
			await ctx.send("Subreddit not found. Try again")

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
	
	@commands.command()
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

	
	@commands.command(aliases=['doesnotexist', 'fakeperson'])
	async def thispersondoesnotexist(self, ctx):
		_image = f'{random.randrange(0,100)}.jpeg'
		file = discord.File(f"./Other/Images/Random-Person/{_image}", filename=_image)
		embed = discord.Embed(title="Real Person?", description = "This person doesn't exist!", color=0xFFFFF0)
		embed.set_image(url=f"attachment://{_image}")
		embed.set_footer(text=f'Requested by {ctx.author}')
		await ctx.send(file=file, embed=embed)
	
def setup(bot):
	bot.add_cog(Random(bot))