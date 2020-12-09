from discord.ext import commands
import os


class OwnerCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    # Hidden means it won't show up on the default help.
    @commands.command(name='load', hidden=True)
    @commands.is_owner()
    async def load(self, ctx, *, cog: str):
        """Command which Loads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.load_extension(f'cogs.{cog}')
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send(f"**`SUCCESS`**, The cog `{cog.replace('cogs.','')}` has been loaded!")

    @commands.command(name='unload', hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, *, cog: str):
        """Command which Unloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.unload_extension(f'cogs.{cog}')
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send(f"**`SUCCESS`**, The cog `{cog.replace('cogs.','')}` has been unloaded!")

    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, *, cog: str):
        """Command which Reloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.unload_extension(f'cogs.{cog}')
            self.bot.load_extension(f'cogs.{cog}')
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send(f"**`SUCCESS`**, The cog `{cog.replace('cogs.','')}` has been reloaded!")
    
    @commands.command()
    @commands.is_owner()
    async def sync(self, ctx):
        msg = await ctx.send(f'Syncing {self.bot.user.name} now!')
        for file in os.listdir('./cogs'):
            if file.endswith('.py'):
                try:
                    self.bot.reload_extension(f"cogs.{file[:-3]}")
                except Exception:
                    pass
        await msg.edit(content=f'{self.bot.user.name} has been synced!')


def setup(bot):
    bot.add_cog(OwnerCog(bot))