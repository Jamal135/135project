
def split_input(text):
    ''' Returns: List of words padded to fixed length. '''
    word_list = text.split()
    max_length = len(max(word_list, key=len))
    for point in range(len(word_list)):
        word_list[point] = word_list[point] + "*" * \
            (max_length - len(word_list[point]))
    return word_list

def reverse_element(word_list, iterator: int):
    ''' Returns: List with every x element reversed. '''
    point = 1
    while point in range(len(word_list)):
        word_list[point] = (word_list[point])[::-1]
        point = point + iterator
    return word_list

def transpose(word_list):
    ''' Returns: Every string in list transposed. '''
    transposed_tuples = list(zip(*word_list))
    return ["".join(transposed_tuple) for transposed_tuple in transposed_tuples]

def encrypt_127(text):
    ''' Returns: Input text encrypted. '''
    word_list = split_input(text)
    adjusted_list = reverse_element(word_list, 2)
    transposed_list = transpose(adjusted_list)
    transposed_string = "".join(transposed_list)
    return(transposed_string)

test = "hello world I am testing that this hopefully works nicely for me so that I can be happy and not so tired"
print(encrypt_127(test))
