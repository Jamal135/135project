
# Some fancy description is definitely here

# Creation date: 25/05/2021

# Imported Tools.
from os import path
from PIL import Image
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
        raise ValueError("Image Read Failed")
    width, height = image.size
    return image, width, height

# Function: gen_key
def gen_key(key, image, width, height):
    return key + (height * width)

# Function: image_coordinates
# Note: key must be remembered unless default is used.
def image_coordinates(height, width, key):
    ''' Returns: Shuffled list of image coordinate tuples. '''
    seed(key)
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
def length_calculator(width, height, data=None):
    ''' Returns: Length Calculations of Data Components. '''
    width_length, height_length = key_conversion(width, height)
    if data != None:
        data_length = len(data)
        total_length = width_length + height_length + data_length
        return total_length, width_length, height_length
    else:
        return width_length, height_length

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
    width_key = integer_conversion(
        end_position[0], "binary").zfill(width_length)
    height_key = integer_conversion(
        end_position[1], "binary").zfill(height_length)
    return width_key, height_key

# Function: gen_numbers
def gen_numbers(key, min_value, max_value, number_values: int = 1):
    """ Returns: Variable Length List of Random Numbers in Defined Range. """
    seed(key)
    if number_values == 1:
        return randint(min_value, max_value)
    else:
        return [randint(min_value, max_value) for _ in range(number_values)]

# Function: message_generator
def message_generator(key, data, width, height, positions, noise=False):
    ''' Returns: Correctly Built Binary Data to Attach to Image. '''
    total_length, width_length, height_length = length_calculator(
        width, height, data)
    pixel_utilisation = capacity_check(total_length, len(positions))
    width_key, height_key = end_point(
        positions, total_length, width_length, height_length)
    message_data = width_key + height_key + data
    if noise:
        remaining_space = (width * height) - len(message_data)
        noise_list = gen_numbers(key, 0, 1, remaining_space)
        noise_string = "".join(map(str, noise_list))
        built_data = message_data + noise_string
    else:
        built_data = message_data
    length = len(built_data)
    return built_data, length, pixel_utilisation

# Function: extract_values
def extract_values(image, length, positions, rgb_order):
    ''' Returns: Existing Binary Data to be Replaced. '''
    locations = [image.getpixel(
        (positions[point][1], positions[point][0])) for point in range(length)]
    exact_points = [locations[point][rgb_order[point]]
                    for point in range(length)]
    binary_values = [integer_conversion(
        exact_points[point], "binary").zfill(8) for point in range(length)]
    return "".join([binary_values[point][7] for point in range(length)])

# Function: data_comparison
def data_comparison(current_values, new_values, length):
    ''' Returns: Percentage Measure of how close two Binary Strings Match. '''
    matches = sum([1 for point in range(length)
                  if current_values[point] == new_values[point]])
    return round((100/length) * matches, 2)

# Function: data_rebuild
def data_rebuild(locations, new_values, rgb_order, length):
    ''' Returns: Modified List of Tuples given New Values. '''
    input_list = [list(element) for element in locations]
    for point in range(length):
        input_list[point][rgb_order[point]] = new_values[point]
    return [tuple(element) for element in input_list]

# Function: attach_data
def attach_data(image, length, positions, rgb_order, image_message):
    ''' Returns: New Image Data with RGB colours Correctly Modified with Data. '''
    locations = [image.getpixel(
        (positions[point][1], positions[point][0])) for point in range(length)]
    exact_points = [locations[point][rgb_order[point]]
                    for point in range(length)]
    binary_values = [integer_conversion(
        exact_points[point], "binary").zfill(8) for point in range(length)]
    new_binary_values = [binary_values[point][0:7] +
                         image_message[point] for point in range(length)]
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
def extract_key(image, positions, rgb_order, width_length, height_length):
    ''' Returns: Extracted Data End Point. '''
    key_length = width_length + height_length
    key_data = extract_values(image, key_length, positions, rgb_order)
    width_key = integer_conversion(key_data[:width_length], "decimal")
    height_key = integer_conversion(key_data[width_length:], "decimal")
    end_position = (width_key, height_key)
    return end_position, key_length

# Function: data_extract
def data_extract(image, positions, rgb_order, end_position, key_length):
    ''' Returns: Extracted binary data from provided image. '''
    modified_positions = positions[key_length:]
    modified_rgb_order = rgb_order[key_length:]
    length = positions.index(end_position) - key_length
    return extract_values(image, length, modified_positions, modified_rgb_order)

# Function: API_image_append
# key: Shuffles Order of Image Locations.
def API_image_append(image_name, indata, input_key: int = 999, noise: bool = False):
    ''' Returns: Data Appended to Image if Possible. '''
    # Load the appropriate image file for processing.
    image, width, height = load_image(image_name)
    # Create a unique key from image and input key.
    key = gen_key(input_key, image, width, height)
    # Generate list of image coordinates for data ordering.
    positions = image_coordinates(height, width, key)
    # Generate list of which RGB value to modify at each pixel.
    rgb_order = gen_numbers(key, 0, 2, len(positions))
    # Generate the binary data to attach to the provided image.
    binary_indata = binary_conversion(indata, "binary")
    # Compile the complete message to be attached to the image.
    image_message, length, usage = message_generator(
        key, binary_indata, width, height, positions, noise)
    # Extract the existing values from the image that will be replaced.
    existing_values = extract_values(image, length, positions, rgb_order)
    # Compare current and new data to determine key effectiveness.
    key_effectiveness = data_comparison(existing_values, image_message, length)
    # Produce new image by replacing current data with new message data.
    result_image = attach_data(
        image, length, positions, rgb_order, image_message)
    # Build new image into an output file to view.
    result_image.save(LOCATION % "new_gate.png")
    # Return useful calculated metrics.
    return usage, key_effectiveness

# Function: API_image_extract
def API_image_extract(image_name, input_key: int = 999):
    ''' Returns: Data Extracted from Image if Possible. '''
    # Load the appropriate image file for processing.
    image, width, height = load_image(image_name)
    # Create a unique key from image and input key.
    key = gen_key(input_key, image, width, height)
    # Generate list of image coordinates for data ordering.
    positions = image_coordinates(height, width, key)
    # Generate list of which RGB value to modify at each pixel.
    rgb_order = gen_numbers(key, 0, 2, len(positions))
    # Calculate end point key from image size.
    width_length, height_length = length_calculator(width, height, None)
    # Decipher end point from image data.
    end_position, key_length = extract_key(
        image, positions, rgb_order, width_length, height_length)
    # Extract remaining image data from image.
    binary_data = data_extract(
        image, positions, rgb_order, end_position, key_length)
    # Convert extracted data from binary to plaintext.
    return binary_conversion(binary_data, "decimal")

x = "Please work for the love of god!"
print(API_image_append("gate.png", x, 9, False))
print(API_image_extract("new_gate.png", 9))
