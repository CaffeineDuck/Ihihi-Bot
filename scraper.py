import discord
from discord.ext import commands, tasks

token = "NzY3Mjc5MjAzMjY3Mzc5Mjgw.X4vmcQ.HWfMnd0Yv-qxAw8QMV_7U115exI"
client = commands.Bot(command_prefix=".", case_insensitive=True)

@client.event
async def on_ready():
    print("Bot is ready")
    
@client.command()
async def waifu(ctx):
    await ctx.send("lol")
    print("lol")

client.run(token)

