
#135Code Encryption/Decryption Algorithm


#Required for alphabetical sequence generator.
import random
#Required for base64 encoding/decoding.
import base64
#Required for floor function
import math

#Use input to generate alphabetical sequence.
def generate_alpha_sequence(input):
    #List of all supported characters
    character_list = ['E', 'I', 'p', '7', '3', 'Q', 'V', 'A', '0', 'm', 'j', 'x', 'v', 'J', '9',
                     'H', 'M', 'F', 'f', 'T', 'n', 'D', 'S', '6', 'Y', 'k', '5', 'o', '/', 'U', 
                     'w', 'c', 'h', 'd', 'l', 'L', 'z', 'X', '+', 's', 'R', 'g', 'b', 'r', 'O', 
                     '1', 'B', 'e', 'P', 'y', 'a', 'C', 't', 'Z', 'K', 'W', 'i', 'N', '8', 'G', 
                     '=', 'u', '4', 'q', '2']
    length = len(character_list)
    #Generation of seeded alphabetical sequence using input.
    random.seed(input)
    alphabetical_sequence = (random.sample(character_list, length))
    return alphabetical_sequence

#Replace special characters in input text.
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
    replacements = random.sample(character_pool, k = number_characters)
    count = 0
    while count in range(length):
        selected_character = input_list[count]
        #Replace characters with symbol and character.
        if selected_character in characters and argument == '+':
            output_list.append('\a')
            position = characters.index(selected_character)
            output_list.append(replacements[position])
            count = count + 1
        #Remove symbol and character and return original character.
        elif selected_character == '\a' and argument == '-':
            selected_character = input_list[count + 1]
            position = replacements.index(selected_character)
            output_list.append(characters[position])
            count = count + 2
        #If selected character is not special, append selected character.
        else:
            output_list.append(selected_character)
            count = count + 1
    return output_list

#Convert Text input into suitable format.
def list_creation(input_text, argument):
    #Determine number groups and insert spaces.
    split_text = list(input_text)
    random.seed()
    #Random insert spaces.
    if argument == '+':
        number_groups = random.randint(3, 15)
        for _ in range(number_groups):
            position = random.randint(1, len(input_text) - 2)
            split_text.insert(position, " ")
    #Regular insert spaces.
    if argument == '-':
        number_groups = 2
        split = int((len(input_text)) / number_groups)
        split_text.insert(split, " ")
    grouped_text = ''.join(split_text)
    #Convert text to list of list of characters.
    list_groups = grouped_text.split(' ')
    output_list = list(map(list, list_groups))
    longest_word_length = len(max(list_groups, key=len))
    #Make all lists as long as longest word (list).
    for selected_word in output_list:
        if len(selected_word) < longest_word_length:
            difference = (longest_word_length - len(selected_word))
            for _ in range(difference):
                selected_word.append('\b')
    return output_list

#Join list of lists into one list.
def join(input_list):
    joined_lists = []
    for a_tuple in input_list:
            input_list[input_list.index(a_tuple)] = list(a_tuple)
    for a_list in input_list:
        joined_lists.append(''.join(a_list))
    output_list = list(' '.join(joined_lists))
    return output_list

#Turn expanded_list into list of lists containing each group of characters to be transposed.
def group(expanded_list, key):
    #Key is the end number that was extracted earlier.
    length = len(expanded_list)
    number_lists = int(length / key)
    output_list = []
    temporary_list = []
    #Use key to correct convert list into list of lists
    for count_lists in range(key):
        for count_characters in range(number_lists):
            position_in_list = (number_lists * count_lists) + count_characters
            temporary_list.append(expanded_list[position_in_list])
        output_list.append(temporary_list)
        temporary_list = []
    return output_list

#Transpose encode_list and return transpose_list.
def transpose(input_list):
    output_list = (list(zip(*input_list)))
    return output_list

#Flatten input list of lists into list.
def flatten(input_list):
    output_list = []
    for sublist in input_list:
        for val in sublist:
            output_list.append(val)
    output_list.append('\a')
    return output_list

#Define calculation function for use in factoring function.
def calculation(factor, alpha_sequence_length, val):
    try: calculation = int((val * factor) + (((val * (factor + 1)) / alpha_sequence_length)) - (((val * 13.5) / ((val + 1) / 6))))
    except: calculation = int((val * factor) + (((val * (factor + 1)) / alpha_sequence_length)))
    return calculation

