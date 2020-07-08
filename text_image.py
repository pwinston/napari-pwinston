"""create_text_image: create a PIL image with centered text.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont


def draw_text(image, text, nx=0.5, ny=0.5):

    font = ImageFont.truetype('Arial Black.ttf', size=244)
    (text_width, text_height) = font.getsize(text)
    x = nx * image.width - text_width / 2
    y = ny * image.height - text_height / 2

    color = 'rgb(255, 255, 255)'  # white

    draw = ImageDraw.Draw(image)
    draw.text((x, y), text, fill=color, font=font)


def create_text_array(text, nx=0.5, ny=0.5):
    text = str(text)
    SIZE = (1024, 1024)
    image = Image.new('I', SIZE)
    draw_text(image, text, nx, ny)
    return np.array(image)


def test():
    image = create_text_image("test")
    outfile = "image.png"
    image.save(outfile)
    print(f"Wrote: {outfile}")


if __name__ == '__main__':
    test()
