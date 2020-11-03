import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, BucketType, cooldown
from datetime import datetime, timedelta
import asyncio
import json
import pymongo
import os

"""
Checks if it is in a local machine
"""
try:
	os.environ['TEST']
	is_local = True
except Exception:
	is_local = False

class Moderation(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		"""
		Mongo Db
		"""
		self.mongoclient = os.environ['MONGOCLIENT']
		self.bot_mongo = pymongo.MongoClient(self.mongoclient)
		self.db = self.bot_mongo.ihihihibot_db
		"""
		As I host my bot, i have a testing bot and a main bot so it 
		fetches the prefix from database according to where its hosted!
		"""
		if is_local:
			self.prefixes = self.db.server_test_prefixes
		else:
			self.prefixes = self.db.server_prefixes
	
	@commands.command(aliases=['m'])
	@cooldown(1, 10, BucketType.user)
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
	@cooldown(1, 60, BucketType.user)
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
	@cooldown(1, 100, BucketType.user)
	@commands.has_permissions(ban_members=True)
	async def ban(self, ctx, user: discord.Member, *, reason=None):
		await user.ban(reason=reason)
		embed = discord.Embed(description = f"Has been Banned, because {reason}")
		embed.set_author(name= user, url=user.avatar_url, icon_url=user.avatar_url)
		embed.set_footer(text=f'Requested by {ctx.author}')
		await ctx.send(embed=embed)
		await user.send(f"You have been banned. Reason {reason}")
	


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
	@cooldown(1, 10, BucketType.user)
	@commands.has_permissions(kick_members = True)
	async def warn(self, ctx, user: discord.Member = None, *, reason = "No reason provided"):
		if not user:
			await ctx.send("DUMBASS mention whom to warn!")
		else:
			embed = discord.Embed(description = f"Because {reason}")
			embed.set_author(name= f"{user} has been warned", url=user.avatar_url, icon_url=user.avatar_url)
			embed.set_footer(text=f'Requested by {ctx.author}')
			await ctx.send(embed=embed)
			await user.send(f"You have been warned. Reason {reason}")
		


	@commands.command(name='purge')
	async def purge(self, ctx, num_messages: int = 10, user:discord.Member = None):
		"""
		Clear <n> messages from current channel
		"""
		if user:
			channel = ctx.message.channel
			def check(msg):
				return msg.author.id == user.id
			await ctx.message.delete()
			await channel.purge(limit=num_messages, check=check, before=None)
			await ctx.send(f"`{num_messages} messages from {user} deleted!`", delete_after=5)
			return
		channel = ctx.message.channel
		await ctx.message.delete()
		await channel.purge(limit=num_messages, check=None, before=None)
		await ctx.send(f"`{num_messages} messages has been deleted!`", delete_after=5)

			
		
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
	@commands.cooldown(20, 60, BucketType.user)
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
	
	@commands.command()
	async def unlock(self, ctx):
		channel = ctx.channel
		overwrites = channel.overwrites[ctx.guild.default_role]
		overwrites.send_messages = True
		await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
		await ctx.send('**The channel `{}` has now been unlocked!**'.format(ctx.channel.name))
	

	@commands.command(aliases=['sw', 'setwelcome', 'set_w', 'welcome'])
	@cooldown(1, 10, BucketType.user)
	async def set_welcome(self, ctx, channel : discord.TextChannel=None):
		cur = self.prefixes.find_one({'server_id':ctx.guild.id})
		prefix = cur.get('prefix')
	
		def check(m):
			return m.author == ctx.author and m.channel == ctx.channel

		if not channel:
			await ctx.send(f'Please provide a channel \n `{prefix}welcome <#channel>`')
			return
		
		await ctx.send("Please write `yes` if you would like a custom welcome text. \n If you are okay with the defualt welcome message, please type `no`")
		await ctx.send("PLEASE REPLY WITH A VALID CUSTOM MESSAGE WITHIN 20 SECONDS OR TYPE **ABORT** TO CANCEL!")
		custom_bool = await self.bot.wait_for('message', check=check, timeout = 20)
		if custom_bool.content.lower() in ['no','n']:

			old_data  = self.prefixes.find_one({'server_id' : ctx.guild.id})
			new_data = { "$set": {
							'welcome_channel': channel.id,
							'custom_message': None
					}
			}
			self.prefixes.update_one(old_data, new_data)
			print(f"Welcome channel for server {ctx.guild.id} has been added!")
			await ctx.send(f'The welcomes channel has been set as `{channel.name}`.')	

		elif custom_bool.content.lower() in ['yes','y']:
			await ctx.send("Please type the custom message!")
			await ctx.send("PLEASE REPLY WITH A VALID CUSTOM MESSAGE WITHIN 100 SECONDS OR TYPE **ABORT** TO CANCEL!")
			
			custom_message = await self.bot.wait_for('message', check=check, timeout=100)
			if custom_message.content.lower() == "abort":
				return
			else:
				old_data  = self.prefixes.find_one({'server_id' : ctx.guild.id})
				new_data = { "$set": {
								'welcome_channel': channel.id,
								'custom_message': f'{str(custom_message.content)}'
						}
			}
			self.prefixes.update_one(old_data, new_data)
			print(f"Welcome channel for server {ctx.guild.id} has been added!")
			await ctx.send(f'The welcomes channel has been set as `{channel.name}`.')
	


		


	@commands.command(aliases=['rw', 'remove_w', 'r_welcome', 'removewelcome', 'rwelcome'])
	@cooldown(1, 60, BucketType.user)
	async def remove_welcome(self, ctx):

		old_data  = self.prefixes.find_one({'server_id' : ctx.guild.id})
		new_data = { "$set": {
						'welcome_channel': None
				}
		}
		self.prefixes.update_one(old_data, new_data)
		print(f"Welcome channel for server {ctx.guild.id} has been removed!")	

		await ctx.send(f'You have removed the welcome messages!')

def setup(bot):
	bot.add_cog(Moderation(bot))
			
	