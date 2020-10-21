import discord
from discord.ext import commands
import requests

member={}
people = []
role_name = "Mods"

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

	#Returns
	return(people)

class role_by_xp(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command()
	async def mod(self, ctx):
		#Variables
		mee6API = "https://mee6.xyz/api/plugins/levels/leaderboard/"+str(ctx.guild.id)+"?limit=999&page=0"
		peoples = api(people, mee6API, member)
		person = ctx.author.id
		prsn = ctx.author
		peopless =[]

		# role_member = client.role_name.members
		for user in peoples:
			users = await self.bot.fetch_user(user)
			peopless.append(users)
		
		#Checks if the person if applicable to get the role        
		if str(person) in peoples:
			role = discord.utils.get(ctx.guild.roles, name=role_name)
			await prsn.add_roles(role)
			print(str(prsn) + " Has Been given Mod Role")
			await ctx.send(ctx.author.mention + " Has been given mod role!")
		elif str(person) != people:
			await ctx.send("Get into the top 3 first motherfucker! " + ctx.author.mention)

		#remove the roles of people who aren't applicable
		for members in list(ctx.guild.members):
			if members in peopless:
				pass
			else:
				role = discord.utils.get(ctx.guild.roles, name=role_name)
				await members.remove_roles(role)


def setup(bot):
	bot.add_cog(role_by_xp(bot))
