from collections import Counter
from random import choices
import sqlite3
import pandas as pd
from pandarallel import pandarallel

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
        c.execute(f"SELECT word, frequency FROM words WHERE length(word) <= ? and length(word) >= ? and language = ?",
                  (length, minlength, language)).fetchall(), columns=['word', 'frequency'])
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
    print(c.execute(f'SELECT * FROM puzzleWords').fetchall())
    conn.commit()
    conn.close()

def insertPuzzle(currentPuzzle: pd.DataFrame, puzzleLanguage:str, puzzleSize:tuple, database:str) -> None:
    """
    Inserts a new puzzle into the database
    @param currentPuzzle: dataframe containing the current puzzle
    @param puzzleLanguage: 2 characters (example: 'EN' or 'FR') representing the language of puzzle (usually first two letters of the language name)
    @param puzzleSize: tuple containing the x and y dimensions of the puzzle
    @param database: path to the database, equal to the name specified at the beginning of this python file by default
    @return: None
    """

    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute("INSERT INTO puzzles(language, Xdimension, Ydimension) VALUES (?, ?, ?)", (puzzleLanguage, puzzleSize[0], puzzleSize[1]))
    currentPuzzleID = c.execute('SELECT MAX(id) FROM puzzles').fetchone()[0]

    for _, row in currentPuzzle.iterrows():
        wordIndex = c.execute(f"SELECT ID FROM words WHERE word = ?", (row['word'],)).fetchone()[0] #Get index of the word from language database
        c.execute(f"INSERT INTO puzzleWords(puzzleId, wordId, is_vertical, Xcoord, Ycoord) VALUES (?, ?, ?, ?, ?)",
                  (currentPuzzleID, wordIndex, row['IS_VERTICAL'], row['x'], row['y'])) # insert word into puzzle database of appropriate language

    conn.commit()
    conn.close()

def generatePuzzle(size: tuple, availableWords:pd.DataFrame) -> pd.DataFrame:
    if availableWords.dropna(subset=['frequency']).size < 5:
        raise ValueError("Not enough words to generate a puzzle")

    puzzle = pd.DataFrame(columns=['word', 'is_vertical', 'x', 'y'])

    centerWord = availableWords.dropna(subset=['frequency']).sort_values(by='word', key=lambda x: x.str.len(), ascending=False).iloc[0]['word'] #Get the longest word that is common (freq is not NaN)
    print(centerWord)
    puzzle = pd.concat([puzzle, pd.DataFrame([{'word': centerWord, 'is_vertical': False, 'x': (size[0]-len(centerWord)) // 2, 'y': size[1] // 2}])], ignore_index=True) # add the center word to the puzzle at the center of the board
    return puzzle