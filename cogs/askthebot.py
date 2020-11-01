from discord.ext import commands
import discord
import random

class askthebot(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command(aliases = ['gay','gayr8', 'gae'])
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def gayrate(self, ctx, user: discord.Member = None):
		if user == None:
			user = ctx.author
		gayr8 = random.randrange(1,100)
		rate = f"{user.mention}, You are {str(gayr8)}% Gay!"
		embed = discord.Embed(title = "Gay Rate", description = rate, colour = discord.Colour.green())
		await ctx.send(embed=embed)

	@commands.command()
	async def anyone(self, ctx,*, input = None):
		guild_members = ctx.guild.members
		members = [member for member in guild_members if not member.bot]
		member = random.choice(members)
		if input == None:
			await ctx.send(f"{member.mention} is the chosen one!")
		else:
			await ctx.send(f"{member.mention} is chosen to {input}!")
		
	@commands.command()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def waifu(self, ctx, user: discord.Member = None):
		if not user:
			user = ctx.author

		waifu = random.randrange(1,10)

		if waifu == 1 or waifu == 2:
			emoji = ":face_vomiting:"
		elif waifu == 3 or waifu == 4:
			emoji = ":nauseated_face:"
		elif waifu == 5 or waifu == 6:
			emoji = ":cold_sweat:"
		elif waifu == 7:
			emoji = ":kissing:"
		elif waifu == 8:
			emoji = ":smirk:"
		elif waifu == 9:
			emoji = ":relaxed:"
		elif waifu == 10:
			emoji = ":heart_eyes:"

		rate = f"{user.mention}, You are {str(waifu)}/10 waifu! {emoji}"

		embed = discord.Embed(title = "Waifu Rate", description = rate, colour = discord.Colour.red())
		await ctx.send(embed=embed)
	
def setup(bot):
	bot.add_cog(askthebot(bot))
	
