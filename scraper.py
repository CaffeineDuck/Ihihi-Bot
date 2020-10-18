import requests
import json

request = requests.get("https://mee6.xyz/api/plugins/levels/leaderboard/766213304141086731?limit=999&page=0")

result = request.json()

players = result.get("players")

member={}

for player in players:
    member[player.get("id")] = player.get("xp")

max_xp_member = max(member, key=member.get)

