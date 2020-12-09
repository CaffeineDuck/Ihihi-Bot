from datetime import datetime
from typing import Callable, List, Optional

from discord import Embed, Color, TextChannel, Member
from discord.abc import Messageable
from discord.ext.commands import Bot
from discord.message import Message

class Wizard:

    def __init__(self, bot: Bot, commander: Member, items: List[str], prompts: List[str], title, embed_color=0xf1c40f, completed_message: str ='Wizard Complete', response_content_form: str = 'content'):
        self.total_steps = len(items)
        self.embed = Embed(
            title=title,
            description=f'Step 1 of {len(prompts)}',
            color=embed_color,
            timestamp=datetime.utcnow()
        )
        self.waiting = 'Waiting for your input...'
        self.message = None
        self.items = items
        self.prompts = prompts
        self.bot = bot
        self.commander = commander
        self.completed_message = completed_message
        self.response_content_form = response_content_form
        self.__step = 0
    
    @property
    def step(self):
        return self.__step
    
    @step.setter
    def step(self, new):
        self.__step = new
        self.embed.description = f'Step {new} of {self.total_steps}'

    def default_check(self, message: Message):
        return all((message.author == self.commander, message.channel == self.message.channel))
        
    async def start(self, location: Messageable) -> None:
        """Sends the initial wizard

        Parameters
        ----------
        location : discord.abc.Messageable
            The place to send the embed to

        Raises
        ------
        RuntimeError
            If the message has already been sent once before
        """
        if self.message is not None:
            raise RuntimeError('Message already sent')
        else:
            self.embed.add_field(name=self.items[self.step], value=self.waiting, inline=False)
            self.embed.add_field(name='Instruction', value=self.prompts[self.step], inline=False)
            self.message = await location.send(embed=self.embed)

    async def step_forward(self, check: Optional[Callable] = None):
        """Runs one step of the wizard

        Parameters
        ----------
        check : Optional[Callable], optional
            The check to call along with the default one
            which will check for the same author and channel, by default None

        Returns
        -------
        str
            The content of the response
        """
        if check is not None:
            # Combine the user's custom check with the default check
            new_check = lambda m: all((check(m), self.default_check(m)))
        else:
            # No user provided check, use the default
            new_check = self.default_check
        response = await self.bot.wait_for('message', check=new_check)
        response_content = response.content
        if len(response_content) < 1024:
            self.embed.set_field_at(self.step, name=self.items[self.step], value=response_content, inline=False)
        else:
            self.embed.set_field_at(self.step, name=self.items[self.step], value='```Content exceeds embed\'s limit!```', inline=False)
        if self.step + 1 < len(self.items):
            self.step += 1
            self.embed.set_field_at(-1, name='Instruction', value=self.prompts[self.step], inline=False)
            self.embed.insert_field_at(-1, name=self.items[self.step], value=self.waiting, inline=False)
        else:
            self.embed.remove_field(-1)
            self.embed.description = self.completed_message
            self.embed.color = Color.green()
        await self.message.edit(embed=self.embed)
        await response.delete()

        if self.response_content_form == 'object':
            return response
        elif self.response_content_form == 'content':
            return response_content
        else:
            return "Specified return type is not valid!"

    async def run(self, location: Messageable) -> List[str]:
        """Runs the wizard all the way through,
        use this if you don't wish to use any custom
        checks in any step

        Parameters
        ----------
        location : discord.abc.Messageable
            The channel to send the wizard to

        Returns
        -------
        List[str]
            All the responses given
        """
        await self.start(location)
        return [await self.step_forward() for _ in range(self.total_steps)]



