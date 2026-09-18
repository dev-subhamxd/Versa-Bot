from PIL import Image, ImageDraw, ImageFont

def make_card(name, rarity, image_path):
    card = Image.new("RGBA", (400, 600), "white")
    draw = ImageDraw.Draw(card)

    art = Image.open(image_path).resize((360, 360))
    card.paste(art, (20, 20))

    font = ImageFont.truetype("arial.ttf", 28)
    draw.text((20, 400), name, font=font, fill="black")
    draw.text((20, 440), rarity, font=font, fill="gold")

    card.save("output_card.png")
    return "output_card.png"
