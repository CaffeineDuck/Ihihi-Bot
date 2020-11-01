import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, BucketType, cooldown
from datetime import timedelta
import datetime
import asyncio
import time
import math
import random

def convert_size(bytes):
   if bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(bytes, 1024)))
   p = math.pow(1024, i)
   s = round(bytes / p, 2)
   return "%s %s" % (s, size_name[i])


class info(commands.Cog):
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
		embed = discord.Embed(description = user.mention, timestamp = ctx.message.created_at, colour = discord.Color.blue())
		embed.set_author(name= user, url=user.avatar_url, icon_url=user.avatar_url)
		embed.add_field(name= "**Joined**", value = joined_at  , inline = True)
		embed.add_field(name= "**Registered**", value = created_at  , inline = True)
		embed.add_field(name= f"**Roles**[{no_of_roles}]", value = roles  , inline = False)
		embed.add_field(name= "**Permissions**", value = permission  , inline = False)
		embed.add_field(name= "**Acknowledgements**", value = acknowledgement  , inline = False)
		embed.set_thumbnail(url=user.avatar_url)
		embed.set_footer(text = f"ID: {user.id}")
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

	"""
	The following command is written by:
	Author: _-*™#7139
	Edited by: Samrid Pandit
	"""

	@commands.command(aliases=['si'])
	@commands.cooldown(1, 5, BucketType.guild)
	async def serverinfo(self, ctx):
		try:
			embed = discord.Embed(
				title=f'{ctx.guild.name}',
				color=discord.Color.red(),
				timestamp= datetime.datetime.utcnow()
			)
			embed.set_thumbnail(url=ctx.guild.icon_url)
			embed.add_field(name='Owner?', value=f'{ctx.guild.owner}')
			embed.add_field(name='Owner ID?', value=f'`{ctx.guild.owner.id}`')
			embed.add_field(name='Owner Created at?', value=f"{ctx.guild.owner.created_at.strftime('%a, %#d %B %Y, %I:%M %p')}", inline=False)
			embed.add_field(name='Server Name?', value=f'{ctx.guild.name}')
			embed.add_field(name='Server ID?', value=f'`{ctx.guild.id}`')
			banner = ctx.guild.region[0]
			banner = list(banner)
			x = banner[0].upper()
			banner.pop(0)
			banner.insert(0, x)
			banner = ''.join(map(str, banner))
			embed.add_field(name='Region?', value=f'{banner}')
			embed.add_field(name=f'Created at?', value=f"{ctx.guild.created_at.strftime('%a, %#d %B %Y, %I:%M %p')}", inline=False)
			embed.add_field(name="Emoji's?", value=f'{len(ctx.guild.emojis)}')
			embed.add_field(name=f'Members?', value=f'{len(ctx.guild.members)}')
			verif = ctx.guild.verification_level[0]
			verif = list(verif)
			x = verif[0].upper()
			verif.pop(0)
			verif.insert(0, x)
			verif = ''.join(map(str, verif))
			embed.add_field(name=f'Verification Level?', value=f'{verif}')
			if ctx.guild.afk_channel == True:
				embed.add_field(name='AFK Channel?', value=f'{ctx.guild.afk_channel.name}', inline=False)
				embed.add_field(name='AFK Timeout?', value=f'{ctx.guild.afk_timeout}')
			else:
				pass
			
			true = ctx.guild.mfa_level
			if true == 1:
				true = 'Yes!'
			else:
				true = 'No!'
			embed.add_field(name='Admin 2FA?', value=f'{true}')
			boost = ctx.guild.premium_subscription_count
			if boost == 0:
				boost = 'None 😭'
			else:
				pass
			embed.add_field(name='Boosts!', value=f'{boost}')
			level = ctx.guild.premium_tier
			if level == 0:
				count = 2 - ctx.guild.premium_subscription_count
				level = 'Level 0. You need {} more boosts for level 1!'.format(count)
			elif level == 1:
				count = 15 - ctx.guild.premium_subscription_count
				level = 'Level 1. You need {} more boosts for level 2'.format(count)
			elif level == 2:
				count = 30 - ctx.guild.premium_subscription_count
				level = 'Level 2. You need {} more boosts for level 3'.format(count)
			elif level == 3:
				count = ctx.guild.premium_subscription_count
				level = 'Level 3. Max level with a whopping {} boosts!!!'.format(count)
			embed.add_field(name='Channels?', value=f'{len(ctx.guild.channels)}')
			bots = 0
			for member in ctx.guild.members:
				if member.bot == True:
					bots += 1
				else:
					pass
			embed.add_field(name=f'Bots?', value=f'{bots}')
			embed.add_field(name=f'Main Lang?', value=f'{ctx.guild.preferred_locale}')
			embed.add_field(name=f'Emoji Limit?', value=f'{ctx.guild.emoji_limit}')
			embed.add_field(name=f'Bitrate Limit?', value=f'{convert_size(ctx.guild.bitrate_limit)}')
			embed.add_field(name='Filesize Limit?', value=f'{convert_size(ctx.guild.filesize_limit)}')
			embed.add_field(name='Large?', value=f'{ctx.guild.large}')
			embed.add_field(name='Server Level!', value=f'{level}', inline=False)
			embed.set_footer(text=f'Prompted by {ctx.author}', icon_url=ctx.author.avatar_url)
			msg = await ctx.send(embed=embed)
			def reaction_check(m):
				user = ctx.author
				if m.message_id == msg.id and m.user_id == user.id and str(m.emoji) == "▶️":
					return True
				return False
			try:
				await msg.add_reaction('▶️')
				await self.bot.wait_for('raw_reaction_add', check=reaction_check)
				embed = discord.Embed(
					title=f'{ctx.guild.name} Features!',
					color=ctx.author.colour, timestamp=datetime.datetime.utcnow()
				)
				embed.set_thumbnail(url=ctx.guild.icon_url)
				if 'VIP_REGIONS' in ctx.guild.features:
					embed.add_field(name='VIP Region?', value=' Yes!')
				else:
					embed.add_field(name='VIP Region?', value=' Nope!')
				if 'VANITY_URL' in ctx.guild.features:
					embed.add_field(name='Vanity URL?', value=' Yes!')
				else:
					embed.add_field(name='Vanity URL?', value=' Nope!')
				if 'INVITE_SPLASH' in ctx.guild.features:
					embed.add_field(name='Invite Splash?', value=' Yes!')
				else:
					embed.add_field(name='Invite Splash?', value=' Nope!')
				if 'VERIFIED' in ctx.guild.features:
					embed.add_field(name='Verified?', value=' Yes!')
				else:
					embed.add_field(name='Verified?', value=' Nope!')
				if 'PARTENERED' in ctx.guild.features:
					embed.add_field(name='Partner?', value=' Yes!')
				else:
					embed.add_field(name='Partner?', value=' Nope!')
				if 'MORE_EMOJI' in ctx.guild.features:
					embed.add_field(name="50+ Emoji Allowance?", value=f' Yes!')
				else:
					embed.add_field(name='50+ Emoji Allowance?', value=' Nope!')
				if 'DISCOVERABLE' in ctx.guild.features:
					embed.add_field(name='Discoverable?', value=' Yes!')
				else:
					embed.add_field(name='Discoverable?', value=' Nope!')
				if 'FEATURABLE' in ctx.guild.features:
					embed.add_field(name='Featured?', value=' Yes!')
				else:
					embed.add_field(name='Featured?', value=' Nope!')
				if 'COMMUNITY' in ctx.guild.features:
					embed.add_field(name='Community?', value=' Yes!')
				else:
					embed.add_field(name='Community?', value=' Nope!')
				if 'COMMERCE' in ctx.guild.features:
					embed.add_field(name='Commerce?', value=' Yes!')
				else:
					embed.add_field(name='Commerce?', value=' Nope!')
				if 'PUBLIC' in ctx.guild.features:
					embed.add_field(name='Public?', value=' Yes!')
				else:
					embed.add_field(name='Public?', value=' Nope!')
				if 'NEWS' in ctx.guild.features:
					embed.add_field(name='Announcements?', value=' Yes!')
				else:
					embed.add_field(name='Announcements?', value=' Nope!')
				if 'BANNER' in ctx.guild.features:
					embed.add_field(name='Banners?', value=' Yes!')
				else:
					embed.add_field(name='Banners?', value=' Nope!')
				if 'ANIMATED_ICON' in ctx.guild.features:
					embed.add_field(name='Animated Icon?', value=' Yes!')
				else:
					embed.add_field(name='Animated Icon?', value=' Nope!')
				if 'WELCOME_SCREEN_ENABLED' in ctx.guild.features:
					embed.add_field(name='Welcome Screen?', value=' Yes!')
				else:
					embed.add_field(name='Welcome Screen?', value=' Nope!')
				embed.set_footer(text=f'Prompted by {ctx.author}', icon_url=ctx.author.avatar_url)
				await msg.clear_reactions()
				await msg.edit(embed=embed)
			except asyncio.TimeoutError:
				await msg.delete()
				await ctx.send('You never reacted in time!')
		except Exception as e:
			await ctx.send(e)


def setup(bot):
	bot.add_cog(info(bot))
