import discord
from discord.ext import commands

class error_handler(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	"""
	This part does the ON READY SHIT
	"""
	@commands.Cog.listener()
	async def on_ready(self):
		await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Your  THICC  ass"))
		print("GOD HAS AWOKEN!")

	"""
	This Part Handles all the errors!
	"""

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		if isinstance(error, commands.NSFWChannelRequired):
			image = "https://i.imgur.com/oe4iK5i.gif"
			embed = discord.Embed(title="NSFW not allowed here", description = "Use NSFW commands in a NSFW marked channel (look in channel settings, dummy")
			embed.set_image(url=image)
			embed.set_footer(text="GOTO NSFW CHANNEL DUMBASS" )
			await ctx.send(embed=embed)
		elif isinstance(error, commands.RoleNotFound):
			await ctx.send("Role not found!")
		elif isinstance(error, commands.MissingRequiredArgument):
			await ctx.send("Please add the missing arguments!")
		elif isinstance(error, commands.CommandOnCooldown):
			await ctx.send(f"Wait for a while dumbass! {ctx.author.mention} {error}.")
		elif isinstance(error, commands.CommandInvokeError):
			await ctx.send(error)
		else:
			raise error
def setup(bot):
	bot.add_cog(error_handler(bot))