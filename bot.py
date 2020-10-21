
from discord.ext import commands
import discord
import os
from PIL import Image
from io import BytesIO
from decouple import config

intents = discord.Intents.default()
intents.members = True

token = config('TOKEN')
client = commands.Bot(command_prefix=".", case_insensitive=True, intents=intents)

@client.command()
async def load(ctx, extension):
	client.load_extension(f'cogs.{extension}')
	await ctx.send(f'The Plugin {extension} has been enabled!')

@client.command()
async def unload(ctx, extension):
	client.unload_extension(f'cogs.{extension}')
	await ctx.send(f'The Plugin {extension} has been disabled!')

"""
Image manipulation isn't working on cogs so these files are here!
"""

@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def wanted(ctx, user: discord.Member = None):
	if user == None:
		user = ctx.author
	
	wanted = Image.open('Images/wanted.jpg')
	asset = user.avatar_url_as(size=128)
	data = BytesIO(await asset.read())
	pfp = Image.open(data)
	pfp = pfp.resize((395, 395))
	wanted.paste(pfp, (269,451))
	wanted.save("wanted.png")
	await ctx.send(file = discord.File("wanted.png"))
	
@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def hitler(ctx, user: discord.Member = None):
	if user == None:
		user = ctx.author
	
	wanted = Image.open('Images/hitler.jpg')
	asset = user.avatar_url_as(size=128)
	data = BytesIO(await asset.read())
	pfp = Image.open(data)
	pfp = pfp.resize((194, 194))
	wanted.paste(pfp, (56,56))
	wanted.save("hitler.png")
	await ctx.send(file = discord.File("hitler.png"))

for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		client.load_extension(f"cogs.{filename[:-3]}")


client.run(token)
	
