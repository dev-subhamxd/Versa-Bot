from PIL import Image, ImageDraw, ImageFont

def make_card(name, rarity):
    # Create the blank card canvas
    card = Image.new("RGBA", (400, 600), "white")
    draw = ImageDraw.Draw(card)

    # Placeholder "art" box (just a colored rectangle for now,
    # instead of loading a real image file)
    draw.rectangle([20, 20, 380, 380], fill="lightgray", outline="black", width=3)
    draw.text((150, 180), "ART HERE", fill="black")

    # Card border
    draw.rounded_rectangle([10, 10, 390, 590], radius=15, outline="black", width=4)

    # Use a safe default font so this works with no font file needed
    font = ImageFont.load_default()

    draw.text((20, 400), f"Name: {name}", font=font, fill="black")
    draw.text((20, 440), f"Rarity: {rarity}", font=font, fill="black")

    card.save("output_card.png")
    return "output_card.png"
