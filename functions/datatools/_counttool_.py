'''Creation date: 09/01/2021'''

def string_format(input_string, include_spaces, case_sensitive):
    ''' Returns: String with Spaces Optionally Removed and Capitals Optionally Lowered. '''
    if not include_spaces: space_string = input_string.replace(" ", "")
    else: space_string = input_string
    if case_sensitive: return space_string, len(space_string)
    return space_string.lower(), len(space_string)

def char_order(in_position):
    ''' Returns: Specified List Order. '''
    _, char_count, char_percent = in_position
    return char_count, char_percent

def count_analysis(input_string, include_spaces:bool = True, case_sensitive:bool = True):
    ''' Returns: List of Lists Containing Count and Percentage Share of all Characters. '''
    in_string, length = string_format(input_string, include_spaces, case_sensitive)
    char_set = list(set(in_string))
    count_list = list(map(lambda pos:in_string.count(pos), char_set))
    probability_list = list(map(lambda pos:round((int(pos)/length), 4), count_list))
    char_dictionary = zip(char_set, count_list, probability_list)
    return sorted(char_dictionary, key = char_order, reverse = True)
