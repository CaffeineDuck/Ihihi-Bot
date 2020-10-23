import discord
from discord.ext import commands

class autoresponse(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	"""
	Autoresponses like f, no u, imagine
	"""
	@commands.Cog.listener()
	async def on_message(self, message):
		"""
		Checks if the message author is bot or now
		"""
		#Checks If the messager isn't bot
		if message.author.bot == True:
			pass
		else:
		#Response to imagine
			if "imagine" in message.content:
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

def setup(bot):
	bot.add_cog(autoresponse(bot))