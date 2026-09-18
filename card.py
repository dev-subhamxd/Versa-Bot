from PIL import Image, ImageDraw, ImageFont

def make_card(name, rarity):
    card = Image.new("RGBA", (600, 250), "white")
    draw = ImageDraw.Draw(card)

    draw.rectangle([20, 20, 180, 180], fill="lightgray", outline="black", width=3)
    draw.text((30, 30), "ART HERE", fill="black")

    draw.rounded_rectangle([10, 10, 190, 90], radius=15, outline="black", width=4)

    font = ImageFont.load_default()

    draw.text((20, 200), f"Name: {name}", font=font, fill="black")
    draw.text((20, 240), f"Rarity: {rarity}", font=font, fill="black")

    card.save("output_card.png")
    return "output_card.png"
