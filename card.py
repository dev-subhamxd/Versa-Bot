"""utensils/card.py - profile card renderer."""
import io
import textwrap

import discord
from PIL import Image, ImageDraw, ImageFont

W, H = 600, 300


def _font(size, bold=False):
    names = ["DejaVuSans-Bold.ttf", "arialbd.ttf"] if bold else ["DejaVuSans.ttf", "arial.ttf"]
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def card_display(display_name, about_me):
    """Render the profile card and return it as a discord.File.

    Usage: await ctx.send(file=card_display(ctx.author.display_name, about_me))
    """
    display_name = str(display_name or "Unknown")
    about_me = str(about_me or "")

    img = Image.new("RGB", (W, H), "white")
    draw = ImageDraw.Draw(img)

    # Black circle (top left)
    draw.ellipse((25, 25, 125, 125), fill="black")

    # Empty box (lower left)
    draw.rounded_rectangle((25, 165, 125, 270), radius=12, outline="black", width=2)

    # Company line + name
    draw.text((150, 30), "Versa Pvt. LTD.", font=_font(18), fill="black")
    draw.text((150, 65), display_name, font=_font(36, bold=True), fill="black")

    # Yellow box with about me
    box = (150, 125, 575, 180)
    draw.rounded_rectangle(box, radius=12, fill="#FFF0C2", outline="black", width=1)
    lines = textwrap.wrap(about_me, width=48)[:3]
    line_h = 18
    y = box[1] + (box[3] - box[1] - line_h * len(lines)) // 2
    for line in lines:
        draw.text((box[0] + 12, y), line, font=_font(13), fill="black")
        y += line_h

    # Empty box under it
    draw.rounded_rectangle((150, 195, 575, 270), radius=12, outline="black", width=2)

    buf = io.BytesIO()
    img.save(buf, "PNG")
    buf.seek(0)
    return discord.File(buf, filename="profile_card.png")
