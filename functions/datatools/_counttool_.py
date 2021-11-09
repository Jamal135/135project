
# Tool to analyse and compare the frequency of each character in a data set.
# Creation date: 09/01/2021

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
    # Format Input with Respect to Case and Spaces Boolean Arguments.
    in_string, length = string_format(input_string, include_spaces, case_sensitive)
    # Create Set of all Unique Characters Contained in Input.
    char_set = list(set(in_string))
    # Count the Number of Occurrences of each Character in Character Set.
    count_list = list(map(lambda pos:in_string.count(pos), char_set))
    # Calculate Percentage of Total Input that is Each Character in Character Set.
    probability_list = list(map(lambda pos:round((int(pos)/length), 4), count_list))
    # Join Character, Count, and Percentage Lists into one Ordered List of Lists.
    char_dictionary = zip(char_set, count_list, probability_list)
    return sorted(char_dictionary, key = char_order, reverse = True)
