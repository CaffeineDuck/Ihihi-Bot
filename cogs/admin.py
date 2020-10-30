import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from datetime import datetime, timedelta
import asyncio

class admin(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(aliases=['user', 'info'])
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def whois(self, ctx, user: discord.Member = None):
		if user == None:
			user = ctx.author


		"""
		Variables for the EMBED DOWN
		"""
		mentions = [role.mention for role in user.roles]
		roles = mentions[1:]
		no_of_roles = len(roles)
		fmt = "%a, %b %d, %Y, %I:%M %p"
		created_at = user.created_at.strftime(fmt)
		joined_at = user.joined_at.strftime(fmt)
		permission = []
		acknowledgement = []


		"""
		Manages the shitty role description in a cleaner way! 
		(COULD HAVE DONE IT IN A BETTER WAY; SORRY FOR THE HASSLE FUTURE ME :)
		"""
		for perms in user.guild_permissions:
			if "administrator" in perms and 'False' in str(perms[1]):
				acknowledgement.append('Member')
			elif "administrator" in perms and 'True' in str(perms[1]):
				permission.append('Administrator')
				acknowledgement.append('Administrator')
			if "manage_guild" in perms and 'True' in str(perms[1]):
				permission.append('Manage Server')
			if "manage_nicknames" in perms and 'True' in str(perms[1]):
				permission.append('Manage Nicknames')
			if "manage_messages" in perms and 'True' in str(perms[1]):
				permission.append('Manage Message')
			if "kick_members" in perms and 'True' in str(perms[1]):
				permission.append('Kick Members')
			if "ban_members" in perms and 'True' in str(perms[1]):
				permission.append('Ban Members')
			if "manage_roles" in perms and 'True' in str(perms[1]):
				permission.append('Manage Roles')
			if "embed_links" in perms and 'True' in str(perms[1]):
				permission.append('Embed Links')
			if "mention_everyone" in perms and 'True' in str(perms[1]):
				permission.append('Mention Everyone')
			if "manage_channels" in perms and 'True' in str(perms[1]):
				permission.append('Manage Channels')
		

		"""
		Checks if the user is server owner
		"""
		if user == ctx.guild.owner:
			acknowledgement.append('Server Owner')

		if roles == []:
			roles.append('@everyone')
			no_of_roles = 1


		"""
		Converting the list into a string
		"""
		roles = roles[::-1]
		roles = ' '.join(roles)
		permission = ', '.join(permission)
		acknowledgement = ', '.join(acknowledgement)
		

		"""
		Main Embed
		"""
		embed = discord.Embed(description = user.mention, colour = discord.Color.blue())
		embed.set_author(name= user, url=user.avatar_url, icon_url=user.avatar_url)
		embed.add_field(name= "**Joined**", value = joined_at  , inline = True)
		embed.add_field(name= "**Registered**", value = created_at  , inline = True)
		embed.add_field(name= f"**Roles**[{no_of_roles}]", value = roles  , inline = False)
		embed.add_field(name= "**Permissions**", value = permission  , inline = False)
		embed.add_field(name= "**Acknowledgements**", value = acknowledgement  , inline = False)
		embed.set_thumbnail(url=user.avatar_url)
		embed.set_footer(text = f"ID: {user.id} • RIGHT NOW!")
		await ctx.send(embed=embed)

	@commands.command(aliases = ['av', 'pp'])
	async def avatar(self, ctx, user: discord.Member = None):
		if not user:
			user = ctx.author

		embed = discord.Embed(title = 'Avatar', colour = discord.Color.blue())
		embed.set_author(name= user, url=user.avatar_url, icon_url=user.avatar_url)
		embed.set_image(url=user.avatar_url)
		embed.set_footer(text = f"Requested by {user}")
		
		await ctx.send(embed=embed)
	
	
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
	async def kick(self, ctx, user:discord.Member = None,*, reason = None):
		if not user:
			await ctx.send("Please specify whom to kick!")
		else:
			await user.kick(reason=reason)
			embed = discord.Embed(description = f"Has been Kicked, because {reason}")
			embed.set_author(name= user, url=user.avatar_url, icon_url=user.avatar_url)
			embed.set_footer(text=f'Requested by {ctx.author}')
			await ctx.send(embed=embed)
	
	@commands.command(aliases=['b'])
	@commands.has_permissions(ban_members=True)
	async def ban(self, ctx, user: discord.Member, *, reason=None):
		await user.ban(reason=reason)
		embed = discord.Embed(description = f"Has been Banned, because {reason}")
		embed.set_author(name= user, url=user.avatar_url, icon_url=user.avatar_url)
		embed.set_footer(text=f'Requested by {ctx.author}')
		await ctx.send(embed=embed)

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


			
def setup(bot):
	bot.add_cog(admin(bot))
