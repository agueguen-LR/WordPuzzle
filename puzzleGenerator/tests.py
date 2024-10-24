from puzzleMaker import *
from WordsDatabaseGenerator import *

dictionaryFileAddress = "dictionary-fr.txt"
frenchLexiconLink = "http://www.lexique.org/databases/Lexique382/Lexique382.tsv"

dictionary = loadDictionary(dictionaryFileAddress)
frequencies = loadFrequency(frenchLexiconLink, ['ortho', 'freqfilms2', 'freqlivres'])
words = loadLanguage(dictionary, frequencies)
addLanguageToDatabase("FR", words)
# insertPuzzle(generatePuzzle('L'), 'L')
# frenchDictionaryAll = loadDictionaryFR()
# frenchDictionaryABCDE = filterWords(frenchDictionaryAll, "ABCSE")
# print(frenchDictionaryABCDE)
# printDatabase()