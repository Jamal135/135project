
# Some fancy description is definitely here

# Creation date: 25/05/2021

# Imported Tools.
from os import path
from PIL import Image
from math import ceil
from itertools import product
from random import seed, sample, randint

LOCATION = path.dirname(path.abspath(__file__)) + "\\temp_files\\%s"

# Function: load_image
def load_image(image_name):
    ''' Returns: Loaded image and size. '''
    image_location = LOCATION % (image_name)
    try:
        image = Image.open(image_location)
    except:
        raise ValueError("Image Read Failed.")
    width, height = image.size
    return image, width, height

# Function: gen_key
def gen_key(input_key, image, width, height, key_pixels):
    ''' Returns: Unique key from image and input key, and shuffled position lists. '''
    initial_key = input_key + (abs(height + width) * abs(width - height))
    full_positions = image_coordinates(initial_key, None, height, width)
    key_positions = full_positions[:(key_pixels - 1)]
    try:
        pixel_tuples = [image.getpixel(
            (key_positions[point][1], key_positions[point][0])) for point in range(key_pixels - 1)]
    except:
        raise ValueError ("Failed to Grab Key Pixel Values.")
    pixel_integer = sum([int(''.join(map(str, idx))) for idx in pixel_tuples])
    key = initial_key + pixel_integer
    data_positions = image_coordinates(key, full_positions[key_pixels:])
    return key, data_positions

# Function: gen_numbers
def gen_numbers(key, min_value, max_value, number_values: int = 1):
    """ Returns: Variable Length List of Random Numbers in Defined Range. """
    seed(key)
    if number_values == 1:
        return randint(min_value, max_value)
    else:
        return [randint(min_value, max_value) for _ in range(number_values)]

# Function: gen_colours
def gen_colours(key, positions, colour_selection):
    ''' Returns: Correct list of RGB positions based on argument. '''
    if colour_selection == "random":
        return gen_numbers(key, 0, 2, len(positions))
    else:
        colours = {"red": 0, "green": 1, "blue": 2, }
        return [colours[colour_selection]] * len(positions)

# Function: image_coordinates
def image_coordinates(key, coordinates, height=None, width=None):
    ''' Returns: Shuffled list of image coordinate tuples. '''
    seed(key)
    if coordinates is None:
        coordinates = [*product(range(height), range(width))]
    return sample(coordinates, len(coordinates))

