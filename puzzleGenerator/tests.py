from puzzleMaker import *
from WordsDatabaseGenerator import *

dictionaryFileAddress = "dictionary-en.txt"
frenchLexiconLink = "http://www.lexique.org/databases/Lexique382/Lexique382.tsv"
englishLexiconLink = "http://www.lexique.org/databases/SUBTLEX-US/SUBTLEXus74286wordstextversion.tsv"

dictionary = loadDictionary(dictionaryFileAddress)
frequencies = loadFrequency(englishLexiconLink, ['Word', 'SUBTLWF'])
words = loadLanguage(dictionary, frequencies)
addLanguageToDatabase("EN", words)
# insertPuzzle(generatePuzzle('L'), 'L')
# frenchDictionaryAll = loadDictionaryFR()
# frenchDictionaryABCDE = filterWords(frenchDictionaryAll, "ABCSE")
# print(frenchDictionaryABCDE)
# printDatabase()