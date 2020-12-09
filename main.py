import inspect
import itertools
import logging
import os
import traceback
import warnings
from glob import glob
from typing import Any, Mapping, Tuple

import discord
import pymongo
import yaml
import watchgod
from discord import Intents, Embed
from discord.ext import commands, tasks

from help_command import TabiHelpCommand

logging.basicConfig(level=logging.INFO)


class TabiBot(commands.Bot):

	def __init__(self, config: Mapping[str, Any] = None, config_path: str = None, extensions_dir: str = 'cogs', defualt_prefix: str = '.', *args, **kwargs):
		# Checking if arguments were passed properly

		self.defualt_prefix = defualt_prefix

		config_passed = config is not None
		config_path_passed = config_path is not None
		if not config_passed and not config_path_passed:
			# Missing the data we need, raise an error
			raise ValueError("__init__ expects 'config' or 'config_path' to be provided, but received neither")
		elif config_passed and config_path_passed:
			# Since we have valid data, we just warn the user and move on
			warnings.warn("__init__ received both 'config' and 'config_path', but only one was expected, ignoring file path and using 'config'")
		elif not config_passed:
			# Parse from config file
			with open(config_path) as f:
				self.config = yaml.load(f, yaml.Loader)
		else:
			# Use pre-parsed config
			self.config = config

		self.extensions_dir = extensions_dir

		# Tuple of all activities the bot will display as a status
		self.activities = itertools.cycle((
			discord.Activity(type=discord.ActivityType.watching, name='!help'),
			lambda: discord.Activity(type=discord.ActivityType.listening,
					name=f'{len(bot.commands)} Commands | {len(bot.users)} Users | {len(bot.guilds)} Servers')
		))

		# Declaring intents and initalizing parent class
		intents = Intents.default()
		intents.members = True
		super().__init__(
			intents=intents,
			command_prefix=self.determine_prefix,
			case_insensitive=True,
			help_command=TabiHelpCommand(),
			*args, **kwargs
		)

		self.load_extensions()


	async def mongoClientLoader(self):
		mongoclient = self.config['DATABASE_URI']
		bot = pymongo.MongoClient(mongoclient)
		db = bot.ihihihibot_db
		self.prefixes = db.server_prefixes

	async def determine_prefix(self, bot: commands.Bot, message: discord.Message) -> str:
		"""Determines the prefix to use for command invocation

		Parameters
		----------
		bot : commands.Bot
			The bot that is running
		message : discord.Message
			The message to determine the prefix for

		Returns
		-------
		str
			The prefix for the guild the message is in
		"""
		self.mongoClientLoader()
		cur = self.prefixes.find_one({'server_id':message.guild.id})
		return(cur.get('prefix'))
		if cur:
			return commands.when_mentioned_or(cur.get('prefix'))(bot, message)
		else:
			return commands.when_mentioned_or(self.defualt_prefix)(bot, message)


	def load_extensions(self, reraise_exceptions: bool = False) -> Tuple[Tuple[str], Tuple[str]]:
		"""Loads all extensions

		Parameters
		----------
		reraise_exceptions : bool, optional
			Weather or not to silently continue on error, or raise the exception, by default False

		Returns
		-------
		Tuple[Tuple[str], Tuple[str]]
			A tuple containing a tuple of extensions that loaded successfully,
			followed by a tuple of extensions that failed to load

		Raises
		------
		commands.ExtensionFailed
			There was an error during loading the extension, you can use the 'original'
			atrribute of this exception ot get more details
		commains.NoEntryPointError
			The extension didn't have a setup function visible at the global scope level
		commands.ExtensionAlreadyLoaded
			The extension was already loaded
		commands.ExtensionNotFound
			The path provided contained no valid extensions
		"""
		loaded_extensions = set()
		failed_extensions = set()
		for file in map(lambda file_path: file_path.replace(os.path.sep, '.')[:-3], glob(f'{self.extensions_dir}/**/*.py', recursive=True)):
			try:
				self.load_extension(file)
				loaded_extensions.add(file)
				print(f'{file} loaded')
			except Exception as e:
				failed_extensions.add(file)
				print(f"Failed to load cog {file}")
				if not reraise_exceptions:
					traceback.print_exception(type(e), e, e.__traceback__)
				else:
					raise e
		result = (tuple(loaded_extensions), tuple(failed_extensions))
		return result

	def serve(self) -> None:
		"""Runs the bot, equivilant to calling TabiBot.run(token)"""
		self.run(self.config['DISCORD_TOKEN'])

	@tasks.loop(seconds=10)
	async def status(self):
		"""Cycles through all status every 10 seconds"""
		new_activity = next(self.activities)
		# The commands one is callable so the command counts actually change
		if callable(new_activity):
			await self.change_presence(status=discord.Status.online, activity=new_activity())
		else:
			await self.change_presence(status=discord.Status.online, activity=new_activity)

	@tasks.loop(seconds=1)
	async def cog_watcher_task(self) -> None:
		"""Watches the cogs directory for changes and reloads files"""
		async for change in watchgod.awatch('cogs/', watcher_cls=watchgod.PythonWatcher):
			for change_type, changed_file_path in change:
				try:
					extension_name = changed_file_path.replace(os.path.sep, '.')[:-3]
					if change_type == watchgod.Change.modified:
						try:
							self.unload_extension(extension_name)
						except commands.ExtensionNotLoaded:
							pass
						finally:
							self.load_extension(extension_name)
							print(f'Reloaded {extension_name}')
					elif change_type == watchgod.Change.created:
						self.load_extension(extension_name)
						print(f'Loaded {extension_name}')
					else:
						self.unload_extension(extension_name)
						print(f'Unloaded {extension_name}')
				except (commands.ExtensionFailed, commands.NoEntryPointError) as e:
					traceback.print_exception(type(e), e, e.__traceback__)


	@status.before_loop
	async def before_status(self) -> None:
		"""Ensures the bot is fully ready before starting the task"""
		await self.wait_until_ready()

	async def on_ready(self) -> None:
		"""Called when we have successfully connected to a gateway"""
		print(f'Signed into Discord as {self.user} (ID: {self.user.id})')

		self.status.start()
		self.cog_watcher_task.start()

