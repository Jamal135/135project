'''Creation date: __/__/____'''

import random
import base64


def generate_alpha_sequence(input):
    character_list = ['E', 'I', 'p', '7', '3', 'Q', 'V', 'A', '0', 'm', 'j', 'x', 'v', 'J', '9',
                      'H', 'M', 'F', 'f', 'T', 'n', 'D', 'S', '6', 'Y', 'k', '5', 'o', '/', 'U',
                      'w', 'c', 'h', 'd', 'l', 'L', 'z', 'X', '+', 's', 'R', 'g', 'b', 'r', 'O',
                      '1', 'B', 'e', 'P', 'y', 'a', 'C', 't', 'Z', 'K', 'W', 'i', 'N', '8', 'G',
                      '=', 'u', '4', 'q', '2']
    length = len(character_list)
    random.seed(input)
    return (random.sample(character_list, length))


def character_replace(input_list, argument, factor):
    characters = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    character_pool = ['E', 'I', 'p', 'Q', 'V', 'A', 'm', 'j', 'x', 'v', 'J', 'H', 'M', 'F', 'f',
                      'T', 'n', 'D', 'S', 'Y', 'k', 'o', '/', 'U', 'w', 'c', 'h', 'd', 'l', 'L',
                      'z', 'X', '+', 's', 'R', 'g', 'b', 'r', 'O', 'B', 'e', 'P', 'y', 'a', 'C',
                      't', 'Z', 'K', 'W', 'i', 'N', 'G', '=', 'u', 'q']
    output_list = []
    length = len(input_list)
    number_characters = len(characters)
    random.seed(factor)
    replacements = random.sample(character_pool, k=number_characters)
    count = 0
    while count in range(length):
        selected_character = input_list[count]
        if selected_character in characters and argument == '+':
            output_list.append('\a')
            position = characters.index(selected_character)
            output_list.append(replacements[position])
            count += 1
        elif selected_character == '\a' and argument == '-':
            selected_character = input_list[count + 1]
            position = replacements.index(selected_character)
            output_list.append(characters[position])
            count += 2
        else:
            output_list.append(selected_character)
            count += 1
    return output_list


def list_creation(input_text, argument):
    split_text = list(input_text)
    random.seed()
    if argument == '+':
        number_groups = random.randint(3, 15)
        for _ in range(number_groups):
            position = random.randint(1, len(input_text) - 2)
            split_text.insert(position, " ")
    if argument == '-':
        number_groups = 2
        split = (len(input_text)) // number_groups
        split_text.insert(split, " ")
    grouped_text = ''.join(split_text)
    list_groups = grouped_text.split(' ')
    output_list = list(map(list, list_groups))
    longest_word_length = len(max(list_groups, key=len))
    for selected_word in output_list:
        if len(selected_word) < longest_word_length:
            difference = (longest_word_length - len(selected_word))
            for _ in range(difference):
                selected_word.append('\b')
    return output_list


def join(input_list):
    for a_tuple in input_list:
        input_list[input_list.index(a_tuple)] = list(a_tuple)
    joined_lists = [''.join(a_list) for a_list in input_list]
    return list(' '.join(joined_lists))


def group(expanded_list, key):
    length = len(expanded_list)
    number_lists = int(length / key)
    output_list = []
    temporary_list = []
    for count_lists in range(key):
        for count_characters in range(number_lists):
            position_in_list = (number_lists * count_lists) + count_characters
            temporary_list.append(expanded_list[position_in_list])
        output_list.append(temporary_list)
        temporary_list = []
    return output_list


def transpose(input_list):
    return (list(zip(*input_list)))


def flatten(input_list):
    output_list = []
    for sublist in input_list:
        output_list.extend(iter(sublist))
    output_list.append('\a')
    return output_list


def calculation(factor, alpha_sequence_length, val):
    try:
        calculation = int((val * factor) + (((val * (factor + 1)) /
                          alpha_sequence_length)) - (((val * 13.5) / ((val + 1) / 6))))
    except:
        calculation = int(
            (val * factor) + (((val * (factor + 1)) / alpha_sequence_length)))
    return calculation


def factoring(factor, number_characters, alpha_sequence_length):
    primary_factor = int(factor)
    secondary_factor = primary_factor / 4
    previous_output = 135
    shifting_list = []
    for count in range(number_characters):
        primary_calculation = calculation(
            primary_factor, alpha_sequence_length, count + 1)
        inverse_count = ((count - 1) % number_characters) + 1
        secondary_calculation = calculation(
            secondary_factor, alpha_sequence_length, inverse_count)
        combined_calculation = primary_calculation - secondary_calculation
        if combined_calculation == 0:
            combined_calculation = 1
        output_calculation = int(calculation(
            primary_factor, alpha_sequence_length, combined_calculation))
        magic_a = int(str(output_calculation)[-9:])
        magic_b = int(str(output_calculation)[:8])
        magic_c = ((magic_a * magic_b) + (primary_factor ^ 2))
        magic_output = int(str(magic_c)[-9:])
        combined_output = magic_output + previous_output
        final_output = combined_output % alpha_sequence_length
        if count % 2 == 0:
            final_output = final_output + 1
        shifting_list.append(final_output)
        previous_output = final_output
    return shifting_list


