# WordPuzzle

## Description
Group project for second year at university, my role was to write the python scripts to generate puzzles and add them to the database.
I also came up with the current structure of the database.

## Puzzle generation into database, by Adrien Gueguen

### Adding Puzzles to the Database

Install requirements
```bash
pip install -r ./puzzleGenerator/requirements.txt
```

You can add 100 small english puzzles, large english puzzles, small french puzzles, and large french puzzles to the database by running the add400Puzzles.py script.:

```bash
python3 ./puzzleGenerator/add400Puzzles.py
```

Otherwise you can use the add400Puzzles.py script as an example to add your own puzzles to the database.

### Adding a new language to the database

Adding a new language requires:
 - a dictionary.txt file containing all the valid words of the language, capitalized, one per line
 - a link to an openlexicon database containing the language's word frequencies

You can then use the addLanguageToDatabase.py as an example.

## PHP files by Ekaekatai Gonzalez-Leroy

#### loadPuzzle.php 
This file takes the following parameters:

- type : 
  - 1 : size 13.6
  - 2 : size 6.7
- lang :
  - EN : English
  - FR : French

The file will return a JSON containing: 
- the ID of the puzzle
- the letters
- the XY location of each word and if it's vertical or not
- the length of each word
  
#### verification.php 
This file takes the word played by the player as a string and the ID of the current puzzle.  
It will return, if the word exists, the XY of the word and if it's vertical. If it doesn't exist, it will return false.

## Authors and acknowledgment
Maxime Bucher-Martin, Server and Nginx

Adrien Gueguen, Python and Database

Enzo Cateau, HTML, CSS and JS

Ekaekatai Gonzalez-Leroy, PHP
