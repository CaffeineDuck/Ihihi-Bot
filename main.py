import discord
import motor

from helpCommand import CustomBotHelpCommand
from discord import Intents, Embed
from discord.ext import commands, tasks

import watchgod

class CustomBot(commands.Bot):
        def __init__(self, config: Mapping[str, Any] = None, config_path: str = None, extensions_dir: str = 'cogs', *args, **kwargs):
        # Checking if arguments were passed properly
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
            help_command=CustomBotHelpCommand(),
            *args, **kwargs
        )

        self.load_extensions()