def shift(factor, input_list, alpha_shift_list, alpha_sequence_length, argument, modifier):
    output_list = []
    length = len(input_list)
    shiftdirection = {'+': 1, '-': -1}
    old_character_position = 135
    base_sequence = generate_alpha_sequence(factor)
    if modifier == 1:
        length -= 1
        shift = base_sequence.index(input_list[length])
    for count in range(length):
        alphakey = ((int(factor) + (modifier * 135)) * (count + 1))
        alphabetical_sequence = generate_alpha_sequence(alphakey)
        current_character = input_list[count]
        character_position = alphabetical_sequence.index(current_character)
        if modifier == 0:
            shift = alpha_shift_list[count]
        new_character_position = ((character_position + (shiftdirection[argument] * shift)) + (
            shiftdirection[argument] * old_character_position)) % alpha_sequence_length
        new_character = alphabetical_sequence[new_character_position]
        if argument == '+':
            old_character_position = base_sequence.index(new_character)
        if argument == '-':
            old_character_position = base_sequence.index(current_character)
        output_list.append(new_character)
    if modifier == 1:
        output_list.append(input_list[length])
    return(output_list)


def shift_text(factor, input_list, alpha_shift_list, alpha_sequence_length, argument):
    if argument == '+':
        shift_list = shift(factor, input_list, alpha_shift_list,
                           alpha_sequence_length, '+', 0)
        output_list = shift(factor, shift_list,
                            alpha_shift_list, alpha_sequence_length, '+', 1)
    if argument == '-':
        shift_list = shift(factor, input_list, alpha_shift_list,
                           alpha_sequence_length, '-', 1)
        output_list = shift(factor, shift_list,
                            alpha_shift_list, alpha_sequence_length, '-', 0)
    return(output_list)


def key_insert(encode_list):
    key = (len(encode_list))
    key = list(str(key))
    length = (len(key))
    key_out = ['=']
    key_out.extend(key[val] for val in range(length))
    return key_out


def key_extract(decode_list):
    key = []
    length = (len(decode_list)) - 1
    character_type = True
    while character_type:
        character_input = decode_list[length]
        character_type = character_input.isdigit()
        if character_type is True:
            key.append(str(character_input))
        length = length - 1
    key = list(reversed(key))
    length = len(key)
    decode_list = decode_list[:-(length + 2)]
    key = int(''.join(map(str, key)))
    return key, decode_list


def remove(input_list):
    length = len(input_list)
    output_list = []
    for character_position in range(length):
        current_character = input_list[character_position]
        if current_character == '\b':
            current_character = ''
        output_list.append(current_character)
    return output_list


def special(input_list, argument, factor):
    character_pool = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    random.seed(factor)
    replacements = random.sample(character_pool, k=4)
    if argument == '+':
        output_list = []
        previous_character = ''
        for current_character in input_list:
            if current_character == '\a':
                if previous_character != replacements[2]:
                    output_list.extend([replacements[2]])
                else:
                    output_list.extend([replacements[3]])
            elif current_character == '\b':
                if previous_character != replacements[0]:
                    output_list.extend([replacements[0]])
                else:
                    output_list.extend([replacements[1]])
            else:
                output_list.append(current_character)
            previous_character = current_character
    elif argument == '-':
        output_list = []
        for count in range(len(input_list)):
            if input_list[count] in replacements[:2]:
                output_list.append('\b')
            elif input_list[count] in replacements[2:4]:
                output_list.append('\a')
            else:
                output_list.append(input_list[count])
    return output_list


def encrypt_135(factor, text, argument='-'):
    try:
        int(factor)
    except:
        raise ValueError(f"Invalid key integer {factor}")
    if len(str(factor)) > 135:
        raise ValueError("Key Max Length Exceeded")
    factor = str(int(factor) + 2)
    try:
        encode_string = text.encode('utf-8')
        encoded_byte_string = base64.b64encode(encode_string)
        encoded_string = encoded_byte_string.decode('utf-8')
        alphabetical_sequence = generate_alpha_sequence(factor)
        alpha_sequence_length = len(alphabetical_sequence)
        encrypt_list = list_creation(encoded_string, argument)
        transpose_list = transpose(encrypt_list)
        flattened_list = flatten(transpose_list)
        replaced_list = character_replace(flattened_list, '+', factor)
        key_store = key_insert(encrypt_list[0])
        replaced_list.extend(key_store)
        printable_list = special(replaced_list, '+', factor)
        number_characters = len(printable_list)
        alpha_shift_list = factoring(
            factor, number_characters, alpha_sequence_length)
        encrypted_list = shift_text(
            factor, printable_list, alpha_shift_list, alpha_sequence_length, '+')
        return ''.join(map(str, encrypted_list))
    except:
        raise ValueError("Invalid text input")


def decrypt_135(factor, text):
    try:
        int(factor)
    except:
        raise ValueError("Invalid key integer")
    if len(str(factor)) > 135:
        raise ValueError("Key Max Length Exceeded")
    factor = str(int(factor) + 2)
    if text == "":
        decrypted_list = ""
    try:
        alphabetical_sequence = generate_alpha_sequence(factor)
        alpha_sequence_length = len(alphabetical_sequence)
        number_characters = len(text)
        alpha_shift_list = factoring(
            factor, number_characters, alpha_sequence_length)
        decrypt_list = shift_text(
            factor, text, alpha_shift_list, alpha_sequence_length, '-')
        key = key_extract(decrypt_list)
        unprintable_list = special(key[1], '-', factor)
        restored_list = character_replace(unprintable_list, '-', factor)
        grouped_list = group(restored_list, key[0])
        untransposed_list = transpose(grouped_list)
        joined_list = join(untransposed_list)
        cleaned_list = remove(joined_list)
        decrypted_list = ''.join(cleaned_list)
        decode_string = decrypted_list.encode('utf-8')
        decoded_byte_string = base64.b64decode(decode_string)
        return decoded_byte_string.decode('utf-8')
    except:
        raise ValueError("Invalid text input")
