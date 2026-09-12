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
async def whoami(ctx):
    author = ctx.author
    await ctx.send(
        f"ID: {author.id}\n"
        f"Name: {author.name}\n"
        f"Display name: {author.display_name}\n"
        f"Mention: {author.mention}\n"
        f"Discriminator/tag: {author.discriminator}\n"
        f"Avatar URL: {author.display_avatar.url}\n"
        f"Joined server: {author.joined_at}\n"
        f"Account created: {author.created_at}\n"
        f"Top role: {author.top_role.name}\n"
        f"All roles: {[r.name for r in author.roles]}"
    )

@bot.command()
async def balance(ctx):
    await ctx.send(f"{ctx.author.name}, you have 0 coins. {emoji('godofspaceavatar')}")

bot.run(os.environ["APP_TOKEN"])
