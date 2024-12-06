# Serveur_ubihard

## Name
PuzzleHard

## Description
Server hosted on a repurposed PC, used to host a website on which a simple, randomly-generated, word-puzzle can be played

## Installation
```bash
$ git clone https://gitlab.univ-lr.fr/projets-l2-2024/ubihard/serveur_ubihard.git
```
Anyone connecting to the ULR-Unbuntu 22.04-R.192 Linux VM and entering the IP address ‘10.192.12.92’ in a web browser can access it. 

**Instructions for accessing the server**
- Go to the Linux VM ULR-Unbuntu 22.04-R.192 -1 or -2
- Open the console
- Enter : ```$ ssh nico@10.192.12.92```
- password : tpuser
- Enter : ``` yes```

**Send a file from the university VM to the server**
Put the new version in a temporary folder (tmp) to avoid a ```permission denied```

On the university VM : 
- ```$ sudo scp -r  /home/tpuser/Documents/tmp/Site/pages src nico@10.192.12.92:/tmp/tmp_site```
- ```$ sudo scp  /home/tpuser/Documents/tmp/Site/index.html nico@10.192.12.92:/tmp/tmp_site```
On the remote server : 
- After having sent the folder to /tmp/tmp_site
- Enter : ```$ sudo cp -r ./ /var/www/html/```

**When you make a modification on ngnix, restart the ngnix server**
- Location of the file to be modified : /etc/nginx/sites-available/
- When modification is made : ```$ sudo systemctl reload nginx.service```

## Usage

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

## Roadmap
Fully functional, additional functionalities added on a case-by-case basis

## Authors and acknowledgment
Maxime Bucher-Martin

Adrien Gueguen

Enzo Cateau

Ekaekatai Gonzalez-Leroy 

## Project status

Final steps of development, finishing touches