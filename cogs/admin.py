import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from datetime import datetime, timedelta

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
		embed = discord.Embed(title = f"{user.name}#{user.discriminator}", description = user.mention, colour = discord.Color.blue())
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
		roles = ' '.join(roles)
		permission = ', '.join(permission)
		acknowledgement = ', '.join(acknowledgement)
		

		"""
		Main Embed
		"""
		embed.add_field(name= "**Joined**", value = joined_at  , inline = True)
		embed.add_field(name= "**Registered**", value = created_at  , inline = True)
		embed.add_field(name= f"**Roles**[{no_of_roles}]", value = roles  , inline = False)
		embed.add_field(name= "**Permissions**", value = permission  , inline = False)
		embed.add_field(name= "**Acknowledgements**", value = acknowledgement  , inline = False)
		embed.set_thumbnail(url=user.avatar_url)
		embed.set_footer(text = f"ID: {user.id} • RIGHT NOW!")
		await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(admin(bot))
