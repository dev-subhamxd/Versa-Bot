import os
import time

import discord
from discord.ext import commands

from card import card_display
from database import _get, register_user

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
    about_me = "Living life of a million Souls, in the chaos of Humanity......"
    avatar_bytes = await ctx.author.display_avatar.replace(size=256, format="png").read()
    await ctx.send(file=card_display(ctx.author.display_name, about_me, avatar_bytes))

@bot.command()
async def search(ctx):
    await ctx.send(f"Hello {ctx.author.mention}")
    path = f"users/{ctx.author.id}"
    data = await _get(path)
    await ctx.send(str(data))

@bot.command()
async def register(ctx):
    await ctx.send("Checking User's Database.....")
    path = f"users/{ctx.author.id}"

    if await _get(path) is not None:
        await ctx.send("User Data already exists!")
        return

    await ctx.send("Registering User in the Database......")
    result = await register_user(ctx.author.id)
    await ctx.send(result)

# --------------------- Miscellaneous ---------------------

@bot.command()
async def ping(ctx):
    start = time.perf_counter()
    msg = await ctx.send("Pinging...")
    api_latency = (time.perf_counter() - start) * 1000

    db_start = time.perf_counter()
    await _get("pingcheck")
    db_latency = (time.perf_counter() - db_start) * 1000

    await msg.edit(content=(
        f"🏓 Pong!\n"
        f"Gateway: `{bot.latency * 1000:.2f}ms`\n"
        f"API: `{api_latency:.2f}ms`\n"
        f"Firebase: `{db_latency:.2f}ms`"
    ))
    
bot.run(os.environ["APP_TOKEN"])
