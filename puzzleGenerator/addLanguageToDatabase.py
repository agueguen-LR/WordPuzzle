from WordsDatabaseGenerator import *

#Insert the name of the sqlite database here
SQLITE_DATABASE_NAME = "../Database/puzzles.db"

frenchDictionaryFileAddress = "dictionary-fr.txt" #file containing all valid words of the Scrabble dictionary, one per line
englishDictionaryFileAddress = "dictionary-en.txt"

frenchLexiconLink = "http://www.lexique.org/databases/Lexique382/Lexique382.tsv" #'ortho', 'freqfilms2', 'freqlivres'
englishLexiconLink = "http://www.lexique.org/databases/SUBTLEX-US/SUBTLEXus74286wordstextversion.tsv" #'Word', 'SUBTLWF'

def addFrenchToDatabase():
    dictionary = loadDictionary(frenchDictionaryFileAddress)
    frequencies = loadFrequency(frenchLexiconLink, ['ortho', 'freqfilms2', 'freqlivres'])
    words = loadLanguage(dictionary, frequencies)
    addLanguageToDatabase("french", words, SQLITE_DATABASE_NAME, "FR")

def addEnglishToDatabase():
    dictionary = loadDictionary(englishDictionaryFileAddress)
    frequencies = loadFrequency(englishLexiconLink, ['Word', 'SUBTLWF'])
    words = loadLanguage(dictionary, frequencies)
    addLanguageToDatabase("english", words, SQLITE_DATABASE_NAME, "EN")