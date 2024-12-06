<?php
//phpinfo();

try {
    $connexion = new PDO('sqlite:../../../Database/puzzles.db');
}
catch(Exception $e)
{
    echo 'Erreur : '.$e->getMessage().'<br />';
    echo 'N° : '.$e->getCode();
}
//garder en tête les connexions persistantes