# Defining root level commands
bot = TabiBot(config_path='config.yaml')

@bot.command(aliases=['where', 'find'])
@commands.is_owner()
async def which(ctx, *, cmd_name: str) -> None:
	"""Finds the cog a command is part of"""
	command = bot.get_command(cmd_name)
	if command is None:
		embed = Embed(
			title='Command not found \U0000274C',
			description='You created me, how could you not remember what commands I have? \U0001F62D',
			color=discord.Color.red()
		)
	else:
		inner_command = command.callback
		command_defined_on = inspect.getsourcelines(inner_command)[1]
		full_command_signature = f'async def {inner_command.__name__}{inspect.signature(inner_command)}'
		if type(command) is commands.Command and not command.parent:
			command_type = 'Standalone command'
		elif type(command) is commands.Group:
			command_type = 'Command group'
		else:
			command_type = f'Subcommand of `{command.parent.qualified_name}`'
		embed = Embed(
			title='Target aquired \U0001F3AF',
			color=discord.Color.green()
		)
		embed.add_field(name='Help text', value=command.help)
		embed.add_field(name='Part of extension', value=command.cog.qualified_name if command.cog is not None else 'Root Module', inline=False)
		embed.add_field(name='Type of command', value=command_type)
		embed.add_field(name='Defined on line', value=command_defined_on, inline=False)
		embed.add_field(name='Signature', value=full_command_signature, inline=False)
	await ctx.send(embed=embed)

@bot.command()
@commands.is_owner()
async def shutdown(ctx) -> None:
	"""Shuts down the bot, owners only"""
	await ctx.send("Logging out.")
	await bot.logout()

@shutdown.error
async def shutdown_error(ctx, error):
	if isinstance(error, commands.NotOwner):
		embed = discord.Embed(
			color=discord.Color.dark_blue(),
			description='You do not have the permissions to do that!'
		)
		await ctx.send(embed=embed)
	else:
		traceback.print_exception(type(error), error, error.__traceback__)

@bot.command()
@commands.is_owner()
async def loadjsk(ctx) -> None:
	"""Loads jishaku for debugging, owners only"""
	await ctx.send("Loaded Jishaku")
	await bot.load_extension("jishaku")

@loadjsk.error
async def loadjsk_error(ctx, error) -> None:
	if isinstance(error, commands.ExtensionAlreadyLoaded):
		await ctx.send("Jishaku is already loaded!")
	if isinstance(error, commands.ExtensionFailed):
		await ctx.send("Error Logged, Look at your traceback for more details")
	else:
		traceback.print_exception(type(error), error, error.__traceback__)

