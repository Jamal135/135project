'''Creation Date: 05/04/2021'''


from base64 import b32encode, b32decode, b16encode, b16decode, b64encode, b64decode, b85encode, b85decode
from secrets import choice as secret_choice
from random import seed, sample, randint
from time import time as epochtime
from math import trunc

# Base 85 Character Set.
B85 = {
    "size": 85,
    "set": "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!#$%&()*+-;<=>?@^_`{|}~",
    "encode": b85encode,
    "decode": b85decode,
    "padding": False,
    "pad": "",
    "gap": 0
}

# Base 64 Character Set.
B64 = {
    "size": 64,
    "set": "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+/",
    "encode": b64encode,
    "decode": b64decode,
    "padding": True,
    "pad": "=",
    "gap": 4
}

# Base 16 Character Set.
B16 = {
    "size": 16,
    "set": "0123456789ABCDEF",
    "encode": b16encode,
    "decode": b16decode,
    "padding": False,
    "pad": "",
    "gap": 0
}

# Base 10 Decimal Set.
B10 = {
    "set": "0123456789",
    "size": 10
}

# Define Acceptable Encoding Formats.
FORMATS = {
    "base16": B16,
    "base64": B64,
    "base85": B85
}


def time_read(length: int = 0):
    """ Returns: Time Since Epoch as Int. """
    try:
        time = (trunc(epochtime() * 1000) - 1616653584820)
    except:
        raise ValueError("Time Read Failed")
    return time if length == 0 else time % (10**length)


def gen_random(length: int = 12):
    """ Returns: Python Secrets Random Generate Number of X Length. """
    return int(''.join(secret_choice(B10["set"]) for _ in range(length)))


def gen_nonce(nonce_type):
    """ Returns: Nonce Integer Based on Provided Nonce Argument. """
    if nonce_type == "time":
        return time_read()
    if nonce_type == "random":
        return gen_random()
    if nonce_type == "hybrid":
        return int(str(gen_random(6)) + str(time_read(6)))
    try:
        return abs(int(nonce_type)) + 1
    except:
        raise ValueError(f"Invalid Nonce Argument: {nonce_type}")


def in_position(in_string, in_set):
    """ Returns: List of int String Index Positions in Set. """
    return list(map(lambda char: in_set.find(char), in_string))[::-1]


def convert_decimal(in_string, in_base, in_pos_list):
    """ Returns: Decimal Int Representation of Input. """
    if in_base == 10:
        return str(in_string)
    return sum(map(lambda pos: (in_base**pos[0])*pos[1], enumerate(in_pos_list)))


def input_divmod(input_quotient, out_base):
    """ Returns: List of Remainder Values for Each Character Position Calculated. """
    remainder_list = []
    while input_quotient > 0:
        input_quotient, remainder = divmod(input_quotient, out_base)
        remainder_list.append(remainder)
    return remainder_list[::-1]


def out_position(int_in_string: int, out_base):
    """ Returns: Representation of Int in Output Base. """
    return input_divmod(int_in_string, out_base)


def sub_characters(out_pos_point, output_set):
    """ Returns: List of Output Set Character at each Output Position Index. """
    if isinstance(out_pos_point, int):
        return output_set[out_pos_point]
    else:
        return "".join(list(map(lambda pos: output_set[pos], out_pos_point)))


def base_convert(in_string, in_base, out_base, input_set, output_set):
    """ Returns: Representation of Input in Different Base with Selected Character Set. """
    if in_base != 10:
        in_pos_list = in_position(in_string, input_set)
        int_in_string = convert_decimal(in_string, in_base, in_pos_list)
    else:
        int_in_string = in_string
    out_pos_list = out_position(int_in_string, out_base)
    return sub_characters(out_pos_list, output_set)


def text_encoding(in_text, argument, encoding):
    """ Returns: Base Encoded or Decoded Text. """
    try:
        encode_text = in_text.encode('utf-8')
        if argument == "encode":
            encoded_byte_text = encoding["encode"](encode_text)
        else:
            encoded_byte_text = encoding["decode"](encode_text)
        return encoded_byte_text.decode('utf-8')
    except:
        raise ValueError(f"Invalid Text Input: {in_text}")


def convert_input(in_text, argument, encoding):
    """ Returns: Input Text Correctly Encoded or Decoded. """
    if argument == "encode":
        converted_text = text_encoding(in_text, "encode", encoding)
        if encoding["padding"] == True:
            return converted_text.replace(encoding["pad"], "")
        else:
            return converted_text
    else:
        if encoding["padding"] == True:
            padding = encoding["gap"] - (len(in_text) % encoding["gap"])
            padded_text = in_text + (encoding["pad"] * padding)
        else:
            padded_text = in_text
        return text_encoding(padded_text, "decode", encoding)


