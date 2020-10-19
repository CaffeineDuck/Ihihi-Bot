import requests
import json
import discord
from discord.ext import commands, tasks
from discord.utils import get

class applicable_members:

    #Variables
    member={}
    mee6API = "https://mee6.xyz/api/plugins/levels/leaderboard/766213304141086731?limit=999&page=0"
    people = []

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

class samrid_bot:

    #Variables
    token = "NzY3Mjc5MjAzMjY3Mzc5Mjgw.X4vmcQ.HWfMnd0Yv-qxAw8QMV_7U115exI"
    role_name = "Mods"
    peoples = applicable_members.api(applicable_members.people, applicable_members.mee6API, applicable_members.member)

    #Declaring Prefix
    client = commands.Bot(command_prefix=".", case_insensitive=True)


    @client.event
    async def on_ready():
        print("Bot is ready")
    
    ppl = peoples[1]
    
    @tasks.loop(seconds=5.0, count=5)
    async def addrole(person, role_n, client):
        member = person
        role = role_n
        await client.add_roles(member, role)

    addrole.start(ppl, role_name, client)
    print(peoples)

    client.run(token)