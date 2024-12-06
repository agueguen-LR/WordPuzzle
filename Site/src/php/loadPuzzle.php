<?php
include('connexion.php');
//Variables Parametres

$dimensions = [];
$langue = '' ;
$blacklist = "";

//Traitement des Parametres
$type =  htmlspecialchars($_GET['type']);
$lang =  htmlspecialchars($_GET['lang']);


switch ($type) {

    case 0:
        $dimensions = [13,6];
        break;
    case 1:
        $dimensions = [6,7];
        break;
    default:
        throw new Exception("Une erreur est survenue dans le type");
}
switch ($lang) {
    case 0:
        $langue = 'FR';
        break;
    case 1:
        $langue = 'EN';
        break;
    default:
        throw new Exception("An error has occurred in language");
}

//if (isset($_COOKIE['blacklistPuzzle'])){
//    if (!empty( $_COOKIE['blacklistPuzzle']) ){
//        $blacklist = htmlspecialchars($_COOKIE['blacklistPuzzle']);
//    }
//
//}
//else{
//    throw new Exception("Cookie is not defined");
//}


//CONST

const SQL_PUZZLE_CHARACTERISTICS = "
    SELECT id, letters
    FROM puzzles 
    WHERE Xdimension = :dimensionX
      AND Ydimension = :dimensionY
      AND language = :langue 
      AND id NOT IN (%s)
    ORDER BY RANDOM()
    LIMIT 1
";

const SQL_WORD = "
SELECT PW.Xcoord, PW.Ycoord, PW.is_vertical, PW.wordId
FROM puzzles P
    JOIN  puzzleWords PW ON P.id = PW.puzzleId
     WHERE puzzleId = :puzzleId
     ORDER BY PW.wordId ASC ";

//Requête préparé

$puzzleCaracteristics = $connexion->prepare(
    sprintf(SQL_PUZZLE_CHARACTERISTICS, $blacklist)
);


$word =$connexion->prepare(
    sprintf(SQL_WORD)

);

$wordListPrepared = $connexion->prepare('SELECT id, word FROM words
    JOIN puzzleWords ON words.id = puzzleWords.wordId
                WHERE puzzleID = :puzzleId ORDER BY id ASC;');



//Execution des parametres de puzzle Caracteristics
$puzzleCaracteristics->execute([':dimensionX' => $dimensions[0], ':dimensionY' => $dimensions[1], ':langue' => $langue]);


//Ajout des donnees(DimensionX,Y, id puzzle et lettres du puzzles) dans puzzlesCaracteristicsArray
$puzzleCaracteristicsArray = $puzzleCaracteristics->fetch(PDO::FETCH_ASSOC);
//print_r($puzzleCaracteristicsArray);

//Execution des parametres de puzzle word
$word->execute([$puzzleCaracteristicsArray['id']]);

//Ajout des mots en fonction de l'ID du puzzle
$wordsArray = $word->fetchAll(PDO::FETCH_ASSOC);

//Algo taille

//Execution des parametres de wordListPrepared
$wordListPrepared ->execute([$puzzleCaracteristicsArray['id']]);

//Ajout des Mots et leur id dans wordList
$wordList = $wordListPrepared->fetchAll(PDO::FETCH_ASSOC);

//Parcours de wordsArray
for ($i = 0; $i < count($wordList); $i++) {
    //On retire wordId de l'array
    unset($wordsArray[$i]['wordId']);

    //On place une nouvelle cle et valeur dand l'array
    $wordsArray[$i]['length'] = strlen($wordList[$i]['word']);

}
//
$resultat =array_merge(array($puzzleCaracteristicsArray),$wordsArray);


//Encodage JSON
echo json_encode($resultat);

