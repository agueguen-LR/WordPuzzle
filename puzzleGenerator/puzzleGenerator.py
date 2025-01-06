from collections import Counter
from random import choices, choice
import sqlite3
import numpy as np
import pandas as pd
from pandarallel import pandarallel
from re import finditer

pandarallel.initialize(progress_bar=False, verbose=0)

#Frequency tables for the English and French languages
frequenciesEN = {
        'A': 8.167, 'B': 1.492, 'C': 2.782, 'D': 4.253, 'E': 12.702, 'F': 2.228, 'G': 2.015, 'H': 6.094,
        'I': 6.966, 'J': 0.153, 'K': 0.772, 'L': 4.025, 'M': 2.406, 'N': 6.749, 'O': 7.507, 'P': 1.929,
        'Q': 0.095, 'R': 5.987, 'S': 6.327, 'T': 9.056, 'U': 2.758, 'V': 0.978, 'W': 2.360, 'X': 0.150,
        'Y': 1.974, 'Z': 0.074
    }
frequenciesFR = {
        'A': 7.636, 'B': 0.901, 'C': 3.260, 'D': 3.669, 'E': 14.715, 'F': 1.066, 'G': 0.866, 'H': 0.737,
        'I': 7.529, 'J': 0.613, 'K': 0.049, 'L': 5.456, 'M': 2.968, 'N': 7.095, 'O': 5.796, 'P': 2.521,
        'Q': 1.362, 'R': 6.693, 'S': 7.948, 'T': 7.244, 'U': 6.311, 'V': 1.838, 'W': 0.074, 'X': 0.427,
        'Y': 0.128, 'Z': 0.326
    }

def generateLetters(amount: int, letterFrequency: dict) -> list:
    """
    Generates a list of random letters based on the given frequency
    @param amount: amount of letters to generate
    @param letterFrequency: list of floats representing the frequency of each letter in the alphabet
    @return: list of letters
    """
    return choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", weights=list(letterFrequency.values()), k=amount)

def load_words(database: str, language: str, length=99, minlength=3) -> pd.DataFrame:
    """
    Loads words from the SQLite database for the given language and length constraints.
    @param database: path to the SQLite database
    @param language: 2 characters representing the language of the words (e.g., 'EN' or 'FR')
    @param length: maximum length of the words
    @param minlength: minimum length of the words
    @return: DataFrame containing all the words
    """
    conn = sqlite3.connect(database)
    c = conn.cursor()

    # Fetch all words from the language table within the given length constraints
    allWords = pd.DataFrame(
        c.execute("SELECT id, word, frequency FROM words WHERE length(word) <= ? and length(word) >= ? and language = ?",
                  (length, minlength, language)).fetchall(), columns=['wordID', 'word', 'frequency'])
    conn.commit()
    conn.close()

    return allWords

def filter_words(allWords: pd.DataFrame, letters: list) -> pd.DataFrame:
    """
    Filters the loaded words to contain only the given letters, in the given quantity
    (only words with two 'E's if there are two 'E's in the letters list, for example)
    @param allWords: DataFrame containing all the words
    @param letters: list of letters that can be contained in the words in the appropriate quantity
    @return: DataFrame containing the filtered words
    """
    lettersCounter = Counter(letters)

    def is_valid_word(word):
        word_counter = Counter(word)
        return all(word_counter[char] <= lettersCounter[char] for char in word_counter)

    filteredWords = allWords[allWords['word'].parallel_apply(is_valid_word)]

    return filteredWords

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
        c.execute("INSERT INTO puzzleWords(puzzleId, wordId, is_vertical, Xcoord, Ycoord) VALUES (?, ?, ?, ?, ?)",
                  (currentPuzzleID, row['wordID'], row['is_vertical'], row['x'], row['y'])) # insert word into puzzle database of appropriate language

    conn.commit()
    conn.close()

