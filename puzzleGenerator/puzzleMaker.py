from collections import Counter
from random import choices
import sqlite3
import numpy as np
import pandas as pd
from pandarallel import pandarallel
from re import finditer

pandarallel.initialize(progress_bar=False, verbose=0)

#Dimensions of the large and the small puzzles
LDimensions = (13,6)
SDimensions = (6,7)

def generateLetters(amount: int, letterFrequency: dict) -> list:
    """
    Generates a list of random letters based on the given frequency
    @param amount: amount of letters to generate
    @param letterFrequency: list of floats representing the frequency of each letter in the alphabet
    @return: list of letters
    """
    return choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", weights=list(letterFrequency.values()), k=amount)

def loadAndFilterWords(database: str, language: str, letters: list, length=99, minlength=3) -> pd.DataFrame:
    """
    Loads and filters words from the SQLite database for the given language and constraints.
    @param database: path to the SQLite database
    @param language: 2 characters representing the language of the words (e.g., 'EN' or 'FR')
    @param letters: list of letters that can be contained in the words in the appropriate quantity
    @param length: maximum length of the words
    @param minlength: minimum length of the words
    @return: set containing all the valid words
    """

    conn = sqlite3.connect(database)
    c = conn.cursor()

    # Fetch all words from the language table within the given length constraints
    allWords = pd.DataFrame(
        c.execute("SELECT id, word, frequency FROM words WHERE length(word) <= ? and length(word) >= ? and language = ?",
                  (length, minlength, language)).fetchall(), columns=['wordID', 'word', 'frequency'])
    conn.commit()
    conn.close()

    lettersCounter = Counter(letters)

    def is_valid_word(word):
        word_counter = Counter(word)
        return all(word_counter[char] <= lettersCounter[char] for char in word_counter)

    filteredWords = allWords[allWords['word'].parallel_apply(is_valid_word)]

    return filteredWords

def printDatabase(puzzleLanguage:str, database:str) -> None:
    """
    prints out the puzzle and words database for testing purposes
    @return: None
    """
    conn = sqlite3.connect(database)
    c = conn.cursor()
    print(c.execute('SELECT * FROM puzzles').fetchall())
    print(c.execute('SELECT * FROM puzzleWords').fetchall())
    conn.commit()
    conn.close()

def insertPuzzle(currentPuzzle: pd.DataFrame, puzzleLanguage:str, puzzleSize:tuple, database:str, letters:str) -> None:
    """
    Inserts a new puzzle into the database
    @param currentPuzzle: dataframe containing the current puzzle
    @param puzzleLanguage: 2 characters (example: 'EN' or 'FR') representing the language of puzzle (usually first two letters of the language name)
    @param puzzleSize: tuple containing the x and y dimensions of the puzzle
    @param database: path to the database, equal to the name specified at the beginning of this python file by default
    @param letters: string containing the letters used to generate the puzzle
    @return: None
    """
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute("INSERT INTO puzzles(language, Xdimension, Ydimension, letters) VALUES (?, ?, ?, ?)", (puzzleLanguage, puzzleSize[0], puzzleSize[1], letters))
    currentPuzzleID = c.execute('SELECT MAX(id) FROM puzzles').fetchone()[0]

    for _, row in currentPuzzle.iterrows():
        wordIndex = c.execute("SELECT ID FROM words WHERE word = ? and language = ?", (row['word'], puzzleLanguage)).fetchone()[0] #Get index of the word from language database
        c.execute("INSERT INTO puzzleWords(puzzleId, wordId, is_vertical, Xcoord, Ycoord) VALUES (?, ?, ?, ?, ?)",
                  (currentPuzzleID, wordIndex, row['IS_VERTICAL'], row['x'], row['y'])) # insert word into puzzle database of appropriate language

    conn.commit()
    conn.close()

