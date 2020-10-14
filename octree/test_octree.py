import numpy as np
from napari.layers.image.experimental.octree import Octree

from PIL import Image, ImageDraw, ImageFont


def draw_text(image, text, nx=0.5, ny=0.5):

    font = ImageFont.truetype('Arial Black.ttf', size=72)
    (text_width, text_height) = font.getsize(text)
    x = nx * image.width - text_width / 2
    y = ny * image.height - text_height / 2

    color = 'rgb(255, 255, 255)'  # white

    draw = ImageDraw.Draw(image)
    draw.text((x, y), text, fill=color, font=font)
    draw.rectangle([0, 0, image.width, image.height], width=5)


def create_text_array(text, nx=0.5, ny=0.5) -> np.ndarray:
    text = str(text)
    SIZE = (1024, 1024)
    image = Image.new('RGB', SIZE)
    draw_text(image, text, nx, ny)
    return np.array(image)


def test():
    image = create_text_array("Hello")
    tree = Octree.from_image(image)


if __name__ == "__main__":
    test()
