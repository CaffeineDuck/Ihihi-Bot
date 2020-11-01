import discord
from discord.ext import commands
from PIL import Image
from io import BytesIO
import os

class image_manipulation(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
	
	@commands.command()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def wanted(self, ctx, user: discord.Member = None):
		if not user:
			user = ctx.author
	
		wanted = Image.open('./Other/Images/Manipulation/wanted.jpg')
		asset = user.avatar_url_as(size=128)
		data = BytesIO(await asset.read())
		pfp = Image.open(data)
		pfp = pfp.resize((395, 395))
		wanted.paste(pfp, (269,451))
		wanted.save("./Other/Images/Manipulation/wanted.png")
		await ctx.send(file = discord.File("./Other/Images/Manipulation/wanted.png"))
	
	@commands.command()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def hitler(self, ctx, user: discord.Member = None):
		if not user:
			user = ctx.author
	
		wanted = Image.open('./Other/Images/Manipulation/hitler.jpg')
		asset = user.avatar_url_as(size=128)
		data = BytesIO(await asset.read())
		pfp = Image.open(data)
		pfp = pfp.resize((194, 194))
		wanted.paste(pfp, (56,56))
		wanted.save("./Other/Images/Manipulation/hitler.png")
		await ctx.send(file = discord.File("./Other/Images/Manipulation/hitler.png"))

def setup(bot):
	bot.add_cog(image_manipulation(bot))