"""
Some Parts of the code in here is authored by Seniatical | Modified By: Samrid Pandit
"""

import discord
from discord.ext import commands, tasks
from itertools import cycle
from asyncio import sleep

status = cycle(['status 1', 'status 2'])

def convert(time):
	day = time // (24 * 3600)
	time = time % (24 * 3600)
	hour = time // 3600
	time %= 3600
	minutes = time // 60
	time %= 60
	seconds = time
	return "%d:%d:%d:%d" % (day, hour, minutes, seconds)


class error_handler(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
	
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
		elif isinstance(error, commands.CommandNotFound):
			pass
		if isinstance(error, commands.CommandOnCooldown):
			global time
			time = error.retry_after
			time = convert(time)
			x = time.split(':')
			if x[1] != '0' and x[2] != '0':
				if x[1] == 1:
					message = f'Retry this command after **{x[1]}** hour and **{x[2]}** minutes!'
				else:
					message = f'Retry this command after **{x[1]}** hours and **{x[2]}** minutes!'
			elif x[1] == '0' and x[2] != '0' and x[3] != '0':
				message = f'Retry this command after **{x[2]}** minutes and **{x[3]}** seconds!'
			elif x[3] != '0' and x[1] == '0' and x[2] == '0':
				message = f'Retry this command after **{x[3]}** seconds!'
			msg = await ctx.send(message)
			await sleep(3)
			await msg.delete()
		elif isinstance(error, commands.RoleNotFound):
			await ctx.send("Role not found!")
		elif isinstance(error, commands.MissingRequiredArgument):
			msg = await ctx.send(f'**You have made an error.**\n\n{error.param}')
			await sleep(3)
			await msg.delete()
		elif isinstance(error, commands.TooManyArguments):
			msg = await ctx.send(f'You have given too many args.\nPlease use the command as directed \n {error.param}.')
			await sleep(3)
			await msg.delete()
		elif isinstance(error, commands.BotMissingPermissions):
			msg = await ctx.send('I am missing permissions.')
			await sleep(3)
			await msg.delete()
		elif isinstance(error, commands.MissingPermissions):
			msg = await ctx.send(f'You need **{error.missing_perms[0]}** perms to complete this actions.')
			await sleep(3)
			await msg.delete()
		elif isinstance(error, commands.BotMissingAnyRole):
			msg = await ctx.send(f'**Woops!**\n\nLooks like i am missing the {error.missing_role} role.')
			await sleep(3)
			await msg.delete()
		elif isinstance(error, commands.CheckAnyFailure):
			msg = await ctx.send('An unknown error has occured.')
			await sleep(3)
			await msg.delete()
		elif isinstance(error, commands.errors.NotOwner):
			msg = await ctx.send(f'Only **{ctx.guild.owner}** can use this command.')
			await sleep(3)
			await msg.delete()
		elif isinstance(error, commands.errors.NoPrivateMessage):
			msg = await ctx.send("The user has blocked me or has the DM's closed.")
			await sleep(3)
			await msg.delete()
		elif isinstance(error, discord.ext.commands.DisabledCommand):
			msg = await ctx.send('This command is disabled.')
			await sleep(3)
			await msg.delete()
		elif isinstance(error, discord.errors.Forbidden):
			msg = await ctx.send('I do not have permissions for this command!')
			await sleep(3)
			await msg.delete()
		else:
			await ctx.send(error)
			
def setup(bot):
	bot.add_cog(error_handler(bot))