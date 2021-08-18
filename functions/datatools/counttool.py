
# Tool to analyse and compare the frequency of each character in a data set.
# Creation date: 09/01/2021

# 135code.com API Category Definition.
category = "tools"

# Function: string_format
def string_format(input_string, exclude_spaces, case_sensitive):
    ''' Returns: String with Spaces Optionally Removed and Capitals Optionally Lowered. '''
    if exclude_spaces: space_string = input_string.replace(" ", "")
    else: space_string = input_string
    if case_sensitive: return space_string, len(space_string)
    return space_string.lower(), len(space_string)

# Function: char_order
# in_position: Variable that Equals the Desired Order of List Values.
def char_order(in_position):
    ''' Returns: Specified List Order. '''
    _, char_count, char_percent = in_position
    return char_count, char_percent

# Function: API_char_analysis
# exclude_spaces: Boolean for if Spaces should be Counted.
# case_sensitive: Boolean for if Capital and Lower Case Characters Should be Seperate.
def API_char_analysis(input_string, exclude_spaces:bool = True, case_sensitive:bool = True):
    ''' Returns: List of Lists Containing Count and Percentage Share of all Characters. '''
    # Format Input with Respect to Case and Spaces Boolean Arguments.
    in_string, length = string_format(input_string, exclude_spaces, case_sensitive)
    # Create Set of all Unique Characters Contained in Input.
    char_set = list(set(in_string))
    # Count the Number of Occurrences of each Character in Character Set.
    count_list = list(map(lambda pos:in_string.count(pos), char_set))
    # Calculate Percentage of Total Input that is Each Character in Character Set.
    percent_list = list(map(lambda pos:round((int(pos)/length)*100, 3), count_list))
    # Join Character, Count, and Percentage Lists into one Ordered List of Lists.
    char_dictionary = zip(char_set, count_list, percent_list)
    return sorted(char_dictionary, key = char_order, reverse = True)
