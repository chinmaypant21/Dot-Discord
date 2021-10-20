import discord
import requests
import json
import io
import aiohttp

from os import environ

BOT_TOKEN = environ['DISCORD_DOT_TOKEN']
nsfw_filter = True
meme_api = "https://meme-api.herokuapp.com/gimme"


bot = discord.Client()

def message_activities(msg):
    activities = {".hello": 1, ".bye": 2, ".info": 3}
    if msg in activities:
        return activities[msg]
    else:
        return None


@bot.event
async def on_ready():
    print(f"Logged In as {bot.user}")

async def meme(msg):
  response = requests.request("GET",meme_api)
  json_data = response.json()
  img_url = json_data["url"]
  if nsfw_filter and json_data['nsfw']:
    print("NSFW Found!")
    return await meme(msg)

  async with aiohttp.ClientSession() as session:
    async with session.get(img_url) as resp:
        if resp.status != 200:
            print('Could not download file...')
            return
        data = io.BytesIO(await resp.read())
  await msg.channel.send(file=discord.File(data, 'meme.png'))

async def greet(msg):
  # await msg.channel.send("")
  pass

@bot.event
async def on_message(msg):
    # If message is the one which is sent by this bot
    if (msg.author != bot.user and msg.content.startswith(".")):
      if(msg.content == ".meme"):
        await meme(msg)
      elif msg.content == '.hi':
        await greet(msg)
      else:
        pass
        
      # await msg.channel.send(file=discord.File(await meme(get_meme), 'meme.png'))
        # reply = message_activities(msg.content)
        # if reply is not None:
        #   await msg.channel.send(reply)


bot.run(BOT_TOKEN)
