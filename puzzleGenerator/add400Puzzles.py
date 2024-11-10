from puzzleGenerator import *

#This python file is used to generate some new puzzles into the database
#The puzzles will be generated in English and French of the two dimensions Large (13x6) and Small (6x7)
#It will be 100 puzzles of each combination of language and dimension
#The puzzles will be of 6 letters

#Insert the path to the sqlite database here
SQLITE_DATABASE_NAME = "Database/puzzles.db"

generateNewPuzzlesIntoDatabase(100, SQLITE_DATABASE_NAME, (13,6), "FR", 6, frequenciesFR)
generateNewPuzzlesIntoDatabase(100, SQLITE_DATABASE_NAME, (6,7), "FR", 6, frequenciesFR)
generateNewPuzzlesIntoDatabase(100, SQLITE_DATABASE_NAME, (13,6), "EN", 6, frequenciesEN)
generateNewPuzzlesIntoDatabase(100, SQLITE_DATABASE_NAME, (6,7), "EN", 6, frequenciesEN)