import discord
import requests
import io
import random
import aiohttp
import datetime
import os
from os import environ

BOT_TOKEN = environ['DISCORD_DOT_TOKEN']
nsfw_filter = True
meme_api = "https://meme-api.herokuapp.com/gimme"
greet_words = ("Bonjour","Hola","Zdravstvuyte","Nǐn hǎo","Ciao","Yassou","Selamat siang","नमस्ते","Merhaba","नमो नमः")
greet_identifiers = ("👋","hello","hi","hey","namaste","🙏","hallo","halo")
bot = discord.Client()

def getEmbed(title,description,color,authorName,thumbNail):
    #https://discordpy.readthedocs.io/en/latest/api.html#embed
    #send embedded msg by channel.send(embed=embeddedMsg)
    return discord.Embed(title=title, description=description, color=color, author=authorName, thumbnail=thumbNail)

# bot.py
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

client.run(TOKEN)
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
  try:
    await msg.channel.send(file=discord.File(data, 'meme.png'))
  except:
    print("Error in sending meme")

async def greet(msg):
  await msg.channel.send(random.choice(greet_words)+" :wave:")

async def clear(msg):
  embed_msg = None
  message = msg.content.split(' ')
  if len(message) == 1:
      message.append(1)

  elif message[1].isnumeric():
    if int(message[1]) > 30:
      embed_msg = discord.Embed(title="⛔ Can not purge more than 30 messages at once :rolling_eyes:",color=0x8f0a0a)

    else:
      await msg.channel.purge(limit= int(message[1])+1)
      embed_msg = discord.Embed(title=f":white_check_mark: Removed {message[1]} messages",color=0xdede21)

  else:
    embed_msg = discord.Embed(title="⛔ Invalid argument for clear command :confused:",color=0x8f0a0a)

  embed_msg.set_author(name=msg.author)
  embed_msg.timestamp = datetime.datetime.utcnow()
  embed_msg.set_footer(text='🕦 \u200b')
  await msg.channel.send(embed= embed_msg)

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

# Creating a Discord Connection
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)
