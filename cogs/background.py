import discord
from discord.ext import commands, tasks
import os
import json
import praw


reddit = praw.Reddit(client_id = os.environ['ID'],
				client_secret = os.environ['SECRET'],
				username = os.environ['REDDIT_USERNAME'],
				password = os.environ['PASSWORD'],
				user_agent = "Ihihihi")
			

subreddits = ['memes', 'cursedcomments', 'aww', 'hentai','ass', 'boobs', 'cumsluts', 'pussy', 'RealGirls', 'porngifs', 'creampie', 'creampiegifs']
linked = []


"""
Reddit grabber uses saves the links of from various subreddits to a json file
"""
@tasks.loop(seconds = 3600)
async def reddit_grabber():
	print("-----------------------------------------------")
	print("Reddit Grabber Started")
	print("-----------------------------------------------")
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
	with open('links.json', 'w') as file:
		json.dump(data, file)
	print("-----------------------------------------------")
	print("Reddit grabber has compeleted its task!")

reddit_grabber.start()

class Background(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	'''
	I don't know OOP(Object oriented programming) :( so had to do this in this way!
	Will improve the code with time :)!
	''' 

def setup(bot):
	bot.add_cog(Background(bot))