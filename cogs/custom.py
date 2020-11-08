import discord
from discord.ext import commands
import random


member = []

class custom(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def gn(self, ctx, user: discord.Member = None):
		if not user:
			await ctx.send("Get Naked!")
		else:
			await ctx.send("Get Naked!" + user.mention)
	

	@commands.command()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def henlo(self, ctx, input=None):
		if not input:
			await ctx.send(f"Fuck you! {ctx.author.mention}")
		else:
			await ctx.send(f"Fuck you {input}!")
	

	@commands.command(aliases = ['bye'])
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def byy(self, ctx, *, input=None):
		if not input:
			await ctx.send("Lonenly ass, you are so lonely that you need a bot to say you goodbye! :nauseated_face: " + ctx.author.mention)
		else:
			await ctx.send(f"Goodbye Old Friend {input}")


	@commands.command()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def suk(self, ctx,user: discord.Member = None):
		if not user:
			await ctx.send(f"{ctx.author.mention} How alone can you be to not even find a person in discord for making him/her suck your dick virtually?")
		else:
			await ctx.send(f"{user.mention} Suck {ctx.author.mention}'s DICK!")
	

	@commands.command()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def gg(self, ctx, user: discord.Member = None):
		if not user:
			await ctx.send("Good Game Well Played")
		else:
			await ctx.send(f"Good Game Well Played {user.mention}")
	

	@commands.command()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def muji(self, ctx, user: discord.Member = None):
		if not user:
			await ctx.send("Dherai bigris jatha muji!")
		else:
			await ctx.send(f"Dherai bigris jatha muji! {user.mention}")
	
	@commands.command()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def routine(self, ctx):
		image = "https://cdn.discordapp.com/attachments/766213304846647309/774206708049903616/unknown.png"
		embed = discord.Embed(title="Routine")
		embed.set_image(url=image)
		embed.set_footer(text="I want to DIE!" )
		await ctx.send(embed=embed)


	@commands.command(aliases=['s', 'say'])
	@commands.has_permissions(kick_members = True)
	async def send(self, ctx, member : discord.Member, *, message = "No reason provided"):
		try:
			await member.send(f'{ctx.author.mention} said: {message}')
		except Exception:
			await ctx.send(f'{member.mention} has his/her DMs closed. :(')

	
	@commands.command()
	async def oof(self, ctx, member: discord.Member = None):
		if not member:
			embed = discord.Embed(title="OOF", timestamp = ctx.message.created_at, color=0x50C878)
		else:
			embed = discord.Embed(title=f"OOF {member.mention}", color=0x50C878)
		image = "https://i.kym-cdn.com/entries/icons/original/000/032/425/Screen_Shot_2020-01-14_at_10.34.57_AM.jpg"
		embed.set_image(url=image)
		embed.set_footer(text=f"Requested by {ctx.author}" )
		await ctx.send(embed=embed)

	
	
def setup(bot):
	bot.add_cog(custom(bot))