import discord
from scraper import get_summary

bot = discord.Bot()

@bot.event
async def on_ready():
  print('We have logged in as {0.user}'.format(bot))

# @bot.event
# async def on_message(message):
#   if message.content.startswith('$bbc_summary'):
#     await message.channel.send(get_summary())

@bot.slash_command(guild_ids = [954851709421760522,694962879102976070], description = "Fetch BBC's summary about the war on Ukraine")
async def bbc_summary(ctx):
  await ctx.send(get_summary())

with open("token") as file:
  bot.run(file.readline())