#Calculate shift value for every character (number_characters).
def factoring(factor, number_characters, alpha_sequence_length):
    primary_factor = int(factor)
    secondary_factor = primary_factor / 4
    previous_output = 135
    shifting_list = []
    #Calculation
    for count in range(number_characters):
        #Complete calculations
        primary_calculation = calculation(primary_factor, alpha_sequence_length, count + 1)
        inverse_count = ((count - 1) % number_characters) + 1
        secondary_calculation = calculation(secondary_factor, alpha_sequence_length, inverse_count)
        combined_calculation = primary_calculation - secondary_calculation
        if combined_calculation == 0:
            combined_calculation = 1
        output_calculation = int(calculation(primary_factor, alpha_sequence_length, combined_calculation))
        #Take parts of output calculation.
        magic_a = int(str(output_calculation)[-9:])
        magic_b = int(str(output_calculation)[:8])
        magic_c = ((magic_a * magic_b) + (primary_factor^2))
        magic_output = int(str(magic_c)[-9:])
        #Add previous output number to current value.
        combined_output = magic_output + previous_output
        #Find remainder.
        final_output =  combined_output % alpha_sequence_length
        #Obscure potential even/odd patterns.
        if count % 2 == 0:
            final_output = final_output + 1
        #Create output list.
        shifting_list.append(final_output)
        previous_output = final_output 
    return shifting_list

#Shift input correctly with respect to argument (direction) and modifier (order).
def shift(factor, input_list, alpha_shift_list, alpha_sequence_length, argument, modifier):
    output_list = []
    length = len(input_list)
    shiftdirection = {'+' : 1, '-' : -1}
    old_character_position = 135
    base_sequence = generate_alpha_sequence(factor)
    if modifier == 1:
        length = length - 1
        shift = base_sequence.index(input_list[length])
    for count in range(length):
        #Generate applicable alphabetical sequence for each character.
        alphakey = ((int(factor) + (modifier * 135)) * (count + 1))
        alphabetical_sequence = generate_alpha_sequence(alphakey)
        current_character = input_list[count]
        character_position = alphabetical_sequence.index(current_character)
        if modifier == 0:
            shift = alpha_shift_list[count]
        #Find new position by adding/subtracting shift value with respect to argument.
        new_character_position = ((character_position + (shiftdirection[argument] * shift)) + (shiftdirection[argument] * old_character_position)) % alpha_sequence_length
        new_character = alphabetical_sequence[new_character_position]
        #Update old character position value.
        if argument == '+':
            old_character_position = base_sequence.index(new_character)
        if argument == '-':
            old_character_position = base_sequence.index(current_character)
        output_list.append(new_character)
    if modifier == 1:
        output_list.append(input_list[length])
    return(output_list)

#Shift input text by calling shift function with respect to argument and order.
def shift_text(factor, input_list, alpha_shift_list, alpha_sequence_length, argument):
    if argument == '+':
        shift_list = shift(factor, input_list, alpha_shift_list, alpha_sequence_length, '+', 0)
        output_list = shift(factor, shift_list, alpha_shift_list, alpha_sequence_length, '+', 1)
    if argument == '-':
        shift_list = shift(factor, input_list, alpha_shift_list, alpha_sequence_length, '-', 1)
        output_list = shift(factor, shift_list, alpha_shift_list, alpha_sequence_length, '-', 0)
    return(output_list)

#Calculate minor key.
def key_insert(encode_list):
    key = (len(encode_list))
    key = list(str(key))
    length = (len(key))
    key_out = ['=']
    #Turn key into list of numbers.
    for val in range(length):
        key_out.append(key[val])
    return key_out

#Extract minor key from ciphertext.
def key_extract(decode_list):
    key = []
    length = (len(decode_list)) - 1 
    character_type = True
    #Append key from end of ciphertext.
    while character_type is True:
        character_input = decode_list[length]
        character_type = character_input.isdigit()
        if character_type is True:
            key.append(str(character_input))
        length = length - 1
    key = list(reversed(key))
    #Format key correctly.
    length = len(key)
    decode_list = decode_list[:-(length + 2)]
    key = int(''.join(map(str,key)))
    return key, decode_list

#Remove all _'s from input list.
def remove(input_list):
    length = len(input_list)
    output_list = []
    for character_position in range(length):
        current_character = input_list[character_position]
        if current_character == '\b':
            current_character = ''  
        output_list.append(current_character)
    return output_list

#Replace special characters in list.
def special(input_list, argument, factor):
    character_pool = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] 
    random.seed(factor)
    replacements = random.sample(character_pool, k = 4)
    #Replace special characters with double characters.
    if argument == '+':
        output_list = []
        previous_character = ''
        for current_character in input_list:
            if current_character == '\b':
                if previous_character != replacements[0]:
                    output_list.extend([replacements[0]])
                else:
                    output_list.extend([replacements[1]])
            elif current_character == '\a':
                if previous_character != replacements[2]:
                    output_list.extend([replacements[2]])
                else:
                    output_list.extend([replacements[3]])
            else:
                output_list.append(current_character)
            previous_character = current_character
    #Replace character double ups with special characters.
    if argument == '-':
        output_list = []
        for count in range(len(input_list)):
            if input_list[count] in replacements[0:2]:
                output_list.append('\b')
            elif input_list[count] in replacements[2:4]:
                output_list.append('\a')
            else:
                output_list.append(input_list[count])
    return output_list