def generatePuzzle(size: tuple, availableWords:pd.DataFrame, minimumWordCount: int = 5) -> pd.DataFrame:
    """
    Generates a puzzle with the given size and available words
    @param size: tuple of the x and y dimensions of the puzzle
    @param availableWords: Dataframe containing the available words and their frequency (from loadAndFilterWords)
    @param minimumWordCount: minimum amount of words with frequency>0 to generate a puzzle
    @return: Dataframe containing the generated puzzle
    """
    frequentWords = ((availableWords.dropna(subset=['frequency']) #Remove words with NaN frequency
                                    .sort_values(by='frequency', ascending=False)) #Sort by descending frequency
                                    .sort_values(by='word', key=lambda x: x.str.len(), ascending=False, kind='mergesort')) #Sort by descending word length while keeping the frequency order

    print(frequentWords)

    if frequentWords.shape[0] < minimumWordCount:
        raise ValueError("Not enough words to generate a puzzle")

    newPuzzle = pd.DataFrame(columns=['wordID', 'word', 'is_vertical', 'x', 'y'])
    occupiedArraySpaces = np.array([[0 for _ in range(size[1])] for _ in range(size[0])])
    print(occupiedArraySpaces.T)

    #first word of the puzzle is the longest frequent word and is placed in the center of the board
    centerWord = frequentWords.iloc[0]
    frequentWords.drop(frequentWords.index[0], inplace=True) # Remove the center word from the list of frequent words

    newPuzzle = __add_word_to_puzzle(newPuzzle, centerWord['wordID'], centerWord['word'], False, (size[0]-len(centerWord)) // 2, (size[1]-1) // 2) # add the center word to the puzzle at the center of the board
    print(newPuzzle)
    occupiedArraySpaces = __update_occupied_spaces(occupiedArraySpaces, centerWord['word'], (size[0]-len(centerWord)) // 2, (size[1]-1) // 2, False) # update the occupied spaces of the puzzle
    print(occupiedArraySpaces.T)

    return newPuzzle

def __add_word_to_puzzle(puzzle: pd.DataFrame, wordID: int, word: str, is_vertical: bool, x: int, y: int) -> pd.DataFrame:
    """
    Reminder: the double underscore indicates this function is private and should not be called from outside the module
    Adds a word to the puzzle
    @param puzzle: dataframe containing the current puzzle
    @param wordID: id of the word in the words database
    @param word: word to add
    @param is_vertical: boolean indicating if the word is vertical
    @param x: x coordinate of the word
    @param y: y coordinate of the word
    @return: updated puzzle
    """
    return pd.concat([puzzle, pd.DataFrame([{'wordID': wordID, 'word': word, 'is_vertical': is_vertical, 'x': x, 'y': y}])], ignore_index=True)

def __update_occupied_spaces(occupiedSpaces: np.ndarray, word: str, x: int, y: int, is_vertical: bool) -> np.ndarray:
    """
    Reminder: the double underscore indicates this function is private and should not be called from outside the module
    Updates the occupied spaces of the puzzle
    @param occupiedSpaces: numpy array containing the occupied spaces of the puzzle
    @param word: word to add
    @param x: x coordinate of the word
    @param y: y coordinate of the word
    @param is_vertical: boolean indicating if the word is vertical
    @return: updated occupied spaces
    """
    if is_vertical:
        for i in range(len(word)):
            occupiedSpaces[x, y+i] = 1
    else:
        print(occupiedSpaces.shape)
        for i in range(len(word)):
            occupiedSpaces[x+i, y] = 1

    return occupiedSpaces

def __word_can_be_placed(word: str, intersectionTuple: tuple, occupiedSpaces: np.ndarray, puzzleDimensions: tuple) -> bool:
    """
    Reminder: the double underscore indicates this function is private and should not be called from outside the module
    Checks if a word can be placed in given position on the puzzle
    !! No side words allowed in this version !!
    @param word: word to place
    @param intersectionTuple: Main tuple of the generation algorithm, should contain: (x, y, go_vertical_bool, letter)
    @param occupiedSpaces: numpy array containing the occupied spaces of the puzzle as 1, unoccupied as 0
    @param puzzleDimensions: tuple containing the x and y dimensions of the puzzle
    @return: boolean indicating if the word can be placed
    """
    if intersectionTuple[3] not in word: #If the intersection letter is not in the word we wish to place, return False
        return False

    letterIndexes = [m.start() for m in finditer(intersectionTuple[3], word)] #Get all indexes of the intersection letter in the word

    for index in letterIndexes: #for all theoretical placements of the word
        if intersectionTuple[2]: #Tests for vertical placement
            if intersectionTuple[1] - index < 0 or intersectionTuple[1] + (len(word)-1)-index >= puzzleDimensions[1]: #If the word goes out of bounds
                continue



        else: #Tests for horizontal placement
            if intersectionTuple[0] - index < 0 or intersectionTuple[0] + (len(word)-1)-index >= puzzleDimensions[0]: #If the word goes out of bounds
                continue

        return True



    return True