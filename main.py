import discord
import requests
import io
import random
import aiohttp
import datetime
import os
from PIL import Image

BOT_TOKEN = os.environ['DISCORD_DOT_TOKEN']
nsfw_filter = True
meme_api = "https://meme-api.herokuapp.com/gimme"
greet_words = ("Bonjour","Hola","Zdravstvuyte","Nǐn hǎo","Ciao","Yassou","Selamat siang","नमस्ते","Merhaba","नमो नमः")
greet_identifiers = ("👋","hello","hi","hey","namaste","🙏","hallo","halo")
bot = discord.Client()

def getEmbed(title,description=None,color=0x3eccd6,authorName=None,thumbNail=None):
    #https://discordpy.readthedocs.io/en/latest/api.html#embed
    #send embedded msg by channel.send(embed=embeddedMsg)
    if description:
      return discord.Embed(title=title, description=description, color=color, author=authorName, thumbnail=thumbNail)
    else:
      return discord.Embed(title=title, color=color, author=authorName, thumbnail=thumbNail)

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

async def image_magic(msg):
  if msg.attachments:
        attachment_link = msg.attachments[0].url
        async with aiohttp.ClientSession() as session:
          async with session.get(attachment_link) as resp:
            if resp.status != 200:
                print('Could not download file...')
                return
            data = io.BytesIO(await resp.read())

        img = Image.open(data)
        img_format = img.format #(img format gets removed after manipulation with PIL)
        img = img.rotate(90,expand=True)
        imgByteArr = io.BytesIO()
        img.save(imgByteArr,format=img_format)
        byte_data = io.BytesIO(imgByteArr.getvalue())

        try:
          pass
          await msg.channel.send(file=discord.File(byte_data,'dot_resp.'+img_format))
        except Exception as e:
          print("Error in sending img")
          print(e)

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
    if(msg.author == bot.user):
      return
    
    if (msg.content.startswith(".")):
      if(msg.content == ".meme"):
        await meme(msg)
      elif msg.content.lower() in ['.hi','.hello']:
        await greet(msg)
      
      elif msg.content.split(' ')[0] == ".clear":
        await clear(msg)
      
      elif msg.content.lower().startswith(".rotate"):
        deg_value =  msg.content.lower().replace('.rotate ','')
        if (not deg_value.isdigit()) or int(deg_value) >360 or int(deg_value) < 0:
          await msg.channel.send("Invalid use of .rotate :x:",)
          #todo converting param to digits and passing to image_magic, make  default param = 90
          return
        message = await msg.channel.fetch_message(msg.reference.message_id)
        if message.attachments:
          await image_magic(message)
        else:
          await msg.channel.send("_I rotate images only_ :camera_with_flash:")

    elif msg.content.lower().startswith(greet_identifiers):
      await greet(msg)
  
bot.run(BOT_TOKEN)
'''
# Todo: Use this code for making connection

# Creating a Discord Connection
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)
'''
