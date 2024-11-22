<?php
include('connexion.php');
$essai_joueur  = htmlspecialchars($_GET['essai_joueur']);
//Recuperation du puzzle
$idPuzzle = htmlspecialchars($_GET['idPuzzle']);

//
$verificationPrepared = $connexion->prepare('SELECT PW.Xcoord, PW.Ycoord, PW.is_vertical from Puzzles P
JOIN puzzleWords PW ON P.id = PW.puzzleId
JOIN words W ON PW.wordId = W.id
WHERE P.id = :idPuzzle AND W.word = :essai_joueur');

//Execution de la requete avec parametre
$verificationPrepared->execute([':essai_joueur'=>$essai_joueur,':idPuzzle'=>$idPuzzle]);
//Recuperation des coordonnee
$verification = $verificationPrepared->fetch(PDO::FETCH_ASSOC);

echo json_encode($verification);