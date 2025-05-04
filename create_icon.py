from PIL import Image, ImageDraw, ImageFont
import os

# Create a 256x256 image with a white background
icon_size = 256
img = Image.new("RGBA", (icon_size, icon_size), color=(255, 255, 255, 0))
draw = ImageDraw.Draw(img)

# Draw a card outline
card_width = 180
card_height = 220
card_left = (icon_size - card_width) // 2
card_top = (icon_size - card_height) // 2

# Card background
draw.rectangle(
    [(card_left, card_top), (card_left + card_width, card_top + card_height)],
    fill=(255, 255, 255, 255),
    outline=(0, 0, 0, 255),
    width=4,
)

# Draw some card details (lines)
line_padding = 20
for i in range(1, 5):
    y_pos = card_top + (i * line_padding) + 40
    draw.line(
        [(card_left + 20, y_pos), (card_left + card_width - 20, y_pos)],
        fill=(100, 100, 100, 180),
        width=2,
    )

# Draw a simple colorful pattern in the card top area
draw.rectangle(
    [(card_left + 10, card_top + 10), (card_left + card_width - 10, card_top + 35)],
    fill=(70, 130, 180, 255),  # Steel Blue
    outline=None,
)

# Save as ICO file for Windows
if not os.path.exists("assets"):
    os.makedirs("assets")

img.save(
    "assets/card_icon.ico",
    format="ICO",
    sizes=[(32, 32), (64, 64), (128, 128), (256, 256)],
)
print("Icon created successfully at assets/card_icon.ico")
