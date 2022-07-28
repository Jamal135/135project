'''Creation date: __/__/____'''


from os import path
from PIL import Image
from math import ceil
from itertools import product
from secrets import token_hex
from random import seed, sample, randint

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
    key_coords = shuffled_coords[:key_pixels]
    pixels = [image.getpixel((key_coords[point][0], key_coords[point][1]))
              for point in range(key_pixels - 1)]
    pixel_key = sum(int(''.join(map(str, point))) for point in pixels)
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
    ''' Returns: Input data converted to or from binary. '''
    if argument == "binary":
        byte_array = bytearray(data, "utf-8")
        return "".join([bin(byte)[2:].zfill(8) for byte in byte_array])
    elif argument == "text":
        byte_list = int(data, 2).to_bytes(len(data) // 8, byteorder="big")
        return byte_list.decode('utf-8')


def integer_conversion(input_integer, argument):
    ''' Returns: Input number converted to or from binary. '''
    if argument == "binary":
        return bin(input_integer).replace("0b", "")
    elif argument == "integer":
        return int(input_integer, 2)


def gen_header(method, colour_list, index_list, padding_length):
    ''' Returns: Built binary header data specifying settings. '''
    method_bool = "1" if method == "random" else "0"
    colour_table = ["0", "0", "0"]
    for colour in colour_list:
        colour_table[colour] = "1"
    index_table = ["0", "0", "0", "0", "0", "0", "0", "0"]
    for index in index_list:
        index_table[index] = "1"
    padding_bool = integer_conversion(padding_length, "binary").zfill(5)
    return method_bool + "".join(colour_table) + "".join(index_table) + padding_bool


def calculate_pixel_capacity(method, colour_list, index_list):
    ''' Returns: Number of binary bits each pixel will hold. '''
    if method == "all":
        return len(colour_list) * len(index_list)
    elif method == "random":
        return len(index_list)


def gen_numbers(min_value, max_value, number_values):
    """ Returns: Variable length string of random numbers in range. """
    seed(token_hex(64))
    return "".join([str(randint(min_value, max_value)) for _ in range(number_values)])


def gen_message(width, height, data, positions, method, colours, indexes, capacity, noise_setting):
    ''' Returns: Built message to attach to image. '''
    binary_width = len(integer_conversion(width, "binary"))
    binary_height = len(integer_conversion(height, "binary"))
    message_length = binary_width + binary_height + \
        len(data) + 17  # Header Length
    padding_length = 0 if message_length % capacity == 0 else capacity - \
        (message_length % capacity)
    padding = "0" * padding_length
    total_length = message_length + padding_length
    header = gen_header(method, colours, indexes, padding_length)
    noise = ""
    if noise_setting:
        noise = gen_numbers(0, 1, (len(positions) * capacity) - total_length)
    last_pixel = positions[message_length % capacity]
    width = integer_conversion(last_pixel[0], "binary").zfill(binary_width)
    height = integer_conversion(last_pixel[1], "binary").zfill(binary_height)
    return width + height + header + data + padding + noise


def attach_data(image, positions, colours, indexes, capacity, message):
    ''' Returns: Image data with new values attached. '''
    length = ceil(len(message) / capacity)
    pixels = [image.getpixel((positions[point][0], positions[point][1]))
              for point in range(length)]
    position = 0
    for index, pixel in enumerate(pixels):
        pixel_list = list(pixel)
        for colour in colours[index]:
            data = pixel[colour]
            binary_data = list(integer_conversion(data, "binary").zfill(8))
            for bit in indexes[index]:
                binary_data[bit] = message[position]
                position += 1
            new_value = integer_conversion("".join(binary_data), "integer")
            pixel_list[colour] = new_value
        pixels[index] = tuple(pixel_list)
    [image.putpixel((positions[point][0], positions[point][1]), pixels[point])
     for point in range(length)]
    return image


def extract_data(image):
    pass


def image_attach(image: str, key: int, data: str, method: str, colour_list: list, index_list: list, key_pixels: int, noise: bool):
    ''' Returns: Image file with data attached. '''
    image, width, height = load_image(image)
    positions, image_key = gen_coordinates(image, key, width, height, key_pixels)
    length = len(positions)
    colours = gen_colours(image_key + 122, method, colour_list, length)
    indexes = gen_indexes(image_key + 9, index_list, length)
    capacity = calculate_pixel_capacity(method, colour_list, index_list)
    binary_data = binary_conversion(data, "binary")
    message = gen_message(width, height, binary_data, positions,
                          method, colour_list, index_list, capacity, noise)
    steg_image = attach_data(image, positions,
                             colours, indexes, capacity, message)
    steg_image.save(LOCATION % "122Steg.png")


def image_extract(image: str, key: int, key_pixels: int):
    ''' Returns: Data extracted from 122Steg image. '''
    image_data, width, height = load_image(image)
    positions, image_key = gen_coordinates(
        image_data, key, width, height, key_pixels)
    length = len(positions)


# Revisit methods
# Bit of a sus test text... was a joke when it produced a bug I now need to fix... =(
data = "Hey Larry, the drugs will be at the end of Ann St under the door mat, 6pm"
key = 15
index = [6,7]
colour = [0, 1, 2]
image_attach("gate.png", key, data, "random", colour, index, 8, True)


def image_extract():
    pass
