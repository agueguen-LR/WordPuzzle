from collections import Counter
from random import choices
import sqlite3
import pandas as pd

Ldimensions = {'x':13, 'y':6}
Sdimensions = {'x':6, 'y':7}

def loadDictionaryFR() -> set:
    """
    Loads the dictionary for the given language
    @param language: string of the name of the language in lowercase
    @return: set containing all the words in the given dictionary
    """
    validWords = set()
    f = open("dicofrench.txt", 'r')
    for line in f:
        validWords.add(line.strip('\n'))
    return validWords

def generateLetters(amount: int, letterFrequency: list) -> list:
     return choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", weights = letterFrequency, k=amount)

def filterWords(allWords: set, letters: list, length=99, minlength = 3) -> set:
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
        if all(Counter(word)[char] <= lettersCounter[char] for char in Counter(word)):
            filteredWords.add(word)
    return filteredWords

def generatePuzzle(size: str) -> pd.DataFrame:
    """
    JUST TESTING FOR NOW
    @param size:
    @return:
    """
    output = pd.DataFrame({'word': ["VACHE", "POULET"], 'IS_VERTICAL': [True, False], 'x': [3, 5], 'y':[4, 6]})
    return output

def printDatabase():
    """
    JUST TESTING FOR NOW
    @return:
    """
    conn = sqlite3.connect('sqlite.db')
    c = conn.cursor()
    print(c.execute('SELECT * FROM puzzle').fetchall())
    print(c.execute('SELECT * FROM words').fetchall())

def insertPuzzle(currentPuzzle: pd.DataFrame, puzzleType: str):
    """
    JUST TESTING FOR NOW
    @param currentPuzzle:
    @param puzzleType:
    @return:
    """
    conn = sqlite3.connect("sqlite.db")
    c = conn.cursor()
    c.execute("INSERT INTO puzzle(puzzlesize) VALUES (?)", (puzzleType,))
    for _, row in currentPuzzle.iterrows():
        c.execute("""
                INSERT INTO words(puzzleID, word, IS_VERTICAL, x, y) 
                VALUES (?, ?, ?, ?, ?)
            """, (puzzleType, row['word'], row['IS_VERTICAL'], row['x'], row['y']))
    conn.commit()
    conn.close()

insertPuzzle(generatePuzzle('L'), 'L')
# frenchDictionaryAll = loadDictionaryFR()
# frenchDictionaryABCDE = filterWords(frenchDictionaryAll, "ABCSE")
# print(frenchDictionaryABCDE)
printDatabase()