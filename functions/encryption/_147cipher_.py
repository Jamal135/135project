
# 147Cipher is a substitution based symmetric encryption algorithm which is intended to build upon 135Cipher. Any
# input that can be UTF-8 encoded is supported as a key input and/or as a text input. If the text being encrypted, 
# the key being used for encryption, or the generated nonce change at all, the resulting cipher text will be 
# completely different. The nonce integer can be generated from the current time, as a random value, or as a 
# combination of the two. The generated Nonce is attached to the cipher text in a way derived from  the input text 
# and key such that it is not a value that must be remembered to allow for decryption. This algorithm, however, is 
# not proven to be secure which means it should not be relied upon for any reason. 
# This algorithm is housed at: 135code.com/147cipher
# Creation Date: 05/04/2021

# 147 Cipher Setup.

# Imported Tools.
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
# Base 32 Character Set.
B32 = { 
    "size": 32, 
    "set": "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567",
    "encode": b32encode,
    "decode": b32decode,
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
    "base32": B32,
    "base64": B64,
    "base85": B85
}

# Function: time_read
# Note - 1616653584820 is to Remove Time Prior to Cipher Use Starting
def time_read(length:int = 0):
    """ Returns: Time Since Epoch as Int. """
    try: time = (trunc(epochtime() * 1000) - 1616653584820)
    except: raise ValueError("Time Read Failed")
    if length == 0: return time
    else: return time % (10**length)

# Function: gen_random
def gen_random(length:int = 12):
    """ Returns: Python Secrets Random Generate Number of X Length. """
    return int(''.join(secret_choice(B10["set"]) for _ in range(length)))

# Function: gen_nonce
def gen_nonce(nonce_type):
    """ Returns: Nonce Integer Based on Provided Nonce Argument. """
    if nonce_type == "time": return time_read()
    if nonce_type == "random": return gen_random()
    if nonce_type == "hybrid": return int(str(gen_random(6)) + str(time_read(6)))
    try: return abs(int(nonce_type)) + 1
    except: raise ValueError(f"Invalid Nonce Argument: {nonce_type}")

# Function: in_position
# in_set: Set of Characters to Index Input Against.
def in_position(in_string, in_set):
    """ Returns: List of int String Index Positions in Set. """
    return list(map(lambda char:in_set.find(char), in_string))[::-1]

# Function: convert_decimal
# in_base: Base of Input (number unique characters).
# in_pos_list: List of Index Positions of Input against Set.
def convert_decimal(in_string, in_base, in_pos_list):
    """ Returns: Decimal Int Representation of Input. """
    if in_base == 10: return str(in_string)
    return sum(map(lambda pos:(in_base**pos[0])*pos[1], enumerate(in_pos_list)))

# Function: input_divmod
def input_divmod(input_quotient, out_base):
    """ Returns: List of Remainder Values for Each Character Position Calculated. """
    remainder_list = []
    while input_quotient > 0:
        input_quotient, remainder = divmod(input_quotient, out_base)
        remainder_list.append(remainder)
    return remainder_list[::-1]

# Function: out_position
# out_base: Base of Output (number unique characters).
def out_position(int_in_string:int, out_base):
    """ Returns: Representation of Int in Output Base. """
    return input_divmod(int_in_string, out_base)

# Function: sub_characters
# out_pos_point: Single or List of Character Index Positions.
# output_set: Set of Unique Characters.
def sub_characters(out_pos_point, output_set):
    """ Returns: List of Output Set Character at each Output Position Index. """
    if isinstance(out_pos_point, int): return output_set[out_pos_point]
    else: return "".join(list(map(lambda pos: output_set[pos], out_pos_point)))

# Function: base_convert
def base_convert(in_string, in_base, out_base, input_set, output_set):
    """ Returns: Representation of Input in Different Base with Selected Character Set. """
    if in_base != 10:
        # Create List of Index Positions of in_string in input_set.
        in_pos_list = in_position(in_string, input_set)
        # Convert in_string into Decimal (Base10) Number.
        int_in_string = convert_decimal(in_string, in_base, in_pos_list)
    else: int_in_string = in_string
    # Convert Decimal Number into out_base Number.
    out_pos_list = out_position(int_in_string, out_base)
    # Substitute Index List (out_pos_list) for defined output_set characters.
    return sub_characters(out_pos_list, output_set)

# Function: text_encoding
def text_encoding(in_text, argument, encoding):
    """ Returns: Base Encoded or Decoded Text. """
    try:
        encode_text = in_text.encode('utf-8')
        if argument == "encode": encoded_byte_text = encoding["encode"](encode_text)
        else: encoded_byte_text = encoding["decode"](encode_text)
        return encoded_byte_text.decode('utf-8')
    except: raise ValueError(f"Invalid Text Input: {in_text}")

