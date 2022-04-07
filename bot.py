import discord
from scraper import get_summary, bbc, aljazeera, get_map

bot = discord.Bot()

@bot.event
async def on_ready():
  print('We have logged in as {0.user}'.format(bot))

@bot.slash_command(guild_ids = [954851709421760522,694962879102976070], description = "Fetch BBC's summary")
async def bbcs_summary(ctx):
  await ctx.respond("BBC's summary:")
  await ctx.send(get_summary(bbc))

@bot.slash_command(guild_ids = [954851709421760522,694962879102976070], description = "Fetch Al Jazeera's summary")
async def aljazeeras_summary(ctx):
  await ctx.respond("Al Jazeera's summary:")
  await ctx.send(get_summary(aljazeera))

@bot.slash_command(guild_ids = [954851709421760522,694962879102976070], description = "Fetch Al Jazeera's map")
async def map_of_ukraine(ctx):
  await ctx.respond("Who controls what today:")
  await ctx.send(get_map())

with open("token") as file:
  bot.run(file.readline())