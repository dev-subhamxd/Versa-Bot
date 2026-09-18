import os

import discord
from discord.ext import commands

from card import make_card

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
    
@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}!')
    bot.app_emojis = await bot.fetch_application_emojis()

def emoji(name):
    return discord.utils.get(bot.app_emojis, name=name)

@bot.command()
async def avatar(ctx):
    await ctx.send(f"{emoji('godofspaceavatar')}")

@bot.command()
async def card(ctx):
    await ctx.send(f"{ctx.author.display_name}, here's your card!")
    await ctx.send(make_card("Subham", "Developer"))

bot.run(os.environ["APP_TOKEN"])
