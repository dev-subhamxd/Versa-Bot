import os

import discord
from discord import ui
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

class ProfileView(ui.LayoutView):
    def __init__(self, member: discord.Member, balance: int):
        super().__init__()

        section = ui.Section(
            ui.TextDisplay(f"## {member.display_name}"),
            ui.TextDisplay(f"**Balance:** {balance} coins"),
            accessory=ui.Thumbnail(media=member.display_avatar.url),
        )

        container = ui.Container(
            section,
            ui.Separator(visible=True),
            ui.ActionRow(
                ui.Button(label="Daily Reward", style=discord.ButtonStyle.primary, custom_id="daily"),
            ),
            accent_color=discord.Color.gold(),
        )
        self.add_item(container)

@bot.command()
async def profile(ctx):
    await ctx.send(view=ProfileView(ctx.author, balance=0))
    
@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}!')
    bot.app_emojis = await bot.fetch_application_emojis()

def emoji(name):
    return discord.utils.get(bot.app_emojis, name=name)

@bot.command()
async def balance(ctx):
    await ctx.send(f"{ctx.author.name}, you have 0 coins. {emoji('godofspaceavatar')}")

bot.run(os.environ["APP_TOKEN"])
