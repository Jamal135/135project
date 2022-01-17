'''Creation date: 16/08/2021'''

from os import path
from PIL import Image, ImageColor
from pixelmatch.contrib.PIL import pixelmatch

LOCATION = path.dirname(path.abspath(__file__)) + "\\temp_files\\%s"


def load_image(image_name):
    ''' Returns: Loaded image and size. '''
    image_location = LOCATION % (image_name)
    try:
        return Image.open(image_location)
    except:
        raise ValueError("Image Read Failed")


def image_compare(image_name_1, image_name_2, alpha:int = 0.1, colour: str = "#FF0000"):
    ''' Returns: Image showing difference between images. '''
    image_1 = load_image(image_name_1)
    image_2 = load_image(image_name_2)
    rgb_colour = ImageColor.getcolor(colour, "RGB")
    image_difference = Image.new("RGBA", image_1.size)
    _ = pixelmatch(image_1, image_2, image_difference,
                   threshold=0.001, includeAA=True, alpha=alpha, diff_color=rgb_colour)
    image_difference.save(LOCATION % "difference.png")

image_compare("1.png", "2.png", 0, "#FF0000")
