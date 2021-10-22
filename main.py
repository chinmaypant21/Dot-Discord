import discord
import requests
import json
import io
import random
import aiohttp
import asyncio

from os import environ

BOT_TOKEN = environ['DISCORD_DOT_TOKEN']
nsfw_filter = True
meme_api = "https://meme-api.herokuapp.com/gimme"
greet_words = ("Bonjour","Hola","Zdravstvuyte","Nǐn hǎo","Ciao","Yassou","Selamat siang","नमस्ते","Merhaba","नमो नमः")
greet_identifiers = ("👋","hello","hi","hey","namaste","🙏","hallo","halo")
bot = discord.Client()

def getEmbed(title,description,color):
    #find all properties of discord.Embed at:
    #https://discordpy.readthedocs.io/en/latest/api.html#embed
    #send embedded msg by channel.send(embed=embeddedMsg)
    return discord.Embed(title=title,description=description,color=color)
  
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
  await msg.channel.send(random.choice(greet_words)+" :wave:")

async def clear(msg):
  message = msg.content.split(' ')
  if len(message) == 1:
    await msg.channel.purge(limit=2)
    print(f"cleared 1 message from {msg.channel}")
  elif message[1].isnumeric():
    if int(message[1]) > 30:
      await msg.channel.send("[-] Can not purge more than 30 messages at once :rolling_eyes:")
      return
    await msg.channel.purge(limit= int(message[1])+1)
    await msg.channel.send(f"[+] Removed {message[1]} messages")

  else:
    await msg.channel.send("[-] Invalid argument for clear command :confused: ")


@bot.event
async def on_message(msg):
    # If message is the one which is sent by this bot
    if (msg.author != bot.user and msg.content.startswith(".")):
      if(msg.content == ".meme"):
        await meme(msg)
      elif msg.content.lower() in ['.hi','.hello']:
        await greet(msg)
      
      elif msg.content.split(' ')[0] == ".clear":
        await clear(msg)
      else:
        pass

    elif msg.author != bot.user and msg.content.lower().startswith(greet_identifiers):
      await greet(msg)
  
bot.run(BOT_TOKEN)
