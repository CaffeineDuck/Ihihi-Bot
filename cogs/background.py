import discord
from discord.ext import commands, tasks
import os
import json
import praw
from itertools import cycle

"""
Prints "-------------------------"
"""
def star():
	print("-----------------------------------------------")

'''
Credentials for reddit praw authentication!
'''
reddit = praw.Reddit(client_id = os.environ['ID'],
				client_secret = os.environ['SECRET'],
				username = os.environ['REDDIT_USERNAME'],
				password = os.environ['PASSWORD'],
				user_agent = "Ihihihi")
			

subreddits = ['memes', 'cursedcomments', 'aww', 'hentai','ass', 'boobs', 'cumsluts', 'pussy', 'RealGirls', 'porngifs', 'creampie', 'creampiegifs']
linked = []
status = cycle(['Your THICC Ass', 'Gay Porn', '-_-', 'When you will die!'])


class Background(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	"""
	Reddit grabber uses saves the links of from various subreddits to a json file
	"""
	@staticmethod
	@tasks.loop(hours = 1)
	async def reddit_grabber():
		star()
		print("Reddit Grabber Started")
		star()
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
		star()
		print("Reddit grabber has compeleted its task!")
		star()

"""
Starts the loop of fetching the data from reddit
"""
Background.reddit_grabber.start()

def setup(bot):
	bot.add_cog(Background(bot))