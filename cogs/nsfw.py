import discord
from discord.ext import commands
import random
import json

"""
Reddit sender sends the embed by reading the links in the .txt!
"""
linked = []

async def reddit_grabber(self, subrd, ctx):
	with open('./Other/json/links.json') as json_file:
		main = []
		data = json.load(json_file)
		sub = data[subrd]
		for data_list in sub:
			main.append([data_list['Title'], data_list['Link']])

	datas = random.choice(main)
	link = datas[1]	
	embed = discord.Embed(title = datas[0], timestamp = ctx.message.created_at, colour = discord.Colour.green())
	embed.set_image(url = link)
	embed.set_footer(text=f"Requested by {ctx.author}!")
	if ".jpg" in str(link) or '.png' in str(link) or ".gif" in str(link[-4:-1]):
		await ctx.send(embed=embed)
	elif ".gifv" in str(link):
		await ctx.send(link)
	else:
		await reddit_grabber(self, subrd, ctx)
	return
		

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
	
	@commands.command(aliases=['cream', 'pie'])
	@commands.is_nsfw()
	async def creampie(self, ctx):
		sub = "creampie"
		await reddit_grabber(self, sub, ctx)
	
	@commands.command(aliases=['pgif', 'porn'])
	@commands.is_nsfw()
	async def porngifs(self, ctx):
		sub = "porngifs"
		await reddit_grabber(self, sub, ctx)
	
	
	@commands.command(aliases=['creamg', 'pieg'])
	@commands.is_nsfw()
	async def creampiegif(self, ctx):
		sub = "creampiegifs"
		await reddit_grabber(self, sub, ctx)

	@commands.command(aliases=['onechan', 'onnichan'])
	@commands.is_nsfw()
	async def hentai(self, ctx):
		sub = "hentai"
		await reddit_grabber(self, sub, ctx)
	
def setup(bot):
	bot.add_cog(NSFWcommands(bot))
