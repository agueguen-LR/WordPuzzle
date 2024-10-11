
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


def filterWords(allWords, letters):
    """
    Filters the given set of words to contain only words containing the given letters
    @param allWords: set containing all the words of the language
    @param letters: list of letters that must be contained in the words
    @return: set containing all the words composed of only the given letters
    """
    filteredWords = set()
    for word in allWords:
        if set(word).issubset(letters):
            filteredWords.add(word)
    return filteredWords

frenchDictionaryAll = loadDictionary("French")
frenchDictionaryABCDE = filterWords(frenchDictionaryAll, ['A','B','C','D','E'])
print(frenchDictionaryABCDE)