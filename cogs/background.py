import discord
from discord.ext import commands, tasks
import os
import json
from asyncpraw import Reddit
from itertools import cycle
from thispersondoesnotexist import get_online_person, save_picture
"""
Prints "-------------------------"
"""
def star():
	print("-----------------------------------------------")


class Background(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		
	"""
	Random Person's Image fetcher
	"""
	@staticmethod
	@tasks.loop(hours=24)
	async def image_grabber():
		star()
		print("Image Grabber has started!")
		star()
		for x in range(1,100):
			picture = await get_online_person()
			await save_picture(picture, f"./Other/Images/Random-Person/{x}.jpeg")
		star()
		print("Image Grabber has completed!")
		star()


"""
Starts the loop of fetching the data from reddit
"""
Background.image_grabber.start()

def setup(bot):
	bot.add_cog(Background(bot))