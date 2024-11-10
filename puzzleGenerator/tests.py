from puzzleGenerator import *
from time import time
from tqdm import tqdm

#Insert the name of the sqlite database here
SQLITE_DATABASE_NAME = "Database/puzzles.db"

#Dimensions of the large and the small puzzles
LDimensions = (13,6)
SDimensions = (6,7)

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

letters = generateLetters(6, frequenciesFR)
print("Randomly chosen letters: ")
print(letters)
startTime = time()
allFrenchWords = load_words(SQLITE_DATABASE_NAME, "FR", 6, 3)
print("Time taken to load words: ", time() - startTime, "seconds")
startTime = time()
filteredWords = filter_words(allFrenchWords, letters)
print("Time taken to filter words: ", time() - startTime, "seconds")
# print(filteredWords)
# print(filteredWords.shape)
startTime = time()
newPuzzle = generatePuzzle(LDimensions, filteredWords)
print(newPuzzle)
print("Time taken to generate puzzle: ", time() - startTime, "seconds")
