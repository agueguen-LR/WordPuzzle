from collections import Counter

def loadDictionary(language):
    """
    Loads the dictionary for the given language
    @param language: string of the name of the language in lowercase
    @return: set containing all the words in the given dictionary
    """
    validWords = set()
    f = open("dico"+ language +".txt", 'r')
    for line in f:
        validWords.add(line.strip('\n'))
    return validWords


def filterWords(allWords, letters, length, minlength = 3):
    """
    Filters the given set of words to contain only words according to the given constraints
    @param allWords: set containing all the words of the language
    @param letters: list of letters that can be contained in the words in the appropriate quantity
    @param length: maximum length of the words
    @param minlength: minimum length of the words
    @return: set containing all the valid words
    """
    filteredWords = set()
    lettersCounter = Counter(letters)

    for word in allWords:
        #Optimisation: don't do further operations if word is too long
        if len(word) > length or len(word) < minlength:
            continue
        # Optimisation: don't do further operations if word isn't composed of correct letters using set operations
        if not set(word).issubset(letters):
            continue
        # Final check, word is composed of letters in the correct quantities
        if all(Counter(word)[char] <= lettersCounter[char] for char in Counter(word)) and len(word) <= length:
            filteredWords.add(word)
    return filteredWords

frenchDictionaryAll = loadDictionary("french")
frenchDictionaryABCDE = filterWords(frenchDictionaryAll, "BRAVERA", 5)
print(frenchDictionaryABCDE)