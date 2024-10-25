from collections import Counter
from random import choices
import sqlite3
import pandas as pd

#Insert the name of the sqlite database here
SQLITE_DATABASE_NAME = "puzzles.db"

# Authorized languages, prevents SQL injection, add more if needed
ALLOWED_LANGUAGES = frozenset({'EN', 'FR'})

#Dimensions of the large and the small puzzles
LDimensions = (13,6)
SDimensions = (6,7)

def loadDictionaryFR() -> set:
    """
    Loads the dictionary for the given language
    @return: set containing all the words in the given dictionary
    """
    validWords = set()
    f = open("dictionary-fr.txt", 'r')
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
    Generates a puzzle of the given size (usually 'S' or 'L')
    @param size: character (usually 'S' or 'L') representing the type of puzzle
    @return: pandas Dataframe containing the words, their direction and their starting coordinates
    """
    output = pd.DataFrame({'word': ["VACHE", "POULET"], 'IS_VERTICAL': [True, False], 'x': [3, 5], 'y':[4, 6]})
    return output

def printDatabase(puzzleLanguage:str, database:str = SQLITE_DATABASE_NAME) -> None:
    """
    prints out the puzzle and words database for testing purposes
    @return: None
    """
    if puzzleLanguage not in ALLOWED_LANGUAGES:
        raise ValueError(f"Invalid puzzle language: {puzzleLanguage}")

    conn = sqlite3.connect(database)
    c = conn.cursor()
    print(c.execute('SELECT * FROM puzzle').fetchall())
    tableName = f'puzzleWords{puzzleLanguage}'
    print(c.execute(f'SELECT * FROM {tableName}').fetchall())
    conn.commit()
    conn.close()

def insertPuzzle(currentPuzzle: pd.DataFrame, puzzleLanguage:str, puzzleSize:tuple, database:str = SQLITE_DATABASE_NAME) -> None:
    """
    Inserts a new puzzle into the database
    @param currentPuzzle: dataframe containing the current puzzle
    @param puzzleLanguage: 2 characters (example: 'EN' or 'FR') representing the language of puzzle (usually first two letters of the language name)
    @param puzzleSize: tuple containing the x and y dimensions of the puzzle
    @param database: path to the database, equal to the name specified at the beginning of this python file by default
    @return: None
    """
    if puzzleLanguage not in ALLOWED_LANGUAGES:
        raise ValueError(f"Invalid puzzle language: {puzzleLanguage}")

    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute("INSERT INTO puzzle(language, Xdimension, Ydimension) VALUES (?, ?, ?)", (puzzleLanguage, puzzleSize[0], puzzleSize[1]))
    tableName = f'puzzleWords{puzzleLanguage}'
    currentPuzzleID = c.execute('SELECT MAX(puzzleID) FROM puzzle').fetchone()[0]

    for _, row in currentPuzzle.iterrows():
        wordIndex = c.execute(f"SELECT ID FROM {puzzleLanguage} WHERE word = ?", (row['word'],)).fetchone()[0] #Get index of the word from language database

        c.execute(f"INSERT INTO {tableName}(puzzleID, word, is_vertical, Xcoord, Ycoord) VALUES (?, ?, ?, ?, ?)",
                  (currentPuzzleID, wordIndex, row['IS_VERTICAL'], row['x'], row['y'])) # insert word into puzzle database of appropriate language

    conn.commit()
    conn.close()
