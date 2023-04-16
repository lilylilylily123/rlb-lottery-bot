import asyncio
import os
import time
import discord
from discord.ext import tasks
import json
from dotenv import load_dotenv
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

load_dotenv()
chrome_driver_path = "/Users/gerardhernandez/code/rollbit-tracker/chromedriver"

token = os.getenv("TOKEN")
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
bot = discord.Bot()
channelid = []

@bot.event
async def on_ready():
    print("Bot is ready")
    loop.start()


@bot.event
async def on_guild_join(guild):
    print("Joined a guild: {0}".format(guild.id))
    await guild.text_channels[0].send("Joined a guild: {0}".format(guild.id))
    return guild


def helperfunc(channel_id):
    global channelid
    channelid.append(channel_id)
@bot.slash_command(name="setup")
async def setup(ctx):
    await ctx.defer()
    message = await ctx.followup.send("Setting up alerts for this channel...")
    await asyncio.sleep(2)
    await message.edit(content="Done!")
    await asyncio.sleep(2)
    helperfunc(ctx.channel.id)


async def send_stat(stats):
    if not channelid:
        print("No channel set up")
        return
    for i in channelid:
        channel = bot.get_channel(i)
        await channel.send(stats)
        print("Sent stats to {0}".format(i))


chrome_options.add_argument("--headless")

async def get_id():
    apiUrl = "https://rollbit.com/rlb/lottery/current"
    driver.get(apiUrl)
    WebDriverWait(driver, 10).until(lambda driver: driver.find_element(By.CLASS_NAME, 'css-1jje1nd'))
    content = driver.find_element(By.CLASS_NAME, 'css-1jje1nd').text
    res = [int(i) for i in content.split() if i.isdigit()]
    print(res[0])
    if res[0] >= 15:
        await send_stat("Lottery is at ``{0}/100``! Go buy!".format(res[0]))
    else:
        pass


async def total():
    await get_id()
    return


@tasks.loop(minutes=5)
async def loop():
    await total()


driver = webdriver.Chrome(options=chrome_options)
bot.run(token)