@bot.command()
@commands.is_owner()
async def load(ctx, extention: str) -> None:
	"""Loads an extension, owners only"""
	bot.load_extension(f'cogs.{extention}')
	embed = discord.Embed(
		color=discord.Color.dark_blue(),
		description=f'{extention} Cog has loaded'
	)
	await ctx.send(embed=embed)


@load.error
async def load_error(ctx, error) -> None:
	if isinstance(error, commands.NotOwner):
		embed = discord.Embed(
			color=discord.Color.dark_blue(),
			description='This can only be used by the bot\'s owners!'
		)
	elif isinstance(error, commands.ExtensionAlreadyLoaded):
		embed = discord.Embed(
			color=discord.Color.dark_blue(),
			description='This Extension is already loaded!'
		)
		await ctx.send(embed=embed)
	elif isinstance(error, commands.ExtensionNotFound):
		embed = discord.Embed(
			color=discord.Color.dark_blue(),
			description='This Extension does not exsist!'
		)
		await ctx.send(embed=embed)
	else:
		traceback.print_exception(type(error), error, error.__traceback__)

@bot.command()
@commands.is_owner()
async def unload(ctx, extention) -> None:
	"""Unloads an extension, owners only"""
	bot.unload_extension(f'cogs.{extention}')
	embed = discord.Embed(
		color=discord.Color.dark_blue(),
		description=f'{extention} Cog has been disabled'
	)
	await ctx.send(embed=embed)


@unload.error
async def unload_error(ctx, error) -> None:
	if isinstance(error, commands.NotOwner):
		embed = discord.Embed(
			color=discord.Color.dark_blue(),
			description='This can only be used by the bot\'s owners!'
		)
		await ctx.send(embed=embed)
	elif isinstance(error, commands.ExtensionNotLoaded):
		embed = discord.Embed(
			color=discord.Color.dark_blue(),
			description='This Extension is not loaded!'
		)
		await ctx.send(embed=embed)
	elif isinstance(error, commands.ExtensionNotFound):
		embed = discord.Embed(
			color=discord.Color.dark_blue(),
			description='This Extension does not exist!'
		)
		await ctx.send(embed=embed)
	else:
		traceback.print_exception(type(error), error, error.__traceback__)

@bot.command()
@commands.is_owner()
async def cogs(ctx) -> None:
	"""Shows all loaded extensions, owners only"""
	cogs = []
	
	for cog in bot.cogs:
		cogs.append(f"`{cog}`")

	cogs_str = ', '.join(cogs)
	embed = discord.Embed(
		title=f"All Cogs",
		description = cogs_str,
		colour=discord.Color.dark_blue()
	)
	embed.set_footer(
		text=f'You can always do {ctx.prefix}help to see all cog features!')
	await ctx.send(embed=embed)

@cogs.error
async def cogs_error(ctx, error) -> None:
	if isinstance(error, commands.NotOwner):
		embed = discord.Embed(
			color=discord.Color.dark_blue(),
			description='This can only be used by the bot\'s owners!'
		)
		await ctx.send(embed=embed)
	else:
		traceback.print_exception(type(error), error, error.__traceback__)

@bot.command()
@commands.is_owner()
async def reload(ctx, extension) -> None:
	"""Reloads an extension, owners only"""
	bot.unload_extension(f'cogs.{extension}')
	bot.load_extension(f'cogs.{extension}')
	embed = discord.Embed(
		title=':white_check_mark: **Successfully reloaded ' + extension + '.**')
	await ctx.send(embed=embed)

@reload.error
async def reload_error(ctx, error):
	if isinstance(error, commands.NotOwner):
		embed = discord.Embed(
			color=discord.Color.dark_blue(),
			description='This can only be used by the bot\'s owners!'
		)
	elif isinstance(error, commands.ExtensionNotLoaded):
		embed = discord.Embed(
			color=discord.Color.dark_blue(),
			description='This extension is not loaded!'
		)
		await ctx.send(embed=embed)
	elif isinstance(error, commands.ExtensionNotFound):
		embed = discord.Embed(
			color=discord.Color.dark_blue(),
			description='This extension does not exsist!'
		)
		await ctx.send(embed=embed)
	else:
		traceback.print_exception(type(error), error, error.__traceback__)


if __name__ == '__main__':
	bot.serve()
