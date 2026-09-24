"""utensils/card.py - profile card renderer for the bot."""
import asyncio
import inspect
import io
import os
import textwrap

import discord
from PIL import Image, ImageDraw, ImageFont, ImageOps

from db import get as db_get  # <-- adjust to match your db.py

# Project layout assumed:
#   assets/backgrounds/<id>.png
#   assets/decorations/<id>.png   (transparent PNG, drawn over the avatar)
#   assets/fonts/<id>.ttf
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")

W, H = 600, 300

# Card templates: every coordinate lives here so new templates are just new entries.
TEMPLATES = {
    "default": {
        "avatar": (25, 25, 125, 125),          # circle bbox
        "deco_scale": 1.3,                      # decoration size relative to avatar
        "side_box": (25, 165, 125, 270),        # empty box, lower left
        "title_pos": (150, 30), "title_size": 18,
        "name_pos": (150, 65), "name_size": 36, "name_max_w": 420,
        "bio_box": (150, 125, 575, 180), "bio_size": 13, "bio_wrap": 48,
        "bottom_box": (150, 195, 575, 270),     # empty box under the bio
    },
}


# ---------------------------------------------------------------- database
async def _get(path):
    """Call db.py's GET (sync or async) and never let a DB error break the card."""
    try:
        result = db_get(path)
        if inspect.isawaitable(result):
            result = await result
        return result or {}
    except Exception:
        return {}


def _owns(inventory, category, item_id):
    """True if item_id is in inventory[category]. Handles dict or list (Firebase can return either)."""
    if not item_id:
        return False
    items = inventory.get(category) if isinstance(inventory, dict) else None
    if isinstance(items, dict):
        return bool(items.get(item_id))
    if isinstance(items, list):
        return item_id in items
    return False


def _asset(category, item_id, ext):
    """Path to an asset file, or None if missing."""
    path = os.path.join(ASSETS, category, os.path.basename(str(item_id)) + ext)
    return path if os.path.isfile(path) else None


async def _resolve_customizations(user_id):
    """Returns only the selections that are selected AND owned AND exist on disk."""
    selected, inventory = await asyncio.gather(
        _get(f"users/{user_id}/card/selected"),
        _get(f"users/{user_id}/inventory"),
    )
    profile = await _get(f"users/{user_id}/card/profile")

    def pick(key, category, ext):
        item_id = selected.get(key)
        if _owns(inventory, category, item_id):
            return _asset(category, item_id, ext)
        return None

    template_id = selected.get("template")
    if template_id not in TEMPLATES or not _owns(inventory, "templates", template_id):
        template_id = "default"

    return {
        "background": pick("background", "backgrounds", ".png"),
        "decoration": pick("decoration", "decorations", ".png"),
        "font": pick("font", "fonts", ".ttf"),
        "template": template_id,
        "title": profile.get("title") or "",
        "bio": profile.get("bio") or "",
    }


# ---------------------------------------------------------------- drawing
def _font(path, size):
    for candidate in (path, "DejaVuSans.ttf", "arial.ttf"):
        if not candidate:
            continue
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _render(avatar_bytes, name, opts):
    t = TEMPLATES[opts["template"]]

    # Background: custom (cover-cropped to 600x300) or plain white
    if opts["background"]:
        bg = Image.open(opts["background"]).convert("RGB")
        img = ImageOps.fit(bg, (W, H), Image.LANCZOS)
    else:
        img = Image.new("RGB", (W, H), "white")
    draw = ImageDraw.Draw(img)

    # Avatar in circle (4x mask for smooth edges); falls back to black circle
    x0, y0, x1, y1 = t["avatar"]
    size = x1 - x0
    if avatar_bytes:
        avatar = Image.open(io.BytesIO(avatar_bytes)).convert("RGB").resize((size, size), Image.LANCZOS)
        mask = Image.new("L", (size * 4, size * 4), 0)
        ImageDraw.Draw(mask).ellipse((0, 0, size * 4 - 1, size * 4 - 1), fill=255)
        mask = mask.resize((size, size), Image.LANCZOS)
        img.paste(avatar, (x0, y0), mask)
    else:
        draw.ellipse(t["avatar"], fill="black")

    # Avatar decoration (transparent PNG centered on the avatar)
    if opts["decoration"]:
        deco_size = int(size * t["deco_scale"])
        deco = Image.open(opts["decoration"]).convert("RGBA").resize((deco_size, deco_size), Image.LANCZOS)
        cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
        img.paste(deco, (cx - deco_size // 2, cy - deco_size // 2), deco)

    # Empty boxes
    draw.rounded_rectangle(t["side_box"], radius=12, outline="black", width=2)
    draw.rounded_rectangle(t["bottom_box"], radius=12, outline="black", width=2)

    # Title (small line above the name)
    if opts["title"]:
        draw.text(t["title_pos"], opts["title"], font=_font(opts["font"], t["title_size"]), fill="black")

    # Name (shrinks until it fits)
    name_size = t["name_size"]
    name_font = _font(opts["font"], name_size)
    while name_size > 12 and draw.textlength(name, font=name_font) > t["name_max_w"]:
        name_size -= 2
        name_font = _font(opts["font"], name_size)
    draw.text(t["name_pos"], name, font=name_font, fill="black")

    # Bio box (yellow)
    bx0, by0, _bx1, by1 = t["bio_box"]
    draw.rounded_rectangle(t["bio_box"], radius=12, fill="#FFF0C2", outline="black", width=1)
    lines = textwrap.wrap(opts["bio"], width=t["bio_wrap"])[:3]
    bio_font = _font(opts["font"], t["bio_size"])
    line_h = t["bio_size"] + 5
    y = by0 + (by1 - by0 - line_h * len(lines)) // 2
    for line in lines:
        draw.text((bx0 + 12, y), line, font=bio_font, fill="black")
        y += line_h

    buf = io.BytesIO()
    img.save(buf, "PNG")
    buf.seek(0)
    return buf


# ---------------------------------------------------------------- public API
async def card_display(author):
    """Build the profile card for a discord.Member/User. Returns a discord.File.

    Usage:  await ctx.send(file=await card_display(ctx.author))
    """
    try:
        avatar_bytes = await author.display_avatar.replace(size=256, format="png").read()
    except discord.DiscordException:
        avatar_bytes = None

    opts = await _resolve_customizations(author.id)

    # Pillow is blocking, so render off the event loop to keep the bot responsive
    loop = asyncio.get_running_loop()
    buf = await loop.run_in_executor(None, _render, avatar_bytes, author.display_name, opts)
    return discord.File(buf, filename="profile_card.png")


async def premium_card_display(author, template_id):
    # TODO: later
    raise NotImplementedError
