#!/usr/bin/env python3

import discord
import os
import platform
import pathlib
import random
from discord.ext import commands

TOKEN = os.getenv("TOKEN")
PREFIX = "!"

bot = commands.Bot(command_prefix=PREFIX, case_insensitive=True, help_command=None)

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
    greetings = ["Hello!", "Hi there!", "Hey!", "Greetings!", "Hola!"]
    greeting = random.choice(greetings)
    await ctx.send(greeting)

@bot.event
async def on_ready():
    print(f"{bot.user.name} is ready!")
    print(f"Discord.py version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")

def main():
    bot.run(TOKEN)

if __name__ == "__main__":
    main()
