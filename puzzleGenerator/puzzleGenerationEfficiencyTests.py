from puzzleGenerator import *
from time import time
from tqdm import tqdm

#Insert the name of the sqlite database here
SQLITE_DATABASE_NAME = "Database/puzzles.db"

#Amount of puzzles to attempt to generate
puzzlesToGenerate = 100

#Amount of times those puzzles will be generated (to get an average)
amountOfTestsToRun = 5

#Dimensions of the puzzles to generate # Large = (13,6) # Small = (6,7)
dimensions = (13,6)

#Language of the puzzles to generate # English = "EN" # French = "FR"
language = "EN"

#Amount of letters the test puzzles will contain
amountOfLetters = 6

#frequency table of the letters in the language the puzzles will be generated in, refer to the tables in the puzzleGenerator.py file
frequencyTable = frequenciesEN

resultData = {"puzzlesGenerated": [], "puzzlesWordCount": [], "allWordsLoadTime": [], "filterWordsTime": [], "puzzleGenerationTime": [], "totalTime": []}

startTotalTime = time()
for _ in tqdm(range(amountOfTestsToRun)):
    puzzlesGenerated = 0

    startLoading = time()
    allWords = load_words(SQLITE_DATABASE_NAME, language, amountOfLetters, 3)
    resultData["allWordsLoadTime"].append(time() - startLoading)

    for _ in range(puzzlesToGenerate):
        try:
            letters = generateLetters(amountOfLetters, frequencyTable)

            startFiltering = time()
            filteredWords = filter_words(allWords, letters)
            filterTime = time() - startFiltering

            startGeneration = time()
            newPuzzle = generatePuzzle(dimensions, filteredWords)
            generationTime = time() - startGeneration
            wordsPerPuzzle = newPuzzle.shape[0]

            puzzlesGenerated += 1
            resultData["filterWordsTime"].append(filterTime)
            resultData["puzzleGenerationTime"].append(generationTime)
            resultData["puzzlesWordCount"].append(wordsPerPuzzle)
        except ValueError:
            continue
    resultData["puzzlesGenerated"].append(puzzlesGenerated)
resultData["totalTime"] = time() - startTotalTime

print(f"Results for this test: {amountOfTestsToRun} tests attempting to generate {puzzlesToGenerate} puzzles each")
print("Total time taken: ", round(resultData["totalTime"], 2), "seconds")
print("Total puzzles generated: ", totalPuzzlesGenerated:=sum(resultData["puzzlesGenerated"]))
print("Average amount of puzzles generated: ", round(totalPuzzlesGenerated / amountOfTestsToRun, 3))
print("Average amount of words in a puzzle: ", round(sum(resultData["puzzlesWordCount"]) / totalPuzzlesGenerated, 3))
print("Average time taken to load words from database: ", round(sum(resultData["allWordsLoadTime"]) / amountOfTestsToRun, 3), "seconds")
print("Average time taken to filter words: ", round(sum(resultData["filterWordsTime"]) / totalPuzzlesGenerated, 3), "seconds")
print("Average time taken to generate a puzzle: ", round(sum(resultData["puzzleGenerationTime"]) / totalPuzzlesGenerated, 3), "seconds")
print("Average puzzle generation rate: ", round(totalPuzzlesGenerated / resultData["totalTime"], 3), "puzzles per second")