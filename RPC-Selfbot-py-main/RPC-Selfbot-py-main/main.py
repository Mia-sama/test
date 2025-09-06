import os
import time
import asyncio
import datetime

import discord
from discord.ext import commands
import yaml

with open("config.yml","r") as file:
  config = yaml.full_load(file.read())


from ext.imgid import get_img_id
if config["replit"]:
  from ext.bot_stat import keep_on
  keep_on()
  token = os.environ.get("TOKEN")
else:
  token = config["token"]


# Initialization
appid = config["application_id"]
imgdic = None
starttime = None
partyd = None
timed = None


bot = commands.Bot(command_prefix='xxXx')
bot.remove_command("help")


try:
  if config["images"]["enable_images"] in [True,"true","True"]:  
    imgdic = dict([
      ("large_image", get_img_id(appid,config["images"]["large_image_key"])), 
      ("large_text", config["images"]["large_image_text"]),
      ("small_image", get_img_id(appid,config["images"]["small_image_key"])),
      ("small_text", config["images"]["small_image_text"])
     ]) 

except TypeError:
  print("\n")
  raise TypeError("Application ID needed to use art assets / images.")

if config["elapsed_time"]["enable_elapsed_time"]:
  if config["elapsed_time"]["mode"].lower() == "normal":
    starttime = int(time.time())*1000
    timed = dict([("start",starttime),("end",None)])

  elif config["elapsed_time"]["mode"].lower() == "custom_start":
    if isinstance(config["elapsed_time"]["start_time"],int):
      starttime = config["elapsed_time"]["start_time"]*1000

    elif isinstance(config["elapsed_time"]["start_time"],datetime.datetime):
      starttime = config["elapsed_time"]["start_time"].timestamp()

    timed = dict([("start",starttime),("end",None)])
    
  elif config["elapsed_time"]["mode"] == "countdown":
    endtime = int(config["elapsed_time"]["end_time"])*1000
    timed = dict([("start",None),("end",endtime)])


async def update_mc():
      act = discord.Activity(
          application_id=appid,
          name=config["game"],
          type = discord.ActivityType.playing,
          state= config["state"],
          details=config["details"],
          assets=imgdic,
          timestamps=timed
        )
  
      await bot.change_presence (activity=act)
      await asyncio.sleep(15)
  

@bot.event
async def on_ready():
    print("—————————————————————————")
    print("RPC Selfbot ready!")
    
    act = discord.Activity(
      application_id=appid,
      name=config["game"],
      type = discord.ActivityType.playing,
      state=config["state"],
      details=config["details"],
      assets=imgdic,
      party=partyd,
      timestamps=timed
    )
  
    await bot.change_presence(activity=act)
    bot.loop.create_task(update_mc())

  
@bot.event
async def on_disconnect():
  print("Rich Presence Stopped")
bot.run(token,bot = False)