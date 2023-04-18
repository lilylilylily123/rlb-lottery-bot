import asyncio
import os
import time
import discord
from pyvirtualdisplay import Display
from discord.ext import tasks
import json
from dotenv import load_dotenv
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
# display = Display(visible=False, size=(800, 600))
# display.start()
load_dotenv()

token = os.getenv("TOKEN")
chrome_options = Options()

chrome_driver_path = "/Users/gerardhernandez/code/rollbit-tracker/chromedriver"
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



async def get_id():
    try:
        with webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options) as driver:
            driver.set_page_load_timeout(20)
            apiUrl = "https://rollbit.com/rlb/lottery/current"
            driver.get(apiUrl)
            WebDriverWait(driver, 10).until(lambda driver: driver.find_element(By.CLASS_NAME, 'css-1jje1nd'))
            content = driver.find_element(By.CLASS_NAME, 'css-1jje1nd').text
            # driver.execute_script("window.scrollTo(0,"+str(content.location['y'])+")")
            res = [int(i) for i in content.split() if i.isdigit()]
            print(res[0])
            if res[0] >= 15:
                await send_stat("Lottery is at ``{0}/100``! Go buy!".format(res[0]))
            else:
                pass
    except Exception as e:
        print(e)
        print("DID NOT WORK.")
        pass


async def total():
    await get_id()
    return


@tasks.loop(minutes=5)
async def loop():
    await total()

chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
bot.run(token)