def key_convert(key, encoding):
    """ Returns: Decimal Base10 Representation of Input Key. """
    try:
        encoded_key = text_encoding(key, "encode", encoding)
        return int(base_convert(encoded_key, encoding["size"], B10["size"], encoding["set"], B10["set"]))
    except:
        raise ValueError(f"Invalid Key Input: {key}")


def list_mix(set_key, encoding, in_set=""):
    """ Returns: Seeded Random Shuffle of Input Set by Input Key. """
    char_set = list(encoding["set"]) if in_set == "" else in_set
    seed(set_key)
    return sample(char_set, len(char_set))


def gen_char_sets(keyA, keyB, length, encoding):
    """ Returns: List of Lists of Character Sets Shuffled by Key. """
    pos_list = range(length)
    set_key = int(keyB) + int(str(keyA)[:274])
    keyB_set = list_mix(keyB, encoding)
    in_set = list_mix(keyA, encoding, keyB_set)
    return list(map(lambda pos: list_mix(set_key + pos[0], encoding, in_set), enumerate(pos_list)))


def gen_numbers(key, min_value, max_value, num_values: int = 1):
    """ Returns: Variable Length List of Random Numbers in Defined Range. """
    seed(key)
    if num_values == 1:
        return randint(min_value, max_value)
    else:
        return [randint(min_value, max_value) for _ in range(num_values)]


def gen_shift_values(key, length, argument, encoding, divider: int = 2, counter: int = 1):
    """ Returns: List Length Long of Generated Shifting Values. """
    pos_list = range(length)
    sign = 1 if argument == "encrypt" else -1
    x = list(map(lambda pos: gen_numbers(
        key + (pos*counter), 1, encoding["size"], 1)*sign, pos_list))
    y = list(map(lambda pos: gen_numbers(
        key + (pos*counter), 1, 2, 1)*sign, pos_list))
    return (list(map(lambda pos: int(x[pos] + (x[pos - 1]/2)) + y[pos], pos_list)))


def shift_prev_values(in_points, sets, argument, encoding):
    """ Returns: Input Position Modified by Index of the Previous Character. """
    sign = 1 if argument == "encrypt" else -1
    char_set = sets[0]
    new_points = [(in_points[0] + (147 * sign)) % encoding["size"]]
    if argument == "encrypt":
        prev_char = char_set[(new_points[0])]
    else:
        prev_char = char_set[(in_points[0])]
    for pos in range(len(in_points) - 1):
        char_set = sets[pos + 1]
        new_points.append(
            (in_points[pos + 1] + (char_set.index(prev_char) * sign)) % encoding["size"])
        if argument == "encrypt":
            prev_char = char_set[(new_points[pos + 1])]
        else:
            prev_char = char_set[(in_points[pos + 1])]
    return new_points


def relative_shift(key, length, in_text, sets, argument, encoding):
    """ Returns: Each Character in Input Text Shifted on Respective Set by Respective Shifting Value. """
    pos_list = range(length)
    in_values = list(
        map(lambda pos: (sets[pos].index(in_text[pos])), pos_list))
    shift_values = gen_shift_values(key, length, argument, encoding)
    if argument == "encrypt":
        new_points = list(map(lambda pos: (
            shift_values[pos] + in_values[pos]) % encoding["size"], pos_list))
        end_points = shift_prev_values(new_points, sets, argument, encoding)
    else:
        new_points = shift_prev_values(in_values, sets, argument, encoding)
        end_points = list(map(lambda pos: (
            shift_values[pos] + new_points[pos]) % encoding["size"], pos_list))
    return "".join(list(map(lambda pos: sub_characters(end_points[pos], sets[pos]), pos_list)))


def substitution(keyA, keyB, in_text, encoding, argument, direction):
    """ Returns: String of Characters Substituted Based on Input Keys. """
    if direction == "reverse" and argument == "encrypt":
        text = in_text[::-1]
    else:
        text = in_text
    length = len(text)
    char_sets = gen_char_sets(keyA, keyB, length, encoding)
    shifted_text = relative_shift(
        keyA, length, text, char_sets, argument, encoding)
    if direction == "reverse" and argument == "decrypt":
        return shifted_text[::-1]
    else:
        return shifted_text


def convert_nonce(key, nonce, argument, encoding):
    """ Returns: Nonce Encoded and Encrypted, or Decrypted and Decoded. """
    if argument == "encrypt":
        encoded_nonce = base_convert(
            nonce, B10["size"], encoding["size"], B10["set"], encoding["set"])
        shifted_nonce = substitution(
            key, 147, encoded_nonce, encoding, "encrypt", "normal")
        return substitution(key + 147, 147, shifted_nonce, encoding, "encrypt", "reverse")
    else:
        shifted_nonce = substitution(
            key + 147, 147, nonce, encoding, "decrypt", "reverse")
        encoded_nonce = substitution(
            key, 147, shifted_nonce, encoding, "decrypt", "normal")
        return int(base_convert(encoded_nonce, encoding["size"], B10["size"], encoding["set"], B10["set"]))


