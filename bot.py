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

@client.command()
async def lol(ctx):
	await ctx.send("LMAO")


for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		client.load_extension(f"cogs.{filename[:-3]}")


client.run(token)
	