# Function: convert_input
def convert_input(in_text, argument, encoding):
    """ Returns: Input Text Correctly Encoded or Decoded. """
    if argument == "encode":
        # Encode Input into Selected Encoding Format.
        converted_text = text_encoding(in_text, "encode", encoding)
        # Remove Padding from Encoded Text if Necessary.
        if encoding["padding"] == True: return converted_text.replace(encoding["pad"], "")
        else: return converted_text
    else:
        if encoding["padding"] == True:
            # Calculate Required Padding to Add.
            padding = encoding["gap"] - (len(in_text) % encoding["gap"])
            # Restore Padding to Encoded Input.
            padded_text = in_text + (encoding["pad"] * padding)
        else: padded_text = in_text
        # Decode Input from Specified Encoding.
        return text_encoding(padded_text, "decode", encoding)

# Function: key_convert
def key_convert(key, encoding):
    """ Returns: Decimal Base10 Representation of Input Key. """
    try:
        encoded_key = text_encoding(key, "encode", encoding)
        return int(base_convert(encoded_key, encoding["size"], B10["size"], encoding["set"], B10["set"]))
    except: raise ValueError(f"Invalid Key Input: {key}")

# Function: list_mix
# set_key: Minor Key to Seed Random Shuffle.
# in_set: Set of Characters to Shuffle.
def list_mix(set_key, encoding, in_set = ""):
    """ Returns: Seeded Random Shuffle of Input Set by Input Key. """
    if in_set == "": char_set = list(encoding["set"])
    else: char_set = in_set
    seed(set_key)
    return sample(char_set, len(char_set))

# Function: gen_char_sets
# keyA: Primary Key for Encryption/Decryption.
# KeyB: Nonce Value, Time, Random, Hybrid, or Fixed.
def gen_char_sets(keyA, keyB, length, encoding):
    """ Returns: List of Lists of Character Sets Shuffled by Key. """
    pos_list = range(length)
    # Calculate Primary set_key with keyB.
    set_key = int(keyB) + int(str(keyA)[:274])
    # Create Shuffled Character Set Using keyB.
    keyB_set = list_mix(keyB, encoding)
    # Create Shuffled keyB Set Using KeyA.
    in_set = list_mix(keyA, encoding, keyB_set)
    # Generate List of Lists of in_set Character Sets Randomly Shuffled.
    return list(map(lambda pos: list_mix(set_key + pos[0], encoding, in_set), enumerate(pos_list)))

# Function: gen_numbers
# min_value: Lowest integer value to possibly be in output.
# max_value: Highest integer value to possibly be in output.
# numberValues: Number of Random Values to be in List.
def gen_numbers(key, min_value, max_value, num_values:int = 1):
    """ Returns: Variable Length List of Random Numbers in Defined Range. """
    seed(key)
    if num_values == 1: return randint(min_value, max_value)
    else: return [randint(min_value, max_value) for _ in range(num_values)]

# Function: gen_shift_values
# divider: Divide Addition by Minor Divider Key.
# counter: Minor value that if modified changes result.
def gen_shift_values(key, length, argument, encoding, divider:int = 2, counter:int = 1):
    """ Returns: List Length Long of Generated Shifting Values. """
    pos_list = range(length)
    if argument == "encrypt": sign = 1
    else: sign = -1
    x = list(map(lambda pos: gen_numbers(key + (pos*counter), 1, encoding["size"], 1)*sign, pos_list))
    y = list(map(lambda pos: gen_numbers(key + (pos*counter), 1, 2, 1)*sign, pos_list))
    return (list(map(lambda pos: int(x[pos] + (x[pos - 1]/2)) + y[pos], pos_list)))

# Function: shift_prev_values
def shift_prev_values(in_points, sets, argument, encoding):
    """ Returns: Input Position Modified by Index of the Previous Character. """
    new_points = []
    if argument == "encrypt": sign = 1
    else: sign = -1
    char_set = sets[0]
    new_points.append((in_points[0] + (147 * sign)) % encoding["size"])
    if argument == "encrypt": prev_char = char_set[(new_points[0])]
    else: prev_char = char_set[(in_points[0])]
    for pos in range(len(in_points) -1):
        char_set = sets[pos + 1]
        new_points.append((in_points[pos + 1] + (char_set.index(prev_char) * sign)) % encoding["size"])
        if argument == "encrypt": prev_char = char_set[(new_points[pos + 1])]
        else: prev_char = char_set[(in_points[pos + 1])]
    return new_points

