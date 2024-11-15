<?php
include('connexion.php');
//Variables Parametres

$dimensions = [];
$langue = '' ;


//Traitement des Parametres
$type =  htmlspecialchars($_GET['type']);
$lang =  htmlspecialchars($_GET['lang']);
switch ($type) {
    case 0:
        $dimensions = [13,6];
        break;
    case 1:
        $dimensions = [6,7];
}
switch ($lang) {
    case 0:
        $langue = 'FR';
        break;
    case 1:
        $langue = 'EN';
}

//Requête préparé
$puzzleCaracteristics =$connexion->prepare('
SELECT PS.id, PS.letters
FROM puzzles PS
    JOIN  puzzleWords P ON PS.id = P.puzzleId
     WHERE Xdimension = :dimensionX
       AND Ydimension = :dimensionY
       AND language = :langue ');


$word =$connexion->prepare('
SELECT PW.Xcoord, PW.Ycoord, PW.is_vertical, PW.wordId
FROM puzzles P
    JOIN  puzzleWords PW ON P.id = PW.puzzleId
     WHERE puzzleId = :puzzleId
     ORDER BY PW.wordId ASC ');

$wordListPrepared = $connexion->prepare('SELECT id, word FROM words
    JOIN puzzleWords ON words.id = puzzleWords.wordId
                WHERE puzzleID = :puzzleId ORDER BY id ASC;');



//Execution des parametres de puzzle Caracteristics
$puzzleCaracteristics->execute([':dimensionX' => $dimensions[0], ':dimensionY' => $dimensions[1], ':langue' => $langue]);
//Ajout des donnees(DimensionX,Y, id puzzle et lettres du puzzles) dans puzzlesCaracteristicsArray
$puzzleCaracteristicsArray = $puzzleCaracteristics->fetch(PDO::FETCH_ASSOC);


//Execution des parametres de puzzle word

$word->execute([$puzzleCaracteristicsArray['id']]);

//Ajout des mots en fonction de l'ID du puzzle

$wordsArray = $word->fetchAll(PDO::FETCH_ASSOC);

//Algo taille

//Execution des paramettres de wordListPrepared

$wordListPrepared ->execute([$puzzleCaracteristicsArray['id']]);
//Ajout des Mots et leur id dans wordList
$wordList = $wordListPrepared->fetchAll(PDO::FETCH_ASSOC);

//echo strlen($wordList[0]['word']);

//Parcours de wordsArray
for ($i = 0; $i < count($wordList); $i++) {
    //
    unset($wordsArray[$i]['wordId']);
    //
    $wordsArray[$i]['length'] = strlen($wordList[$i]['word']);



}
//
$resultat =array_merge(array($puzzleCaracteristicsArray),$wordsArray);
//Encodage JSON

echo json_encode($resultat);