#Encoding Function - Text in - Code out:
def encrypt_135(factor, text, argument = '-'):
    try:
        int(factor)
    except:
        raise ValueError(f"Invalid key integer {factor}")
    if len(str(factor)) > 135:
        raise ValueError("Key Max Length Exceeded")
    #Fix key values 0 and 1 not working.
    factor = str(int(factor) + 2)
    try:        
        #Encode compressed text into Base64.
        encode_string = text.encode('utf-8')
        encoded_byte_string = base64.b64encode(encode_string)
        encoded_string = encoded_byte_string.decode('utf-8')
        #Generate alphabetical sequence using key.
        alphabetical_sequence = generate_alpha_sequence(factor)
        alpha_sequence_length = len(alphabetical_sequence)
        #Create and format list for encode_string ready for Encrypting.
        encrypt_list = list_creation(encoded_string, argument)
        #Calculate and set length of all lists in list to be equal.
        transpose_list = transpose(encrypt_list)
        #Flatten transpose list of lists into list.
        flattened_list = flatten(transpose_list)
        #Replace numbers in flattened list.
        replaced_list = character_replace(flattened_list, '+', factor)
        #Add minor length key to consolidated_list for decoding purposes.
        key_store = key_insert(encrypt_list[0])
        #Attach minor key to text ready for encryption.
        replaced_list.extend(key_store)
        #Turn special characters into printable text.
        printable_list = special(replaced_list, '+', factor)
        #Use factor key to calculate unique list of shifting values for each character in consolidated_list.
        number_characters = len(printable_list)
        alpha_shift_list = factoring(factor, number_characters, alpha_sequence_length)
        #Utilise calculated shifting_list to shift consolidated_list with respect to alphabetical_sequence.
        encrypted_list = shift_text(factor, printable_list, alpha_shift_list, alpha_sequence_length, '+')
        #Join list into one complete string.
        encrypted_list = ''.join(map(str, encrypted_list))
    except:
        raise ValueError("Invalid text input")
    #Return encrypted text output.
    return encrypted_list

#Decode Function - Code in - Text out:
def decrypt_135(factor, text):
    try:
        int(factor)
    except:
        raise ValueError("Invalid key integer")
    if len(str(factor)) > 135:
        raise ValueError("Key Max Length Exceeded")
    #Fix key values 0 and 1 not working.
    factor = str(int(factor) + 2)
    #Skip if entry is empty.
    if text == "":
        decrypted_list = ""
    try:
        #Generate alphabetical sequence using key.
        alphabetical_sequence = generate_alpha_sequence(factor)
        alpha_sequence_length = len(alphabetical_sequence)
        #Use factor key to calculate unique list of shifting values for each character in encoded input.
        number_characters = len(text)
        alpha_shift_list = factoring(factor, number_characters, alpha_sequence_length)
        #Unshift text input using calculated alpha_shift_list with reference to alphabetical_sequence.
        decrypt_list = shift_text(factor, text, alpha_shift_list, alpha_sequence_length, '-')
        #Extract minor key from end of decrypt_list for later decoding and remove key from decrypt_list.
        key = key_extract(decrypt_list)
        #Insert special non-printable characters.
        unprintable_list = special(key[1], '-', factor)
        #Insert numbers from original text that have been replaced back in.
        restored_list = character_replace(unprintable_list, '-', factor)
        #Divide expanded_list into appropriate list of lists.
        grouped_list = group(restored_list, key[0])
        #Transpose expand_list to reveal the original text in encoded input.
        untransposed_list = transpose(grouped_list)
        #Join untransposed_list of lists into joined_list. 
        joined_list = join(untransposed_list)
        #Remove all '_'s from the joined_list to produce the final decoded output.
        cleaned_list = remove(joined_list)
        #Consolidate decrypted list into one string.
        decrypted_list = ''.join(cleaned_list)
        #Decode output from Base64 to plain text.
        decode_string = decrypted_list.encode('utf-8')
        decoded_byte_string = base64.b64decode(decode_string)
        decoded_string = decoded_byte_string.decode('utf-8')
    except:
        raise ValueError("Invalid text input")
    #Return decrypted text output.
    return decoded_string
