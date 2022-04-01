import discord
from scraper import get_summary, bbc, aljazeera

bot = discord.Bot()

@bot.event
async def on_ready():
  print('We have logged in as {0.user}'.format(bot))

@bot.slash_command(guild_ids = [954851709421760522,694962879102976070], description = "Fetch BBC's summary")
async def bbcs_summary(ctx):
  await ctx.respond("BBC's summary:")
  await ctx.send(get_summary(bbc))

@bot.slash_command(guild_ids = [954851709421760522,694962879102976070], description = "Fetch BBC's summary")
async def aljazeeras_summary(ctx):
  await ctx.respond("Al Jazeera's summary:")
  await ctx.send(get_summary(aljazeera))

with open("token") as file:
  bot.run(file.readline())