from discord.ext import commands, tasks
import discord
import os
from PIL import Image
from io import BytesIO
from decouple import config
from itertools import cycle
import json

status = cycle(['Your THICC Ass', 'Gay Porn', '-_-', 'When you will die!'])



def get_prefix(client,message):

	with open(prefix_file, "r") as f:
		prefixes = json.load(f)

	return prefixes[str(message.guild.id)]

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = get_prefix, case_insensitive=True, intents=intents)
prefix_file = "prefixes.json"

try:
	token = os.environ['TOKEN']
except Exception:
	token = config('TOKEN')
	prefix_file = "prefixes_test.json"


@tasks.loop(seconds = 3600)
async def change_status():
	await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=next(status)))

@client.event
async def on_ready():
	change_status.start()
	print("GOD HAS AWOKEN!")
	with open(prefix_file, "w+") as f:
		prefixes = json.load(f)

	for guild in client.guilds:
		if str(guild.id) in prefixes:
			pass
		else:
			prefixes[str(guild.id)] = "."
			with open(prefix_file, "w") as f:
				json.dump(prefixes,f)


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


@client.event
async def on_guild_join(guild):

	with open(prefix_file, "r") as f:
		prefixes = json.load(f)

	prefixes[str(guild.id)] = "."

	with open(prefix_file, "w") as f:
		json.dump(prefixes,f)




@client.command()
@commands.has_permissions(administrator = True)
async def changeprefix(ctx, prefix):

	with open(prefix_file, "r") as f:
		prefixes = json.load(f)

	prefixes[str(ctx.guild.id)] = prefix

	with open(prefix_file, "w") as f:
		json.dump(prefixes,f)    

	await ctx.send(f"The prefix was changed to {prefix}")

@client.command()
async def prefix(ctx):
	with open(prefix_file, "r") as f:
		prefixes = json.load(f)
	pre = prefixes[str(ctx.guild.id)] 
	await ctx.send(f"My prefix for this server is {pre}")

for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		client.load_extension(f"cogs.{filename[:-3]}")


client.run(token)
	