# Function: binary_conversion
# Argument Binary  :  Convert Input data into Binary String.
# Argument Text    :  Convert Input Binary String into Data.
def binary_conversion(input_string, argument):
    ''' Returns: Input Data Converted to/from Binary. '''
    if argument == "binary":
        byte_array = bytearray(input_string, "utf-8")
        return "".join([bin(byte)[2:].zfill(8) for byte in byte_array])
    else:
        byte_list = int(input_string, 2).to_bytes(
            len(input_string) // 8, byteorder="big")
        return byte_list.decode('utf-8')

# Function: integer_conversion
# Argument Binary  :  Decimal Integer to Binary String Representation.
# Argument Decimal :  Binary String Representation to Decimal Integer.
def integer_conversion(input_integer, argument):
    ''' Returns: Input Number Converted to/from Binary. '''
    if argument == "binary":
        return bin(input_integer).replace("0b", "")
    else:
        return int(input_integer, 2)

# Function: key_conversion
def key_conversion(width, height):
    ''' Returns: Integer Describing Length of End Point Key parts. '''
    width_length = len(integer_conversion(width, "binary"))
    height_length = len(integer_conversion(height, "binary"))
    return width_length, height_length

# Function: length_calculator
def length_calculator(width, height, data):
    ''' Returns: Length Calculations of Data Components. '''
    width_length, height_length = key_conversion(width, height)
    data_length = len(data)
    total_length = width_length + height_length + data_length
    print(f"stupid {total_length}")
    return total_length, width_length, height_length

# Function: capacity_check
def capacity_check(data_length, number_points):
    ''' Returns: Pixel Usage Percentage and Breaks if Data is to Long. '''
    remaining_space = number_points - data_length
    if remaining_space < 0:
        raise ValueError(
            f"Input data length {data_length} exceeds image capacity length {number_points}.")
    return round((100/number_points) * data_length, 2)

# Function: end_point
def end_point(positions, total_length, width_length, height_length):
    ''' Returns: Calculated Binary Data End Location Keys. '''
    end_position = positions[total_length]
    print(f"Work {end_position}, {total_length}")
    width_key = integer_conversion(
        end_position[0], "binary").zfill(width_length)
    height_key = integer_conversion(
        end_position[1], "binary").zfill(height_length)
    return width_key, height_key

# Function: message_generator
def message_generator(key, data, width, height, positions, noise, key_pixels):
    ''' Returns: Correctly Built Binary Data to Attach to Image. '''
    total_length, width_length, height_length = length_calculator(
        width, height, data)
    pixel_utilisation = capacity_check(
        total_length, len(positions) + key_pixels)
    width_key, height_key = end_point(
        positions, total_length, width_length, height_length)
    print(width_key + height_key)
    message_data = width_key + height_key + data
    print(f"Message data: {message_data}")
    if noise:
        remaining_space = ((width * height) - 9) - len(message_data)
        noise_list = gen_numbers(key, 0, 1, remaining_space)
        noise_string = "".join(map(str, noise_list))
        built_data = message_data + noise_string
    else:
        built_data = message_data
    length = len(built_data)
    return built_data, length, pixel_utilisation

# Function: extract_values
def extract_values(image, length, positions, rgb_order, index_list):
    ''' Returns: Existing Binary Data to be Replaced. '''
    locations = [image.getpixel(
        (positions[point][1], positions[point][0])) for point in range(length)]
    exact_points = [locations[point][rgb_order[point]]
                    for point in range(length)]
    binary_values = [integer_conversion(
        exact_points[point], "binary").zfill(8) for point in range(length)]
    extracted_values = ""
    index_count = len(index_list)
    index_length = int(ceil(length/index_count))
    for point in range(index_length):
        index_values = []
        for index in range(index_count):
            index_values.append(binary_values[point][index_list[index]])
        extracted_values = extracted_values + "".join(index_values)
    return extracted_values

# Function: data_comparison
def data_comparison(current_values, new_values, length, key_pixels):
    ''' Returns: Percentage Measure of how close two Binary Strings Match. '''
    matches = sum([1 for point in range(length)
                  if current_values[point] == new_values[point]])
    return round((100/length) * (matches + key_pixels), 2)

# Function: data_rebuild
def data_rebuild(locations, new_values, rgb_order, length):
    ''' Returns: Modified List of Tuples given New Values. '''
    input_list = [list(element) for element in locations]
    for point in range(length):
        input_list[point][rgb_order[point]] = new_values[point]
    return [tuple(element) for element in input_list]

# Function: attach_data
def attach_data(image, length, positions, rgb_order, image_message, index_list):
    ''' Returns: New Image Data with RGB colours Correctly Modified with Data. '''
    locations = [image.getpixel(
        (positions[point][1], positions[point][0])) for point in range(length)]
    exact_points = [locations[point][rgb_order[point]]
                    for point in range(length)]
    binary_values = [list(integer_conversion(
        exact_points[point], "binary").zfill(8)) for point in range(length)]
    index_count = len(index_list)
    index_length = int(ceil(length/index_count))
    for point in range(index_length):
        for index in range(index_count):
            binary_values[point][index_list[index]] = image_message[(point * index_count) + index]
    new_binary_values = ["".join(binary_values[point])
                         for point in range(length)]
    new_values = [integer_conversion(
        new_binary_values[point], "decimal") for point in range(length)]
    new_data = data_rebuild(locations, new_values, rgb_order, length)
    try:
        [image.putpixel((positions[point][1], positions[point][0]),
                        new_data[point]) for point in range(length)]
    except:
        raise ValueError("Image Modification Failed.")
    return image

# Function: extract_key
def extract_key(image, positions, rgb_order, width_length, height_length, index_list):
    ''' Returns: Extracted Data End Point. '''
    key_length = width_length + height_length
    key_data = extract_values(image, key_length, positions, rgb_order, index_list)
    width_key = integer_conversion(key_data[:width_length], "decimal")
    height_key = integer_conversion(key_data[width_length:], "decimal")
    end_position = (width_key, height_key)
    return end_position, key_length

# Function: data_extract
def data_extract(image, positions, rgb_order, end_position, key_length, index_list):
    ''' Returns: Extracted binary data from provided image. '''
    index_count = len(index_list)
    index_length = int(ceil(key_length/index_count))
    modified_positions = positions[index_length:]
    modified_rgb_order = rgb_order[index_length:]
    length = positions.index(end_position) - key_length
    return extract_values(image, length, modified_positions, modified_rgb_order, index_list)

# Function: API_image_append
# key: Shuffles Order of Image Locations.
def API_image_append(image_name, input_data, colour_selection: str = "random", input_key: int = 999, index_list: int = 7, noise: bool = False, key_pixels: int = 9):
    ''' Returns: Data Appended to Image if Possible. '''
    # Load the appropriate image file for processing.
    image, width, height = load_image(image_name)
    # Create a unique key and position set from image and input key.
    key, positions = gen_key(input_key, image, width, height, key_pixels)
    # Generate list of which RGB value to modify at each pixel.
    rgb_order = gen_colours(key, positions, colour_selection)
    # Generate the binary data to attach to the provided image.
    binary_indata = binary_conversion(input_data, "binary")
    # Compile the complete message to be attached to the image.
    image_message, length, usage = message_generator(
        key, binary_indata, width, height, positions, noise, key_pixels)
    # Extract the existing values from the image that will be replaced.
    existing_values = extract_values(
        image, length, positions, rgb_order, index_list)
    # Compare current and new data to determine key effectiveness.
    key_effectiveness = data_comparison(
        existing_values, image_message, length, key_pixels)
    # Produce new image by replacing current data with new message data.
    result_image = attach_data(
        image, length, positions, rgb_order, image_message, index_list)
    # Build new image into an output file to view.
    result_image.save(LOCATION % "new_gate.png")
    # Return useful calculated metrics.
    return usage, key_effectiveness

# Function: API_image_extract
def API_image_extract(image_name, colour_selection: str = "random", input_key: int = 999, index_list: int = 7, key_pixels: int = 9):
    ''' Returns: Data Extracted from Image if Possible. '''
    # Load the appropriate image file for processing.
    image, width, height = load_image(image_name)
    # Create a unique key from image and input key.
    key, positions = gen_key(input_key, image, width, height, key_pixels)
    # Generate list of which RGB value to modify at each pixel.
    rgb_order = gen_colours(key, positions, colour_selection)
    # Calculate end point key from image size.
    width_length, height_length = key_conversion(width, height)
    # Decipher end point from image data.
    end_position, key_length = extract_key(
        image, positions, rgb_order, width_length, height_length, index_list)
    # Extract remaining image data from image.
    binary_data = data_extract(
        image, positions, rgb_order, end_position, key_length, index_list)
    # Convert extracted data from binary to plaintext.
    return binary_conversion(binary_data, "decimal")

data = "Please work for the love of god!"
key = 10
index = [0,1]
colour = "random"
print(API_image_append("gate.png", data, colour, key, index, True))
print(API_image_extract("new_gate.png", colour, key, index))
