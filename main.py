from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Message
from discord.ext import commands
import random
import requests
import time
import re

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
VIRUSTOTAL_API_KEY: Final[str] = os.getenv('VIRUSTOTAL_API_KEY')

intents: Intents = Intents.default()
intents.message_content = True
bot: commands.Bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)  # Convert to milliseconds
    await ctx.send(f'Pong! Latency: `{latency}ms`')

@bot.command(help="Change the bot's command prefix.")
@commands.has_permissions(administrator=True)
async def prefix(ctx, new_prefix: str = None):
    if new_prefix is None:
        await ctx.send("Please provide a new prefix.")
        return
    
    global PREFIX
    PREFIX = new_prefix
    bot.command_prefix = new_prefix
    await ctx.send(f"Prefix changed to '{new_prefix}'")

@bot.command(help="Get a random greeting.")
async def hello(ctx):
    greetings = ["Hello!", "Sup G", "Hey!", "Buenas!", "Howdy!"]
    greeting = random.choice(greetings)
    await ctx.send(greeting)

@bot.command(help="Pick a game to play.")
async def jogo(ctx):
    games = ["NFS Heat", "GTA", "Formula 1", "Rocket League", "Fortnite", "Bloons TD6"]
    game = random.choice(games)
    await ctx.send(game)

@bot.event
async def on_message(message):
    # Check if the message author is the bot itself
    if message.author == bot.user:
        return
    
    if "nosso" in message.content.lower():
        await message.channel.send("NOSSO?? https://media1.tenor.com/m/P-brVOL7poAAAAAd/ours-communism.gif")

    # Check for links in the message content
    for word in message.content.split():
        if word.startswith("http://") or word.startswith("https://"):
            # Check if the link is malicious
            if await is_malicious_link(word):
                defanged_url = await defang_link(word)
                await message.delete()
                await message.channel.send(f"Warning: The link '{defanged_url}' may be malicious and has been removed.")
            break  # Stop checking if one link is found

    await bot.process_commands(message)


import time

async def defang_link(link):
    # Replace 'http://' and 'https://' with 'hxxp://' and 'hxxps://'
    defanged_link = re.sub(r'(https?://)', r'hxxps://', link)
    return defanged_link

async def is_malicious_link(link):
    if not VIRUSTOTAL_API_KEY:
        print("VirusTotal API key not found.")
        return False

    defanged_link = await defang_link(link)

    url = f"https://www.virustotal.com/vtapi/v2/url/report"
    params = {"apikey": VIRUSTOTAL_API_KEY, "resource": defanged_link}
    
    try:
        while True:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                json_response = response.json()
                print("VirusTotal API Response:", json_response)
                if json_response.get("response_code") == 1:
                    # If the scan is finished, check if any positives (malware) were detected
                    if json_response.get("positives", 0) > 0:
                        return True
                    else:
                        return False
                elif json_response.get("response_code") == -2:
                    # If the resource is still queued for scanning, wait and retry
                    print("Resource still queued for scanning. Waiting...")
                    time.sleep(10)  # Wait for 10 seconds before retrying
                else:
                    # Handle other response codes if needed
                    print("Unexpected response from VirusTotal API:", json_response)
                    return False
            else:
                print("Error response from VirusTotal API:", response.text)
                return False
    except Exception as e:
        print("Error occurred during VirusTotal API request:", e)
        return False

def main():
    bot.run(TOKEN)

if __name__ == "__main__":
    main()