# Function: relativeCharShift
def relative_shift(key, length, in_text, sets, argument, encoding):
    """ Returns: Each Character in Input Text Shifted on Respective Set by Respective Shifting Value. """
    # Create Iterator List of Positions for Calculations.
    pos_list = range(length)
    # Generate list of Current Index Positions for all Characters.
    in_values = list(map(lambda pos: (sets[pos].index(in_text[pos])), pos_list))
    # Generate Key Derived Shifting Values for all Characters in Encoded Text.
    shift_values = gen_shift_values(key, length, argument, encoding)
    # Shift by Prev Values and Shift Values in Order Based upon Provided Argument.
    if argument == "encrypt":
        new_points = list(map(lambda pos: (shift_values[pos] + in_values[pos]) % encoding["size"], pos_list))
        end_points = shift_prev_values(new_points, sets, argument, encoding)
    else:
        new_points = shift_prev_values(in_values, sets, argument, encoding)
        end_points = list(map(lambda pos: (shift_values[pos] + new_points[pos]) % encoding["size"], pos_list))
    # Substitute Shifted Index Positions for respective Characters at Index Positions.
    return "".join(list(map(lambda pos: sub_characters(end_points[pos], sets[pos]), pos_list)))

# Function: substitution
# keyA: The Key used in Encryption/Decryption.
# keyB: The Generated or Fixed Nonce Integer Value.
# direction: Substitute down Text or up Text.
# "normal" = down | "reverse" = up   
def substitution(keyA, keyB, in_text, encoding, argument, direction):
    """ Returns: String of Characters Substituted Based on Input Keys. """
    # Reverse Input Text Based upon in Argument and Direction.
    if direction == "reverse" and argument == "encrypt": text = in_text[::-1]
    else: text = in_text
    # Read length of the Encoded Text.
    length = len(text)
    # Generate Key + Nonce Seeded Character Set for all Characters.
    char_sets = gen_char_sets(keyA, keyB, length, encoding)
    # Positively Shift all Text by Respective Values across Respective Char Sets.
    shifted_text = relative_shift(keyA, length, text, char_sets, argument, encoding)
    # Reverse Output Text Based Upon in Argument and Direction.
    if direction == "reverse" and argument == "decrypt": return shifted_text[::-1]
    else: return shifted_text

# Function: convert_nonce
def convert_nonce(key, nonce, argument, encoding):
    """ Returns: Nonce Encoded and Encrypted, or Decrypted and Decoded. """
    if argument == "encrypt":
        encoded_nonce = base_convert(nonce, B10["size"], encoding["size"], B10["set"], encoding["set"])
        shifted_nonce = substitution(key, 147, encoded_nonce, encoding, "encrypt", "normal")
        return substitution(key + 147, 147, shifted_nonce, encoding, "encrypt", "reverse")
    else:
        shifted_nonce = substitution(key + 147, 147, nonce, encoding, "decrypt", "reverse")
        encoded_nonce = substitution(key, 147, shifted_nonce, encoding, "decrypt", "normal")
        return int(base_convert(encoded_nonce, encoding["size"], B10["size"], encoding["set"], B10["set"]))

# Function: nonce_format
# Note - If nonce_length Exceeds 3968, Function Breaks (Shouldn't Happen).
def nonce_format(char_set, nonce, num_text, encoding):
    """ Returns: Nonce Input Correctly Formatted for Appending. """
    nonce_length = len(nonce)
    if nonce_length >= 3968: raise ValueError("Max Nonce Length Exceeded")
    len_calc = input_divmod(nonce_length, encoding['size'] -1)
    if len(len_calc) == 1: nonce_key = str(char_set[len_calc[0]]) + nonce
    else: nonce_key = str(len_calc[0]*char_set[-1]) + str(char_set[len_calc[1]]) + nonce
    return len(nonce_key) + num_text, nonce_key

# Function: gen_point_key
def gen_point_key(in_text, char_set):
    """ Returns: Key Integer Derived from Index of Last Character and Sum of Text. """
    index_points = in_position(in_text, "".join(char_set))
    sum_points = sum(index_points)
    last_char = char_set.index(in_text[len(in_text) - 1])
    return sum_points + (last_char * 147)

# Function: text_pair
def text_pair(in_text, insert_points, char_set, nonce):
    """ Returns: Input Text and Nonce Combined into one String. """
    in_list = list(in_text)
    num_chars = len(nonce)
    cut_points = insert_points[:num_chars]
    reversed_nonce = nonce[::-1]
    reversed_points = cut_points[::-1]
    for pos, index in enumerate(reversed_points):
        if index >= len(in_list) - 1: index = len(in_list) - 1
        in_list.insert(index, reversed_nonce[pos])
    return "".join(in_list)

