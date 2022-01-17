'''Creation date: __/__/____'''

from math import pow
from re import search

# Define key character sets.
inCharSet = "".join([
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q",
    "r", "s", "t", "u", "v", "w", "x", "y", "z", ".", "'", "=", "!", "-", "+"])
outCharSet = "".join([
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "g",
    "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x",
    "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O",
    "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "+", "/", ",", "#", "$", "%",
    "&", "*", "(", ")", "^", "[", "]", ":", ";", '"', "<", "@", ">", "?", "!", "-", "`",
    ".", "_", "'", "{", "}"])

# Define sub character sets.
subSetOne = "".join([
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ',', '#', '$', '%', '&', '*', '(',
    ')', '^', '[', ']', ':', ';', '"', '<', '@', '>', '?', '/', '='])
subSetTwo = "".join([
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
    'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '=', '!', '-', '+'])


def inputSpaces(string: str, idxs=[]):
    match = search(" ", string)
    if match is None:
        return idxs
    lastMatch = idxs[-1] if len(idxs) > 0 else -1
    idx = match.regs[0][0]
    return inputSpaces(string[idx + 1:], idxs + [idx + lastMatch + 1])


def spaceDistance(spaceIndex):
    return list(map(lambda pos: pos[1]-pos[0], zip(spaceIndex[:-1], spaceIndex[1:])))


def spaceEncode(spaceList):
    numDigits = list(map(lambda pos: len(str(pos))-1, spaceList))
    zeroList = list(map(lambda pos: "0"*pos, numDigits))
    return "".join(list(map(lambda x, y: str(x) + str(y), zeroList, spaceList)))


def inputPosition(inputString, inputSet):
    return list(map(lambda char: inputSet.find(char), inputString))[::-1]


def convertDecimal(inputString, inBase, inputSet, inPosList):
    if inputSet == ["0123456789"]:
        return str(inputString)
    return sum(map(lambda pos: (inBase**pos[0])*pos[1], enumerate(inPosList)))


def inputDivmod(inputQuotient, outBase):
    remainderList = []
    while inputQuotient > 0:
        inputQuotient, remainder = divmod(inputQuotient, outBase)
        remainderList.append(remainder)
    return remainderList[::-1]


def outputPosition(intInString, outBase):
    return inputDivmod(int(intInString), outBase)


def subCharacters(outPosList, outputSet):
    return "".join(list(map(lambda pos: outputSet[pos], outPosList)))


def baseConvert(inputString, inBase, outBase, inputSet, outputSet):
    inPosList = inputPosition(inputString, inputSet)
    intInString = convertDecimal(inputString, inBase, inputSet, inPosList)
    outPosList = outputPosition(intInString, outBase)
    return subCharacters(outPosList, outputSet)


def inputShrink(inputString):
    spaceIndex = inputSpaces(inputString)
    spaceList = spaceIndex[:1] + spaceDistance(spaceIndex)
    spaceString = spaceEncode(spaceList)
    spaceShrink = baseConvert(spaceString, 10, 90, inCharSet, outCharSet)
    textList = inputString.replace(" ", "")
    return spaceShrink, textList


def inputExpand(inputString):
    pass

#print(inputShrink("hello world"))
