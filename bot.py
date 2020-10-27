from discord.ext import commands, tasks
import discord
import os
from PIL import Image
from io import BytesIO
from decouple import config
from itertools import cycle
import json	
import pymongo
import motor

"""
Statuses
"""
status = cycle(['Your THICC Ass', 'Gay Porn', '-_-', 'When you will die!'])


"""
As bot is hosted in heroku I have made one testing bot so it 
chooses the collection based on where it is hosted!
"""
try:
	mongoclient = os.environ['MONGOCLIENT']
except Exception:
	mongoclient = config('MONGOCLIENT')


"""
Mongo Db
"""
bot = pymongo.MongoClient(mongoclient)
db = bot.ihihihibot_db
prefixes = db.server_prefixes


"""
As bot is hosted in heroku I have made one testing bot so it 
chooses the token based on where it is hosted!
"""
try:
	token = os.environ['TOKEN']
except Exception:
	token = config('TOKEN')
	prefixes = db.server_test_prefixes


"""
Function to get prefix for each server
"""
def get_prefix(client,message):
	cur = prefixes.find_one({'server_id':message.guild.id})
	return(cur.get('prefix'))


"""
Discord.py Variables
"""
defualt_prefix = "."
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = get_prefix, case_insensitive=True, intents=intents)


"""
This Background task loops every 1 hour and changes the status!
"""
@tasks.loop(seconds = 3600)
async def change_status():
	await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=next(status)))


"""
It initializes all the background tasks as soon as it is ready!
"""
@client.event
async def on_ready():
	change_status.start()
	print("GOD HAS AWOKEN!")
	
	for guild in client.guilds:
		
		if prefixes.count_documents({'server_id' : guild.id}) == 0:
			perfix_data = {
				'server_id' : guild.id,
				'prefix' : defualt_prefix,
				'server_name' : guild.name
			}
			prefixes.insert_one(perfix_data)
			print(f"Prefix for server id {guild.id} has been created!")
			

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
	if prefixes.count_documents({'server_id' : guild.id}) == 0:
			perfix_data = {
				'server_id' : guild.id,
				'prefix' : defualt_prefix,
				'server_name' : guild.name
			}
			prefixes.insert_one(perfix_data)
			print(f"Prefix for server id {guild.id} has been created!")

@client.event
async def on_message(msg):
	try:
		if msg.mentions[0] == client.user:
			cur = prefixes.find_one({'server_id':msg.guild.id})
			pre = cur.get('prefix')
			await msg.channel.send(f"My prefix for this server is `{pre}`")
	except:
		pass
	await client.process_commands(msg)


@client.command()
@commands.has_permissions(administrator = True)
async def changeprefix(ctx,*, prefix):

	cur = prefixes.find_one({'server_id':ctx.guild.id})
	old_prefix = cur.get('prefix')

	old_data = {
				'server_id':ctx.guild.id, 
				'prefix':old_prefix
	}
	new_data = {"$set": {
						'server_id':ctx.guild.id, 
						'prefix': prefix
				}
	}

	prefixes.update_one(old_data, new_data)
	print(f"Prefix for the server {ctx.guild.id} has been updated to '{prefix}' !")
	await ctx.send(f"The prefix was changed to {prefix}")

@client.command()
async def prefix(ctx):
	cur = prefixes.find_one({'server_id':ctx.guild.id})
	prefix = cur.get('prefix')
	await ctx.send(f"The prefix is {prefix}")

for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		client.load_extension(f"cogs.{filename[:-3]}")


client.run(token)
	
