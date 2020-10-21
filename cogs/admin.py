import discord
from discord.ext import commands
from datetime import datetime, timedelta

class admin_commands(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(aliases=['user', 'info'])
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def whois(self, ctx, user: discord.Member = None):
		if user == None:
			user = ctx.author

		embed = discord.Embed(title = f"{user.name}#{user.discriminator}", description = user.mention, colour = discord.Color.blue())
		mentions = [role.mention for role in user.roles]
		no_of_roles = len(mentions)
		roles = str(mentions).replace('[', '').replace(']','').replace("\'",'').replace(',','')
		created_at = user.created_at.strftime("%a, %b %d, %Y, %H:%M %p")
		joined_at = user.joined_at.strftime("%a, %b %d, %Y, %H:%M %p")
		fmt = "%H:%M %p"
		message_created = datetime.now().strftime(fmt)

		permission = []
		for perms in user.guild_permissions:
			if "administrator" in perms:
				permission.append('Administrator')
			if "manage_guild" in perms:
				permission.append('Manage Server')
			if "manage_nicknames" in perms:
				permission.append('Manage Nicknames')
			if "manage_messages" in perms:
				permission.append('Manage Message')
			if "kick_members" in perms:
				permission.append('Kick Members')
			if "ban_members" in perms:
				permission.append('Ban Members')
			if "manage_roles" in perms:
				permission.append('Manage Roles')
			if "embed_links" in perms:
				permission.append('Embed Links')
			if "mention_everyone" in perms:
				permission.append('Mention Everyone')

		permission = str(permission).replace('[', '').replace(']','').replace("\'",'')

		embed.add_field(name= "**Joined**", value = joined_at  , inline = True)
		embed.add_field(name= "**Registered**", value = created_at  , inline = True)
		embed.add_field(name= f"**Roles**[{no_of_roles}]", value = roles  , inline = False)
		embed.add_field(name= "**Permissions**", value = permission  , inline = False)
		embed.set_thumbnail(url=user.avatar_url)
		embed.set_footer(text = f"ID: {user.id} • Today at {message_created}")
		await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(admin_commands(bot))
