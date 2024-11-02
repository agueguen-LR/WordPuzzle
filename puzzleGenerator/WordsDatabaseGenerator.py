import sqlite3
import pandas as pd
from unidecode import unidecode

def loadDictionary(dictionaryFile:str) -> pd.DataFrame:
    """
    Loads dictionary.txt file into a pandas Dataframe
    The dictionary should contain 1 word per Line, capital letters only, no special characters
    @param dictionaryFile: file path of the dictionary file
    @return: pandas Dataframe containing all the available words
    """
    df = pd.read_csv(dictionaryFile, names=['word'])
    return df.dropna(subset = ['word'])

def loadFrequency(frequencyFile: str, freqColumns: list) -> pd.DataFrame:
    """
    Loads frequency file (usually tsv from external openlexicon link) into a pandas Dataframe
    @param frequencyFile: address of the lexicon database
    @param freqColumns: list of column names of the frequency table, column 0 should be the words, additional colmuns will be frequency mesurements averaged out
    @return: pandas Dataframe containing the words and their frequency
    """

    frequencies = pd.read_csv(frequencyFile, delimiter='\t', usecols=freqColumns)
    frequencies.rename(columns={freqColumns[0]: 'word'}, inplace=True)
    frequencies['frequency'] = frequencies[freqColumns[1:]].mean(axis=1) # creates freq column as the average of all other columns

    frequencies = frequencies[frequencies.word.map(lambda x: isinstance(x, str))] #filter the frequency dataframe to only contain strings in the word column
    frequencies = frequencies[frequencies.word.map(lambda x: x.isalpha())]  # filter the frequency dataframe to only contain alphabetical strings
    frequencies['word'] = frequencies['word'].apply(lambda x: unidecode(x)) # normalize the words to remove accents (unidecode also works for more complex cases, for example: chinese characters)
    frequencies['word'] = frequencies['word'].apply(lambda x: x.upper()) # Capitalizes the words

    frequencies = frequencies.sort_values(by='frequency', ascending=False) # Sort by descending frequency
    frequencies = frequencies.drop_duplicates(subset='word', keep='first') #Remove duplicate words with lower frequency

    return frequencies[['word', 'frequency']]

def loadLanguage(dictionary:pd.DataFrame, frequencies:pd.DataFrame) -> pd.DataFrame:
    """
    Loads the full dictionary and available frequencies into a pandas Dataframe,
    words not present in the frequencies dataframe will have NaN value
    @param dictionary: dictionary Dataframe
    @param frequencies: frequencies Dataframe
    @return: language Dataframe containing all words and their frequency
    """

    output = pd.merge(dictionary, frequencies[['word', 'frequency']], on='word', how='left')

    output = output.sort_values(by='frequency', ascending=False).reset_index(drop=True)

    return output

def addLanguageToDatabase(languageName:str, language:pd.DataFrame, databaseName: str, languageCode:str = "") -> None:
    """
    adds language to sqlite database
    @param languageName: name of the language, typically first two characters of language name
    @param language: dataframe resulting from loadLanguage
    @param databaseName: name of the sqlite database, typically 'puzzles.db'
    @param languageCode: optional parameter to specify the language code if it is not the first two letters Capitalized
    @return: None
    """
    if languageCode == "":
        languageCode = languageName[:2].upper()
    conn = sqlite3.connect(databaseName)
    c = conn.cursor()
    c.execute("INSERT INTO languages(code, name) SELECT ?, ? WHERE (SELECT 1 FROM languages WHERE code = ?) == NULL ", (languageCode, languageName, languageCode))
    language['language'] = languageCode
    print(language.to_sql('words', conn, index=False ,if_exists='append'))
    conn.commit()
    conn.close()

def clearLanguage(databaseName: str, language: str) -> None:
    """
    Removes the language from the database
    @param databaseName: name of the database
    @param language: name of the language
    @return: None
    """
    conn = sqlite3.connect(databaseName)
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS ?', language)
    conn.commit()
    conn.close()