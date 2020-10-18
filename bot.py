import requests
import json

#Global Variables
member={}

#Gets the data from api
request = requests.get("https://mee6.xyz/api/plugins/levels/leaderboard/766213304141086731?limit=999&page=0")

#Converts the json into Dictionary
result = request.json()

#Gets specific data related to members
players = result.get("players")

#Loop to form dict of player and their xp
for player in players:
    member[player.get("xp")] = player.get("id")

#List of user-id of people illegible to get Mod role
people = list(member.values())[:3]

