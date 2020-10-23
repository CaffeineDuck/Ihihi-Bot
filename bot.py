from discord.ext import commands, tasks
import discord
import os
from PIL import Image
from io import BytesIO
from decouple import config
from itertools import cycle

status = cycle(['Your THICC Ass', 'Gay Pron', '-_-', 'When you will die!'])


intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix=".", case_insensitive=True, intents=intents)
try:
	token = os.environ['TOKEN']
except Exception:
	token = config('TOKEN')
	client = commands.Bot(command_prefix="-", case_insensitive=True, intents=intents)


@tasks.loop(seconds = 3600)
async def change_status():
	await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=next(status)))

@client.event
async def on_ready():
	change_status.start()
	print("GOD HAS AWOKEN!")


@client.command()
async def load(ctx, extension):
	client.load_extension(f'cogs.{extension}')
	await ctx.send(f'The Plugin {extension} has been enabled!')

@client.command()
async def unload(ctx, extension):
	client.unload_extension(f'cogs.{extension}')
	await ctx.send(f'The Plugin {extension} has been disabled!')

@client.command()
async def reload(ctx, extension):
	client.unload_extension(f'cogs.{extension}')
	client.load_extension(f'cogs.{extension}')
	await ctx.send(f"The Plugin {extension} has been reloaded!")


for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		client.load_extension(f"cogs.{filename[:-3]}")


client.run(token)
	
