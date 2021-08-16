
# Some fancy description is definitely here

# Creation date: 16/08/2021

# Imported Tools.
from os import path
from PIL import Image
from pixelmatch.contrib.PIL import pixelmatch

LOCATION = path.dirname(path.abspath(__file__)) + "\\temp_files\\%s"

# Function: load_image
def load_image(image_name):
    ''' Returns: Loaded image and size. '''
    image_location = LOCATION % (image_name)
    try:
        image = Image.open(image_location)
    except:
        raise ValueError("Image Read Failed")
    return image

# Function: image_compare
def image_compare(image_name_1, image_name_2):
    ''' Returns: Image showing difference between images. '''
    image_1 = load_image(image_name_1)
    image_2 = load_image(image_name_2)
    image_difference = Image.new("RGBA", image_1.size)
    image_result = pixelmatch(image_1, image_2, image_difference, threshold=0.001, includeAA=True)
    image_difference.save(LOCATION % "difference.png")

image_compare("1.png","2.png")