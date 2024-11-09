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

    puzzle = pd.DataFrame(columns=['wordID', 'word', 'is_vertical', 'x', 'y'])

    #first word of the puzzle is the longest frequent word and is placed in the center of the board
    centerWord = frequentWords.iloc[0]
    print(centerWord)
    frequentWords.drop(frequentWords.index[0], inplace=True) # Remove the center word from the list of frequent words

    print(frequentWords)
    puzzle = __add_word_to_puzzle(puzzle, centerWord['wordID'], centerWord['word'], False, (size[0]-len(centerWord)) // 2, (size[1]-1) // 2) # add the center word to the puzzle at the center of the board

    return puzzle

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