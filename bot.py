import discord
from scraper import bbc, aljazeera

bot = discord.Bot()

@bot.event
async def on_ready():
  print('We have logged in as {0.user}'.format(bot))

@bot.slash_command(guild_ids = [954851709421760522,694962879102976070], description = "Fetch BBC's summary")
async def bbcs_summary(ctx):
  await ctx.respond("BBC's summary:")
  try:
    await ctx.send(bbc.render_summary_points())
  except Exception as error:
    await ctx.send(f"ERROR: {error}")

@bot.slash_command(guild_ids = [954851709421760522,694962879102976070], description = "Fetch Al Jazeera's summary")
async def aljazeeras_summary(ctx):
  await ctx.respond("Al Jazeera's summary:")
  try:
    await ctx.send(aljazeera.render_summary_points())
  except Exception as error:
    await ctx.send(f"ERROR: {error}")

@bot.slash_command(guild_ids = [954851709421760522,694962879102976070], description = "Fetch Al Jazeera's map")
async def map_of_ukraine(ctx):
  await ctx.respond("Who controls what today:")
  try:
    await ctx.send(aljazeera.get_map())
  except Exception as error:
    await ctx.send(f"ERROR: {error}")
  

with open("token") as file:
  bot.run(file.readline())