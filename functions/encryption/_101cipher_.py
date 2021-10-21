from random import randint, seed

def gen_shift_values(key:int, input_integer:str):
    ''' Returns: Generated list of integer shift values. '''
    input_list = [int(digit) for digit in input_integer]
    digit_count = len(input_list)
    shift_list = []
    for count in range(digit_count):
        seed(key * (count + 2))
        shift_list.append(randint(0,9))
    return shift_list, input_list, digit_count

def shift_integers(shift_list, input_list, digit_count:int, argument:str):
    ''' Returns: Input list shifted by shift values. '''
    output_list = []
    for digit in range(digit_count):
        if argument == "encrypt":
            output_list.append(str((input_list[digit] + shift_list[digit]) % 10))
        if argument == "decrypt":
            unshifted = input_list[digit] - shift_list[digit]
            if unshifted >= 0:
                output_list.append(str(unshifted))
            else:
                output_list.append(str(abs(unshifted + 10)))
    return "".join(output_list)

def encrypt_101(key:int, input_integer:str):
    ''' Returns: Input integer encrypted. '''
    shift_list, input_list, digit_count = gen_shift_values(key, input_integer)
    return shift_integers(shift_list, input_list, digit_count, "encrypt")

def decrypt_101(key:int, input_integer:str):
    ''' Returns: Input integer decrypted. '''
    shift_list, input_list, digit_count = gen_shift_values(key, input_integer)
    return shift_integers(shift_list, input_list, digit_count, "decrypt")
