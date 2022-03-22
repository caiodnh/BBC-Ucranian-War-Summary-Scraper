import discord
from scraper import get_summary

bot = discord.Bot()

@bot.event
async def on_ready():
  print('We have logged in as {0.user}'.format(bot))

@bot.slash_command(guild_ids = [954851709421760522,694962879102976070], description = "Fetch BBC's summary about the war on Ukraine")
async def bbc_summary(ctx):
  post = get_summary()
  try:
    await ctx.respond(post) # raises an exception if it takes more than 3s
  except:
    await ctx.send(post)

with open("token") as file:
  bot.run(file.readline())