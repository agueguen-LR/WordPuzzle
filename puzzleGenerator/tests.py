from puzzleGenerator import *
from time import time
from tqdm import tqdm

#Insert the name of the sqlite database here
SQLITE_DATABASE_NAME = "Database/puzzles.db"

#Dimensions of the large and the small puzzles
LDimensions = (13,6)
SDimensions = (6,7)


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
