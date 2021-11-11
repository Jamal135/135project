#

# Imported Tools.
from os import path
from PIL import Image
from math import ceil
from itertools import product
from random import seed, sample

LOCATION = path.dirname(path.abspath(__file__)) + "\\temp_files\\%s"


def load_image(image_name):
    ''' Returns: Loaded image and size. '''
    image_location = LOCATION % (image_name)
    image = Image.open(image_location)
    width, height = image.size
    return image, width, height


def shuffle(key, data):
    ''' Returns: Shuffled data. '''
    seed(key)
    return sample(data, len(data))


def gen_coordinates(image, key, width, height, key_pixels):
    ''' Returns: Key derived pixel order. '''
    base_key = key + (abs(width + height) * abs(width - height))
    coords = [*product(range(width), range(height))]
    shuffled_coords = shuffle(base_key, coords)
    key_coords = shuffled_coords[:key_pixels - 1]
    pixels = [image.getpixel((key_coords[point][1], key_coords[point][0]))
              for point in range(key_pixels - 1)]
    pixel_key = sum([int(''.join(map(str, point))) for point in pixels])
    image_key = base_key + pixel_key
    data_coords = shuffle(image_key, shuffled_coords[key_pixels:])
    return data_coords, image_key


def random_sample(key, options, length, number_picked):
    ''' Returns: Variable length list of lists of selected options. '''
    seed(key)
    return [sample(options, k=number_picked) for _ in range(length)]


def gen_colours(key, method, colours, length):
    ''' Returns: List colours for each pixel. '''
    if method == "random":
        return random_sample(key, colours, length, 1)
    elif method == "all":
        return random_sample(key, colours, length, len(colours))


def gen_indexes(key, indexes, length):
    ''' Returns: List indexes for each pixel. '''
    return random_sample(key, indexes, length, len(indexes))


def binary_conversion(data, argument):
    ''' Returns: Input Data Converted to or from Binary. '''
    if argument == "binary":
        byte_array = bytearray(data, "utf-8")
        return "".join([bin(byte)[2:].zfill(8) for byte in byte_array])
    elif argument == "text":
        byte_list = int(data, 2).to_bytes(len(data) // 8, byteorder="big")
        return byte_list.decode('utf-8')


def image_attach(image: str, key: int, data: str, method: str, colour_list: list, index_list: list, key_pixels: int, noise: bool):
    ''' Returns: Image file with data attached.'''
    image_data, width, height = load_image(image)
    positions, image_key = gen_coordinates(
        image, key, width, height, key_pixels)
    length = len(positions)
    colours = gen_colours(image_key + 122, method, colour_list, length)
    indexes = gen_indexes(image_key + 9, index_list, length)
    binary_data = binary_conversion(data, "binary")


def image_extract():
    pass
