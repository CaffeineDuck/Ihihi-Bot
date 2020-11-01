import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, BucketType, cooldown
from datetime import datetime, timedelta
import asyncio
import json

class Moderation(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command(aliases=['m'])
	@commands.has_permissions(manage_roles = True)
	async def mute(self, ctx, user:discord.Member = None, time:int = None):
		if not user:
			await ctx.send("Please specify whom to mute")
		else:
			role = discord.utils.get(ctx.guild.roles, name="Muted")
			if not role:
				perms = discord.Permissions(send_messages=False, read_messages=True)
				await ctx.guild.create_role(name="Muted", permissions = perms)
				role = discord.utils.get(ctx.guild.roles, name="Muted")
			await user.add_roles(role)

			if not time:
				embed = discord.Embed(description = "Has been muted!" )
				embed.set_author(name= user, url=user.avatar_url, icon_url=user.avatar_url)
				embed.set_footer(text=f'Requested by {ctx.author}')
				await ctx.send(embed=embed, delete_after=5)
			else:
				embed1 = discord.Embed(description = f"Has been muted for {time} minutes!" )
				embed1.set_author(name= user, url=user.avatar_url, icon_url=user.avatar_url)
				embed1.set_footer(text=f'Requested by {ctx.author}')
				await ctx.send(embed=embed1, delete_after=5)

				if role in user.roles:
					await asyncio.sleep(time*60)
					await user.remove_roles(role)
					embed2 = discord.Embed(description = f"Has been unmuted after {time} minutes!" )
					embed2.set_author(name= user, url=user.avatar_url, icon_url=user.avatar_url)
					embed2.set_footer(text=f'Requested by {ctx.author}')
					await ctx.send(embed=embed2, delete_after=5)

		await asyncio.sleep(4)
		Message = ctx.message
		await Message.delete()


	@commands.command(aliases=['um'])
	@commands.has_permissions(manage_roles = True)
	async def unmute(self, ctx, user:discord.Member = None):
		role = discord.utils.get(ctx.guild.roles, name="Muted")
		if not user:
			await ctx.send("Please mention whom to unmute!")
		else:
			if role in user.roles:
				await user.remove_roles(role)
				embed = discord.Embed(description = "Has been unmuted!" )
				embed.set_author(name= user, url=user.avatar_url, icon_url=user.avatar_url)
				embed.set_footer(text=f'Requested by {ctx.author}')
				await ctx.send(embed=embed, delete_after=5)
			else:
				embed = discord.Embed(description = "Hasn't been muted yet!" )
				embed.set_author(name= user, url=user.avatar_url, icon_url=user.avatar_url)
				embed.set_footer(text=f'Requested by {ctx.author}')
				await ctx.send(embed=embed, delete_after=5)

		await asyncio.sleep(4)
		Message = ctx.message
		await Message.delete()


	@commands.command(aliases=['k'])
	@has_permissions(kick_members = True)
	async def kick(self, ctx, user:discord.Member = None,*, reason = "No Reason Specified"):
		if not user:
			await ctx.send("Please specify whom to kick!")
		else:
			await user.kick(reason=reason)
			embed = discord.Embed(description = f"Because {reason}")
			embed.set_author(name= f"{user} has been kick", url=user.avatar_url, icon_url=user.avatar_url)
			embed.set_footer(text=f'Requested by {ctx.author}')
			await ctx.send(embed=embed)
			try:
				await user.send(f"You have been kicked. Reason {reason}")
			except Exception:
				await ctx.send(f"{user.mention}'s DM is closed!", delete_after = 5)

	@commands.command(aliases=['b'])
	@commands.has_permissions(ban_members=True)
	async def ban(self, ctx, user: discord.Member, *, reason=None):
		await user.ban(reason=reason)
		embed = discord.Embed(description = f"Has been Banned, because {reason}")
		embed.set_author(name= user, url=user.avatar_url, icon_url=user.avatar_url)
		embed.set_footer(text=f'Requested by {ctx.author}')
		await ctx.send(embed=embed)
		try:
			await user.send(f"You have been banned. Reason {reason}")
		except Exception:
			await ctx.send(f"{user.mention}'s DM is closed!", delete_after = 5)


	# The below code unbans player.
	@commands.command(aliases=['ub'])
	@commands.has_permissions(administrator=True)
	async def unban(self, ctx, *, member):
		banned_users = await ctx.guild.bans()
		try:
			member_name, member_discriminator = member.split("#")
		except Exception:
			await ctx.send("Use command properly! eg: `.unban MEE6#4876`")

		for ban_entry in banned_users:
			user = ban_entry.user

			if (user.name, user.discriminator) == (member_name, member_discriminator):
				await ctx.guild.unban(user)
				await ctx.send(f'Unbanned {user.mention}')
	
	@commands.command(aliases=['w'])
	@commands.has_permissions(kick_members = True)
	async def warn(self, ctx, user: discord.Member = None, *, reason = "No reason provided"):
		if not user:
			await ctx.send("DUMBASS mention whom to warn!")
		else:
			embed = discord.Embed(description = f"Because {reason}")
			embed.set_author(name= f"{user} has been warned", url=user.avatar_url, icon_url=user.avatar_url)
			embed.set_footer(text=f'Requested by {ctx.author}')
			await ctx.send(embed=embed)
			try:
				await user.send(f"You have been warned. Reason {reason}")
			except Exception:
				await ctx.send(f"{user.mention}'s DM is closed!", delete_after = 5)


	@commands.command(name='purge')
	async def purge(self, ctx, num_messages: int = 10):
		"""
		Clear <n> messages from current channel
		"""
		channel = ctx.message.channel
		await ctx.message.delete()
		await channel.purge(limit=num_messages, check=None, before=None)
		await ctx.send(f"`{num_messages} messages has been deleted!`", delete_after=5)


	@commands.command(name='purge_user', hidden=True, aliases=['purgeu', 'purgeuser'],)
	async def purge_user(self, ctx, user: discord.Member, num_messages: int = 10):
		"""
		Clear all messagges of <User> within the last [n=10] messages
		"""
		channel = ctx.message.channel

		def check(msg):
			return msg.author.id == user.id

		await ctx.message.delete()
		await channel.purge(limit=num_messages, check=check, before=None)
		await ctx.send(f"`{num_messages} messages from {user} deleted!`", delete_after=5)
	
	@commands.command()
	@cooldown(1, 300, BucketType.user)
	@commands.is_owner()
	async def nuke(self, ctx, channels : discord.TextChannel=None):
		if channels == None:
			await ctx.send('Give a channel')
			return
		if ctx.author != ctx.guild.owner:
			await ctx.send('Only **{}** Can use this Command'.format(ctx.guild.owner))
		else:
			verif = await ctx.send('Are you sure!')
			await ctx.send('Type in `yes`. To proceed')

			def check(m):
				user = ctx.author
				return m.author.id == user.id and m.content == 'yes'

			msg = await self.bot.wait_for('message', check=check)
			await ctx.channel.send('Theres no going back!\n**Are you sure.** \n Type in `yes` to proceed!')
			def check(m):
				user = ctx.author
				return m.author.id == user.id and m.content == 'yes'

			msg = await self.bot.wait_for('message', check=check)
			new = await channels.clone()
			await channels.delete()
			await new.send('https://media1.tenor.com/images/6c485efad8b910e5289fc7968ea1d22f/tenor.gif?itemid=5791468')
			await asyncio.sleep(2)
			await new.send(f'**{self.bot.user.name}** has nuked this channel!')

	@commands.command(aliases=['nick'])
	@commands.has_guild_permissions(manage_nicknames=True)
	async def nickname(self, ctx, member : discord.Member, *args):
		if member == None:
			await ctx.send('Give me a user dumbass')
		elif member == ctx.guild.owner:
			await ctx.send('You cant name the owner!')
		else:
			x = ' '.join(map(str, args))
			await member.edit(nick=f'{x}')
			await ctx.send(f'{member.name} has been changed to {x}')

	@commands.command()
	@commands.has_guild_permissions(manage_channels=True)
	@commands.cooldown(1, 60, BucketType.user)
	async def slowmode(self, ctx, time : int=0):
		if time < 0:
			await ctx.send('Give a positive number.')
			return
		try:
			if time > 21600:
				await ctx.send('Number is too large. You can only have a maximum time of `21600` seconds (6 Hours)')
			else:
				await ctx.channel.edit(slowmode_delay=time)
				await ctx.send(f'The channel {ctx.channel.name} now has a slowmode of {time} seconds')
		except Exception:
			await ctx.send('Not a number!')

	@commands.command()
	@commands.has_permissions(manage_channels=True)
	async def lock(self, ctx, channel: discord.TextChannel=None):
		channel = channel or ctx.channel

		if ctx.guild.default_role not in channel.overwrites:
			overwrites = {
			ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False)
			}
			await channel.edit(overwrites=overwrites)
			await ctx.send("**The channel `{}` has successfully been locked!**".format(ctx.channel.name))
		elif channel.overwrites[ctx.guild.default_role].send_messages == True or channel.overwrites[ctx.guild.default_role].send_messages == None:
			overwrites = channel.overwrites[ctx.guild.default_role]
			overwrites.send_messages = False
			await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
			await ctx.send("**The channel `{}` has successfully been locked!**".format(ctx.channel.name))
		else:
			overwrites = channel.overwrites[ctx.guild.default_role]
			overwrites.send_messages = True
			await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
			await ctx.send('**The channel `{}` has now been unlocked!**'.format(ctx.channel.name))
	
	@commands.command(aliases=['sw', 'setwelcome', 'set_w'])
	async def set_welcome(self, ctx, channel : discord.TextChannel=None):
		if channel == None:
			await ctx.send('You havent provided a valid channel!')
		else:
			with open('JSON/welcome.json', 'r') as f:
				welcome_id = json.load(f)
			welcome_id[str(ctx.guild.id)] = f'{channel.id}'
			with open('JSON/welcome.json', 'w') as f:
				json.dump(welcome_id, f, indent=4)
			await ctx.send(f'The welcomes channel has been set as `{channel.name}`.')

	@commands.command(aliases=['rw', 'remove_w', 'r_welcome', 'removewelcome', 'rwelcome'])
	async def remove_welcome(self, ctx):
		with open('JSON/welcome.json', 'r') as f:
			welcome_id = json.load(f)
		welcome_id[str(ctx.guild.id)] = f'Not Set'
		with open('JSON/welcome.json', 'w') as f:
			json.dump(welcome_id, f, indent=4)
		await ctx.send(f'You have removed the welcome messages!')

def setup(bot):
	bot.add_cog(Moderation(bot))
			
	