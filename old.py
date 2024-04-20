#!/usr/bin/env python3

import discord
import os
import platform
import random
import requests
from discord.ext import commands

TOKEN = "MTIzMDg3NDU4OTc2MDg1MjA4OQ.GgR3Mr.6ow8aeF50q-6vD1WG6jWLUbfvwYemNFDKxx1b8"
VIRUSTOTAL_API_KEY = "0292d14cc7e9aa41c44ffe2a464282c9f976843979060eaf68bc6169055086a3"
PREFIX = "!"

intents = discord.Intents.default()
intents.messages = True  # Enable message content intents

bot = commands.Bot(command_prefix=PREFIX, case_insensitive=True, help_command=None, intents=intents)

@bot.command(help="Test the bot's latency to the server.")
async def ping(ctx):
    latency = round(bot.latency * 1000)  # Convert to milliseconds
    await ctx.send(f"Pong! Latency: {latency}ms")

@bot.command(help="Change the bot's command prefix.")
@commands.has_permissions(administrator=True)
async def prefix(ctx, new_prefix):
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
    if "nosso" in message.content.lower():
        await message.channel.send("☭")

    # Check for links in the message content
    for word in message.content.split():
        if word.startswith("http://") or word.startswith("https://"):
            # Check if the link is malicious
            if await is_malicious_link(word):
                await message.delete()
                await message.channel.send(f"Warning: The link '{word}' may be malicious and has been removed.")
            break  # Stop checking if one link is found

    await bot.process_commands(message)

async def is_malicious_link(link):
    if not VIRUSTOTAL_API_KEY:
        print("VirusTotal API key not found.")
        return False

    url = f"https://www.virustotal.com/vtapi/v2/url/scan"
    params = {"apikey": VIRUSTOTAL_API_KEY, "url": link}
    response = requests.post(url, data=params)

    if response.status_code == 200:
        json_response = response.json()
        if "positives" in json_response:
            # If VirusTotal detects any positives (malware), consider the link malicious
            if json_response["positives"] > 0:
                return True

    return False

@bot.event
async def on_ready():
    print(f"{bot.user.name} is ready!")
    print(f"Discord.py version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")

def main():
    bot.run(TOKEN)

if __name__ == "__main__":
    main()