# Function: text_split
def text_split(in_text, insert_points, char_set):
    """ Returns: Input Text Split into Text and Nonce Strings. """
    nonce_key = []
    encrypted_nonce = ""
    in_list = list(in_text)
    for pos in range(3967):
        if insert_points[pos] >= len(in_list) - 1: point = len(in_list) - 2
        else: point = insert_points[pos]
        char = in_list[point]
        in_list.pop(point)
        nonce_key.append(char)
        if char is not char_set[-1]: break
    length = ((len(nonce_key) - 1) * (len(char_set) -2)) + char_set.index(nonce_key[len(nonce_key) - 1])
    for pos in range(length):
        if insert_points[pos + len(nonce_key)] >= len(in_list) - 1: point = len(in_list) - 2
        else: point = insert_points[pos + len(nonce_key)]
        char = in_list[point]
        in_list.pop(point)
        encrypted_nonce = encrypted_nonce + char
    return "".join(in_list), encrypted_nonce

# Function: pair_function
def pair_function(in_text, key, encoding, nonce:int = None):
    """ Returns: Input Text with Nonce Randomly Attached/Extracted Based on Key. """
    char_set = list_mix(key + 144, encoding)
    num_text = len(in_text)
    if nonce is not None:
        # Encode Nonce, Remove any Padding, and Encrypt.
        encrypted_nonce = convert_nonce(key, nonce, "encrypt", encoding)  
        # Find the Total Length and  Key Characters.
        length, nonce_key = nonce_format(char_set, encrypted_nonce, num_text, encoding)
        # Generate a Minor Key Based on Input Text.
        point_key = gen_point_key(nonce_key + in_text, char_set)
        # Generate Seeded List of Insertion Locations.
        points = gen_numbers(key + point_key, 0, length, length)
        # Join Text and Key into one String.
        return text_pair(in_text, points, char_set, nonce_key)
    else:
        # Generate a Minor Key Based on Input Text.
        point_key = gen_point_key(in_text, char_set)
        # Generate Seeded List of Insertion Locations.
        points = gen_numbers(key + point_key, 0, num_text, num_text)
        # Pull Nonce out of Input Text and Derive Original Text.
        split_text, nonce = text_split(in_text, points, char_set)
        # Decode Nonce and Return both the Split Text and Nonce.
        return split_text, convert_nonce(key, nonce, "decrypt", encoding)

# 147 Cipher Encryption Function.
def encrypt_147(key, in_text, formatting:str = "base64", nonce_type:str = "hybrid"):
    """ Returns: Input Text 147 Encrypted with Input Key. """
    try:
        # Ensure an Appropriate Encoding Argument is Provided.
        try: encoding = FORMATS[formatting]
        except: raise ValueError("Invalid Encoding Argument")
        # Generate Nonce Integer Based on Input Argument.
        nonce = gen_nonce(nonce_type)
        # Encode Text into Specified Encoding and Remove any Padding.
        encoded_text = convert_input(in_text, "encode", encoding)
        # Encode Key into Decimal Number (Base10).
        dec_key = key_convert(key, encoding)
        # Substitute Down Input Text.
        shifted_text = substitution(dec_key, nonce, encoded_text, encoding, "encrypt", "normal")
        # Randomly join Shifted Text and Nonce into one Text.
        full_text = pair_function(shifted_text, dec_key, encoding, nonce)
        # Substitute Up Input Text.
        return substitution(dec_key + 135, 147, full_text, encoding, "encrypt", "reverse")
    except: raise ValueError(f"Encryption with Key: {key} Failed for Input: {in_text}")

# 147 Cipher Decryption Function.
def decrypt_147(key, in_text, formatting:str = "base64"):
    """ Returns: Input Text 147 Decrypted with Input Key. """
    try:        
        # Ensure an Appropriate Encoding Argument is Provided.
        try: encoding = FORMATS[formatting]
        except: raise ValueError("Invalid Encoding Argument")
        # Encode Key into Decimal Number (Base10).
        dec_key = key_convert(key, encoding)
        # Substitute Down Input Text.
        shifted_text = substitution(dec_key + 135, 147, in_text, encoding, "decrypt", "reverse")
        # Seperate Shifted Text into Nonce and Text.
        split_text, nonce = pair_function(shifted_text, dec_key, encoding)
        # Substitute Up Input Text.
        encoded_text = substitution(dec_key, nonce, split_text, encoding, "decrypt", "normal")
        # Add any Required Padding and Decode Text into Plain Text.
        return convert_input(encoded_text, "decode", encoding)
    except: raise ValueError(f"Decryption with Key: {key} Failed for Input: {in_text}")
