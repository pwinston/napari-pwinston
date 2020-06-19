"""create_text_image: create a PIL image with centered text.
"""
from PIL import Image, ImageDraw, ImageFont


def draw_centered_text(image, text):

    font = ImageFont.truetype('Arial Black.ttf', size=244)
    (width, height) = font.getsize(text)
    x = (image.width / 2) - width / 2
    y = (image.height / 2) - height / 2

    color = 'rgb(255, 255, 255)'  # white color

    draw = ImageDraw.Draw(image)
    draw.text((x, y), text, fill=color, font=font)


def create_text_image(text):
    text = str(text)
    SIZE = (1024, 1024)
    image = Image.new('I', SIZE)
    draw_centered_text(image, text)
    return image


def test():
    image = create_text_image("test")
    outfile = "image.png"
    image.save(outfile)
    print(f"Wrote: {outfile}")


if __name__ == '__main__':
    test()
