import os

import discord
from discord.ext import commands

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
    await ctx.send(f"{ctx.author.display_name}, These are the available Avatars! {emoji('godofspaceavatar')}")

@bot.command()
async def hello(ctx):
    await ctx.send("Hello Buddy!")

bot.run(os.environ["APP_TOKEN"])