#Extreme rare case, could generate the exact same puzzle twice
#so unlikely that it shouldn't be a problem with the randomness of generateLetters and of attemptTuple
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

    # print(frequentWords)

    if frequentWords.shape[0] < minimumWordCount:
        raise ValueError("Not enough words to generate a puzzle")

    newPuzzle = pd.DataFrame(columns=['wordID', 'word', 'is_vertical', 'x', 'y'])
    occupiedArraySpaces = np.zeros(size, dtype=int)

    #first word of the puzzle is the longest frequent word and is placed in the center of the board
    centerWord = frequentWords.iloc[0]
    frequentWords.drop(frequentWords.index[0], inplace=True) # Remove the center word from the list of frequent words

    newPuzzle = __add_word_to_puzzle(newPuzzle, centerWord['wordID'], centerWord['word'],
                                     (size[0] - len(centerWord['word'])) // 2, (size[1] - 1) // 2,
                                     False)  # add the center word to the puzzle at the center of the board

    occupiedArraySpaces = __update_occupied_spaces(occupiedArraySpaces, centerWord['word'], (size[0]-len(centerWord['word'])) // 2, (size[1]-1) // 2, False) # update the occupied spaces of the puzzle

    potentialNewWordTuples = []
    potentialNewWordTuples = __update_potential_words_list(potentialNewWordTuples, (size[0]-len(centerWord['word'])) // 2, centerWord['word'], (-1, (size[1]-1) // 2, False)) # Add the potential new words to the list

    # main generation loop
    while len(potentialNewWordTuples) > 0:
        attemptTuple = choice(potentialNewWordTuples) # Choose a random tuple from the list of potential new words positions
        for(_, word) in frequentWords.iterrows():
            wordIndex = __word_can_be_placed(word['word'], attemptTuple, occupiedArraySpaces, size) # Check if the word can be placed

            if wordIndex != -1: # The word can be placed
                coordsOfNewWord = (attemptTuple[0], wordIndex) if attemptTuple[2] else (wordIndex, attemptTuple[1]) # Calculate the coordinates of the new word
                newPuzzle = __add_word_to_puzzle(newPuzzle, word['wordID'], word['word'], coordsOfNewWord[0], coordsOfNewWord[1], attemptTuple[2])  # Add the new word to the puzzle
                occupiedArraySpaces = __update_occupied_spaces(occupiedArraySpaces, word['word'], coordsOfNewWord[0], coordsOfNewWord[1], attemptTuple[2]) # Update the occupied spaces of the puzzle
                potentialNewWordTuples = __update_potential_words_list(potentialNewWordTuples, wordIndex, word['word'], attemptTuple)  # Update the list of potential new words
                frequentWords.drop(word.name, inplace=True)  # Remove the current word from frequentWords
                break # Break the loop as a word has been placed, we will now choose a new position for the next word

        potentialNewWordTuples.remove(attemptTuple) # Remove the tuple from the list of potential new words as it has been used

    return newPuzzle

def generateNewPuzzlesIntoDatabase(amountOfPuzzlesToGenerate: int, database: str, dimensions: tuple, language: str, amountOfLetters: int, frequencyTable: dict) -> None:
    """
    Generates a given amount of puzzles and inserts them into the database
    @param amountOfPuzzlesToGenerate: amount of puzzles to generate
    @param database: path to the SQLite database
    @param dimensions: dimensions of the puzzles to generate (x, y)
    @param language: language of the puzzles to generate (e.g., 'EN' or 'FR')
    @param amountOfLetters: amount of letters the puzzles will contain (e.g., 6)
    @param frequencyTable: frequency table of the letters in the language the puzzles will be generated in, refer to the tables in the puzzleGenerator.py file
    @return: None
    """
    puzzlesGenerated = 0
    allWords = load_words(database, language, amountOfLetters, 3)
    while puzzlesGenerated != amountOfPuzzlesToGenerate:
        try:
            letters = generateLetters(amountOfLetters, frequencyTable)
            filteredWords = filter_words(allWords, letters)
            newPuzzle = generatePuzzle(dimensions, filteredWords)
            insertPuzzle(newPuzzle, language, dimensions, database, ''.join(letters))
            puzzlesGenerated += 1
        except ValueError:
            continue
    return

def __add_word_to_puzzle(puzzle: pd.DataFrame, wordID: int, word: str, x: int, y: int, is_vertical: bool) -> pd.DataFrame:
    """
    Reminder: the double underscore indicates this function is private and should not be called from outside the module
    Adds a word to the puzzle
    @param puzzle: dataframe containing the current puzzle
    @param wordID: id of the word in the words database
    @param word: word to add
    @param x: x coordinate of the word
    @param y: y coordinate of the word
    @param is_vertical: boolean indicating if the word is vertical
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
        for i in range(len(word)):
            occupiedSpaces[x+i, y] = 1

    return occupiedSpaces

#Doesn't allow Intersections for now
def __word_can_be_placed(word: str, intersectionTuple: tuple, occupiedSpaces: np.ndarray, puzzleDimensions: tuple) -> int:
    """
    Reminder: the double underscore indicates this function is private and should not be called from outside the module
    Checks if a word can be placed in given position on the puzzle
    !! No side words allowed in this version !!
    @param word: word to place
    @param intersectionTuple: Main tuple of the generation algorithm, should contain: (x, y, go_vertical_bool, intersection_letter)
    @param occupiedSpaces: numpy array containing the occupied spaces of the puzzle as 1, unoccupied as 0
    @param puzzleDimensions: tuple containing the x and y dimensions of the puzzle
    @return: index of the first letter of the word if it can be placed, -1 otherwise (x or y depending on the direction the word is trying to be placed)
    """
    if intersectionTuple[3] not in word: #If the intersection letter is not in the word we wish to place, return -1
        return -1

    letterIndexes = [m.start() for m in finditer(intersectionTuple[3], word)] #Get all indexes of the intersection letter in the word
    adjacentFlag = False

    for index in letterIndexes: #for all theoretical placements of the word
        if intersectionTuple[2]: #Tests for vertical placement
            startOfWord = intersectionTuple[1] - index
            endOfWord = intersectionTuple[1] + (len(word)-1)-index

            if startOfWord < 0 or endOfWord >= puzzleDimensions[1]: #If the word goes out of bounds
                continue

            for i in range(startOfWord, endOfWord+1):
                if i == intersectionTuple[1]: #Skip the intersection letter
                    continue
                #This uses Python's short-circuit evaluation: if the first condition is true, the second condition is not evaluated, avoiding an index out of bounds error
                #This also uses 1 as True for the second condition as it is a numpy array containing 1s and 0s
                if intersectionTuple[0]+1 < puzzleDimensions[0] and occupiedSpaces[intersectionTuple[0]+1, i]: # Check if there are any adjacent words to the right
                    adjacentFlag = True
                    break
                if intersectionTuple[0]-1 >= 0 and occupiedSpaces[intersectionTuple[0]-1, i]: # Check if there are any adjacent words to the left
                    adjacentFlag = True
                    break
            if adjacentFlag: #If an adjacent word was found, skip to the next index in letterIndexes
                continue
            if startOfWord-1 >= 0 and occupiedSpaces[intersectionTuple[0], startOfWord-1]: # Check if there are any adjacent words above
                continue
            if endOfWord+1 < puzzleDimensions[1] and occupiedSpaces[intersectionTuple[0], endOfWord+1]: # Check if there are any adjacent words below
                continue

        else:  # Tests for horizontal placement
            startOfWord = intersectionTuple[0] - index
            endOfWord = intersectionTuple[0] + (len(word) - 1) - index

            if startOfWord < 0 or endOfWord >= puzzleDimensions[0]:  # If the word goes out of bounds
                continue

            for i in range(startOfWord, endOfWord + 1):
                if i == intersectionTuple[0]:  # Skip the intersection letter
                    continue
                if intersectionTuple[1] + 1 < puzzleDimensions[1] and occupiedSpaces[i, intersectionTuple[1] + 1]:  # Check if there are any adjacent words below
                    adjacentFlag = True
                    break
                if intersectionTuple[1] - 1 >= 0 and occupiedSpaces[i, intersectionTuple[1] - 1]:  # Check if there are any adjacent words above
                    adjacentFlag = True
                    break
            if adjacentFlag:  # If an adjacent word was found, skip to the next index in letterIndexes
                continue
            if startOfWord - 1 >= 0 and occupiedSpaces[startOfWord - 1, intersectionTuple[1]]:  # Check if there are any adjacent words to the left
                continue
            if endOfWord + 1 < puzzleDimensions[0] and occupiedSpaces[endOfWord + 1, intersectionTuple[1]]:  # Check if there are any adjacent words to the right
                continue

        return startOfWord #Valid placement found
    return -1 #No valid placement found

#Doesn't allow Intersections for now (partially because of the __word_can_be_placed function not handling them)
def __update_potential_words_list(potentialWordTuples: list, newWordStartIndex: int, newWord: str, removedTuple: tuple) -> list:
    """
    Updates the available letters list, deleting the first tuple from the list and adding more if needed
    For first word: use tuple (-1, y_coord, False) as removedTuple because newWordStartIndex will be x_coord
    if you want a vertical first word, use tuple (x_coord, -1, True) at your own risk (not tested)
    @param potentialWordTuples: main list of tuples used during puzzle generation
    @return: updated potentialWordTuples
    """
    if newWordStartIndex == -1: #no new word needs to be added
        return potentialWordTuples

    #Add new potential tuples to the list
    if removedTuple[2]: #If the new word is vertical
        for i in range(newWordStartIndex, newWordStartIndex+len(newWord)):
            #skip the intersection letter
            if i == removedTuple[1]:
                continue
            potentialWordTuples.append((removedTuple[0], i, False, newWord[i-newWordStartIndex]))
    else: #If the new word is horizontal
        for i in range(newWordStartIndex, newWordStartIndex+len(newWord)):
            #skip the intersection letter
            if i == removedTuple[0]:
                continue
            potentialWordTuples.append((i, removedTuple[1], True, newWord[i-newWordStartIndex]))

    return potentialWordTuples