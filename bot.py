import requests
import json
import discord
from discord.ext import commands, tasks
from discord.utils import get
import logger

#Class to get the list of applicable members
class applicable_members:

    #Variables
    member={}
    people = []
    role_name = "Mods"
    bots=[767279203267379280 ,270904126974590976, 751026843687321660]

    def api(people, mee6API, member):
        #Gets the data from api
        result = requests.get(mee6API).json()

        #Gets specific data related to members
        players = result.get("players")

        #Loop to form dict of player and their xp
        for player in players:
            member[player.get("xp")] = player.get("id")

        #List of user-id of people illegible to get Mod role
        people = list(member.values())[:3]

        #Returns people
        return (people)

#Class For actual Bot management
class samrid_bot:
    #Variables
    token = "NzY3Mjc5MjAzMjY3Mzc5Mjgw.X4vmcQ.HWfMnd0Yv-qxAw8QMV_7U115exI"
    
    #Declaring Prefix
    client = commands.Bot(command_prefix=".", case_insensitive=True)

    @client.event
    async def on_ready():
        print("Bot is ready")
        
    #Response to be given on message
    @client.event
    async def on_message(message):

        try:
            #mee6API
            mee6API = "https://mee6.xyz/api/plugins/levels/leaderboard/"+str(message.guild.id)+"?limit=999&page=0"

            #Checks If the messager isn't bot
            if message.author.id in applicable_members.bots:
                pass
            else:

                #Checks if the message is for making admin changes
                if "give me mod" in message.content:

                    #Need to Run the command after getting the id 
                    applicable_members.api(applicable_members.people, mee6API, applicable_members.member)

                
                    #Variables
                    people = applicable_members.api(applicable_members.people, mee6API, applicable_members.member)
                    person = message.author.id
                    prsn = message.author
                    role_name = applicable_members.role_name

                    #Checks if the person if applicable to get the role        
                    if str(person) in people:
                        role = discord.utils.get(message.guild.roles, name=role_name)
                        await prsn.add_roles(role)
                        print(str(prsn) + " Has Been given Mod Role")
                        await message.channel.send(message.author.mention + " Has been given mod role!")
                    else:
                        await message.channel.send("Get into the top 3 first motherfucker! "+message.author.mention)
                
                else:
                    #RESPONSES TO SHITTY THINGS
                    #Response to imagine
                    if "imagine" == message.content.split()[0]:
                        await message.channel.send("I can't even " + message.content +", bro!")

                    #Response to f
                    elif "f" == message.content.lower():
                        await message.channel.send("f")
        except Exception:
            logger.exception(Exception)

    #Runs the bot after compiling everything
    client.run(token)