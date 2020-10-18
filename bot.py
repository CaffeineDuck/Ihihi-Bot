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
    member[player.get("id")] = player.get("xp")

#Gives the userid of member with max xp
max_xp_member = max(member, key=member.get)