import os

import discord
from discord.ext import commands

from card import card_display

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
async def profile(ctx):
    await ctx.send(file=card_display(ctx.author.display_name, about_me))
    
bot.run(os.environ["APP_TOKEN"])
