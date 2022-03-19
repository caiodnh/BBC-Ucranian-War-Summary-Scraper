import discord
import os
from scraper import get_summary

client = discord.Client()

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.content.startswith('$bbc_summary'):
    await message.channel.send(get_summary())

with open("token") as file:
  client.run(file.readline())