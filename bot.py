import requests
import json
import discord
from discord.ext import commands, tasks
from discord.utils import get
import datetime
import random

intents = discord.Intents.default()
intents.members = True

#Class For actual Bot management
#Variables
token = "NzY3Mjc5MjAzMjY3Mzc5Mjgw.X4vmcQ.uobt0bqwcyVkBvNWw1753qfV6WE"

#Declaring Prefix
client = commands.Bot(command_prefix=".", case_insensitive=True, intents=intents)


#Class to get the list of applicable members
class applicable_members:

    #Variables
    people = []
    role_name = "Mods"
    bots=[767279203267379280 ,270904126974590976, 751026843687321660]
    member={}

    def api(people, mee6API, member):

        #Gets the data from api
        result = requests.get(mee6API).json()

        #Gets specific data related to members
        players = result.get("players")

        #Loop to form dict of player and their xp
        for player in players:
            member[player.get("xp")] = player.get("id")

        #List of user-id of people illegible to get Mod role
        people = list(member.values())[:2]

        #Returns
        return(people)



class samrid_bot:

	@client.event
	async def on_ready():
		print("Bot is ready")
				
	@client.event
	async def on_message(message):

		#mee6API
		mee6API = "https://mee6.xyz/api/plugins/levels/leaderboard/"+str(message.guild.id)+"?limit=999&page=0"

		#Checks If the messager isn't bot
		if message.author.id in applicable_members.bots:
			pass
		else:
			
				#Checks if the message is for making admin changes
				if "give me mod" == message.content :

					#Variables
					people = applicable_members.api(applicable_members.people, mee6API, applicable_members.member)
					print(people)
					person = message.author.id
					prsn = message.author
					role_name = applicable_members.role_name
					peoples =[]

					# role_member = client.role_name.members
					for user in people:
						users = await client.fetch_user(user)
						peoples.append(users)
					
					#Checks if the person if applicable to get the role        
					if str(person) in people:
						role = discord.utils.get(message.guild.roles, name=role_name)
						await prsn.add_roles(role)
						print(str(prsn) + " Has Been given Mod Role")
						await message.channel.send(message.author.mention + " Has been given mod role!")
					else:
						await message.channel.send("Get into the top 3 first motherfucker! "+message.author.mention)

					#remove the roles of people who aren't applicable
					for member in list(client.get_all_members()):
						if member in peoples:
							pass
						else:
							role = discord.utils.get(message.guild.roles, name=role_name)
							await member.remove_roles(role)

				#RESPONSES TO SHITTY THINGS
				else:
					#Response to imagine
					try:
						if "imagine" == message.content.split()[0]:
							await message.channel.send("I can't even " + message.content +", bro!")

						#Response to f
						elif "f" == message.content.lower():
							await message.channel.send("f")
						
						#Response to no u
						elif "no u" == message.content.lower():
							await message.channel.send("no u")
						
						#Response to .hello there
						elif ".hello there" == message.content.lower() or "hello there" == message.content.lower():
							await message.channel.send("General Kenobi")
						
						#Response to shh
						elif "shh" == message.content.lower().split()[0] or ".shh" == message.content.lower().split()[0]:
							await message.channel.send(":shushing_face:")
						
					except Exception:
						pass
			
		#Send the message to command processor 
		await client.process_commands(message)
			

	
	@client.command()
	async def waifu(ctx,input=None):
		waifu = str(random.randrange(1,10))
		if input == None:
			await ctx.send(ctx.author.mention + " You are " + waifu + "/10 waifu!")
		else:
			await ctx.send(input + " is " + waifu + "/10 waifu!")
	
	@client.command()
	async def tata(ctx,input=None):
		if input == None:
			await ctx.send(ctx.author.mention + " How alone can you be to not even find a person in discord for making him/her suck your dick virtually?")
		else:
			await ctx.send(input + " Suck " + ctx.author.mention + "'s Dick!")
	
	@client.command()
	async def gg(ctx, input=None):
		if input == None:
			await ctx.send("Good Game Well Played")
		else:
			await ctx.send("Good Game Well Played "+input)

	@client.command()
	async def henlo(ctx, input=None):
		if input == None:
			await ctx.send("Fuck you! " + ctx.author.mention)
		else:
			await ctx.send("Fuck you! " + input )
	
	@client.command()
	async def byy(ctx, input=None):
		if input == None:
			await ctx.send("Lonenly ass, you are lonely that you need goodnight from a bot! " + ctx.author.mention)
		else:
			await ctx.send("Goodbye Old Friend " + input)
	
	#Removed Help Command
	client.remove_command('help')




	client.run(token)