def nonce_format(char_set, nonce, num_text, encoding):
    """ Returns: Nonce Input Correctly Formatted for Appending. """
    nonce_length = len(nonce)
    if nonce_length >= 3968:
        raise ValueError("Max Nonce Length Exceeded")
    len_calc = input_divmod(nonce_length, encoding['size'] - 1)
    if len(len_calc) == 1:
        nonce_key = str(char_set[len_calc[0]]) + nonce
    else:
        nonce_key = str(len_calc[0]*char_set[-1]) + \
            str(char_set[len_calc[1]]) + nonce
    return len(nonce_key) + num_text, nonce_key


def gen_point_key(in_text, char_set):
    """ Returns: Key Integer Derived from Index of Last Character and Sum of Text. """
    index_points = in_position(in_text, "".join(char_set))
    sum_points = sum(index_points)
    last_char = char_set.index(in_text[len(in_text) - 1])
    return sum_points + (last_char * 147)


def text_pair(in_text, insert_points, char_set, nonce):
    """ Returns: Input Text and Nonce Combined into one String. """
    in_list = list(in_text)
    num_chars = len(nonce)
    cut_points = insert_points[:num_chars]
    reversed_nonce = nonce[::-1]
    reversed_points = cut_points[::-1]
    for pos, index in enumerate(reversed_points):
        if index >= len(in_list) - 1:
            index = len(in_list) - 1
        in_list.insert(index, reversed_nonce[pos])
    return "".join(in_list)


def text_split(in_text, insert_points, char_set):
    """ Returns: Input Text Split into Text and Nonce Strings. """
    nonce_key = []
    encrypted_nonce = ""
    in_list = list(in_text)
    for pos in range(3967):
        if insert_points[pos] >= len(in_list) - 1:
            point = len(in_list) - 2
        else:
            point = insert_points[pos]
        char = in_list[point]
        in_list.pop(point)
        nonce_key.append(char)
        if char is not char_set[-1]:
            break
    length = (len(nonce_key) - 1) * (len(char_set) - 2) + char_set.index(
        nonce_key[-1])
    for pos in range(length):
        if insert_points[pos + len(nonce_key)] >= len(in_list) - 1:
            point = len(in_list) - 2
        else:
            point = insert_points[pos + len(nonce_key)]
        char = in_list[point]
        in_list.pop(point)
        encrypted_nonce += char
    return "".join(in_list), encrypted_nonce


def pair_function(in_text, key, encoding, nonce: int = None):
    """ Returns: Input Text with Nonce Randomly Attached/Extracted Based on Key. """
    char_set = list_mix(key + 144, encoding)
    num_text = len(in_text)
    if nonce is not None:
        encrypted_nonce = convert_nonce(key, nonce, "encrypt", encoding)
        length, nonce_key = nonce_format(
            char_set, encrypted_nonce, num_text, encoding)
        point_key = gen_point_key(nonce_key + in_text, char_set)
        points = gen_numbers(key + point_key, 0, length, length)
        return text_pair(in_text, points, char_set, nonce_key)
    else:
        point_key = gen_point_key(in_text, char_set)
        points = gen_numbers(key + point_key, 0, num_text, num_text)
        split_text, nonce = text_split(in_text, points, char_set)
        return split_text, convert_nonce(key, nonce, "decrypt", encoding)


def encrypt_147(key, in_text, formatting: str = "base64", nonce_type: str = "hybrid"):
    """ Returns: Input Text 147 Encrypted with Input Key. """
    try:
        try:
            encoding = FORMATS[formatting]
        except:
            raise ValueError("Invalid Encoding Argument")
        nonce = gen_nonce(nonce_type)
        encoded_text = convert_input(in_text, "encode", encoding)
        dec_key = key_convert(key, encoding)
        shifted_text = substitution(
            dec_key, nonce, encoded_text, encoding, "encrypt", "normal")
        full_text = pair_function(shifted_text, dec_key, encoding, nonce)
        return substitution(dec_key + 135, 147, full_text, encoding, "encrypt", "reverse")
    except:
        raise ValueError(
            f"Encryption with Key: {key} Failed for Input: {in_text}")


def decrypt_147(key, in_text, formatting: str = "base64"):
    """ Returns: Input Text 147 Decrypted with Input Key. """
    try:
        try:
            encoding = FORMATS[formatting]
        except:
            raise ValueError("Invalid Encoding Argument")
        dec_key = key_convert(key, encoding)
        shifted_text = substitution(
            dec_key + 135, 147, in_text, encoding, "decrypt", "reverse")
        split_text, nonce = pair_function(shifted_text, dec_key, encoding)
        encoded_text = substitution(
            dec_key, nonce, split_text, encoding, "decrypt", "normal")
        return convert_input(encoded_text, "decode", encoding)
    except:
        raise ValueError(
            f"Decryption with Key: {key} Failed for Input: {in_text}")
