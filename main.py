import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}!')

@bot.command()
async def balance(ctx):
    await ctx.send(f"{ctx.author.name}, you have 0 coins.")

bot.run(os.environ["APP_TOKEN"])
