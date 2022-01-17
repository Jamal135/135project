'''Creation date: 05/01/2021'''

from re import search
from math import pow

char_set = '''0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/~!@#$%^&*;=?<>[]:"{},`'''


def is_set(input_set):
    ''' Returns: Boolean about if Input Set is Unique or not. '''
    return len(input_set) == len(set(input_set))


def set_check(in_base, out_base, input_set, output_set):
    ''' Purpose: Tests if Input Set meet Requirements. '''
    if in_base > len(input_set) or out_base > len(output_set):
        raise ValueError("Custom set doesn't satisfy base")
    if search("[.-]", input_set + output_set) is not None:
        raise ValueError("Custom set contains - or .")


def value_check(in_base, out_base, in_cut_set, out_cut_set, char_set, frac_places):
    ''' Purpose: Test if Inputs Meet Requirements. '''
    if in_base < 2 or in_base > len(char_set):
        raise ValueError("Input base is out of range")
    if out_base < 2 or out_base > len(char_set):
        raise ValueError("Output base is out of range")
    if not is_set(in_cut_set):
        raise ValueError("Input set is not unique")
    if not is_set(out_cut_set):
        raise ValueError("Output set is not unique")
    if frac_places < 0:
        raise ValueError("Negative fractional places value")


def input_sign(in_string):
    ''' Returns: Input String with Sign Removed and Sign Boolean. '''
    return (in_string[1:], True) if in_string[0] == "-" else (in_string, False)


def input_position(abs_in_string, in_cut_set):
    ''' Returns: List of integer String Index Positions in Input Set. '''
    in_pos_list = list(
        map(lambda char: in_cut_set.find(char), abs_in_string))[::-1]
    if -1 in in_pos_list:
        raise ValueError("Input characters not in input set")
    return in_pos_list


def input_float_split(input_set, in_pos_list):
    ''' Returns: integer Value, and if Applicable Decimal integer and Float Boolean. '''
    if (len(input_set) - 1) in in_pos_list:
        int_pos_list = in_pos_list[in_pos_list.index(len(input_set)-1) + 1:]
        frac_pos_list = reversed(
            in_pos_list[:in_pos_list.index(len(input_set)-1)])
        return int_pos_list, frac_pos_list, True
    return in_pos_list, [], False


def convert_decimal(abs_in_string, in_base, in_cut_set, in_pos_list):
    ''' Returns: Decimal integer Representation of Input integer. '''
    if in_cut_set == ["0123456789."]:
        return str(abs_in_string)
    int_pos_list, frac_pos_list, float_input = input_float_split(
        in_cut_set, in_pos_list)
    int_list = map(lambda pos: (
        in_base**pos[0])*pos[1], enumerate(int_pos_list))
    if not float_input:
        return sum(int_list), False
    frac_list = map(lambda pos: (
        in_base**((pos[0]*-1)-1))*pos[1], enumerate(frac_pos_list))
    return str(sum(int_list) + sum(frac_list)), True


def input_divmod(input_quotient, out_base):
    ''' Returns: List of Remainder Values for Each Character Position Calculated. '''
    remainder_list = []
    while input_quotient > 0:
        input_quotient, remainder = divmod(input_quotient, out_base)
        remainder_list.append(remainder)
    return remainder_list[::-1]


def output_position(frac_in_string, out_base, frac_places):
    ''' Returns: Representation of integer in Selected Output Base. '''
    if "." in str(frac_in_string):
        input_quotient = float(frac_in_string) * pow(out_base, frac_places)
    else:
        input_quotient = int(frac_in_string)
    return input_divmod(input_quotient, out_base)


def sub_characters(out_pos_list, out_cut_set):
    ''' Returns: List of Output Set Characters at each Output Position Index. '''
    return "".join(list(map(lambda pos: out_cut_set[pos], out_pos_list)))


def output_format(string, frac_places, out_cut_set, frac_input, sign):
    ''' Returns: Output integer Correctly Formatted with Applicable Sign/Decimal. '''
    if frac_input and frac_places != 0:
        integer = string[:(frac_places*-1)]
        if not integer:
            frac_string = out_cut_set[0] + "." + string[(frac_places*-1):]
        else:
            frac_string = integer + "." + string[(frac_places*-1):]
    else:
        frac_string = string
    if sign:
        return "-" + frac_string
    return frac_string


def base_convert(input_string: str, in_base: str, out_base: str = "10",
                 input_set: str = char_set, output_set: str = char_set, frac_places: str = "5"):
    ''' Returns: Input String at Input Base Converted to Output Base Representation Using Provided Sets. '''
    try:
        in_base_int, out_base_int, frac_places_int = int(
            in_base), int(out_base), int(frac_places)
    except:
        raise ValueError("integer arguments contain non-integer values")
    set_check(in_base_int, out_base_int, input_set, output_set)
    in_cut_set = input_set[:in_base_int] + "."
    out_cut_set = output_set[:out_base_int] + "."
    value_check(in_base_int, out_base_int, in_cut_set,
                out_cut_set, char_set, frac_places_int)
    abs_in_string, sign = input_sign(input_string)
    in_pos_list = input_position(abs_in_string, in_cut_set)
    frac_in_string, frac_input = convert_decimal(
        abs_in_string, in_base_int, in_cut_set, in_pos_list)
    out_pos_list = output_position(
        frac_in_string, out_base_int, frac_places_int)
    output_string = sub_characters(out_pos_list, out_cut_set)
    return output_format(output_string, frac_places_int, out_cut_set, frac_input, sign)
