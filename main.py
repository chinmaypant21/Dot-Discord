import discord
import requests
import json
import io
import aiohttp
from os import environ 
BOT_TOKEN = environ['DISCORD_DOT_TOKEN']
link = "https://meme-api.herokuapp.com/gimme"
bot = discord.Client()
'''NSFW FILTER TODO'''

def message_activities(msg):
  activities = {
    ".hello":1,
    ".bye":2,
    ".info":3
  }
  if msg in activities:
    return activities[msg]
  else:
    return None

@bot.event
async def on_ready():
  print(f"Logged In as {bot.user}")

@bot.event
async def on_message(msg):
  # If message is the one which is sent by this bot
  if(msg.author != bot.user and msg.content.startswith(".")):
    response = requests.request("GET",link)
    json_data = response.json()
    img_url = json_data["url"]

    async with aiohttp.ClientSession() as session:
      async with session.get(img_url) as resp:
        if resp.status != 200:
            print('Could not download file...')
            return
        data = io.BytesIO(await resp.read())
        await msg.channel.send(file=discord.File(data, 'image.png'))
    # reply = message_activities(msg.content)
    # if reply is not None:
    #   await msg.channel.send(reply)
    
bot.run(BOT_TOKEN)
