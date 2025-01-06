// Site/src/js/function.js

// Contenu actuel de la zone de texte et lettres sélectionnées
let selectedLetters = [];
let textAreaContent = '';

// Initialisation des événements
document.addEventListener('DOMContentLoaded', () => {
    setupLetterSelection();
    setupPowerUpButtons();
    setupMenuToggle();
});

/**
 * Configure la sélection de lettres et les événements de clic sur les lettres.
 */
function setupLetterSelection() {
    document.querySelectorAll('.letter').forEach(letter => {
        letter.addEventListener('click', () => handleLetterClick(letter));
    });
}

/**
 * Gère le clic sur une lettre.
 * @param {HTMLElement} letter - Élément HTML de la lettre cliquée.
 */
function handleLetterClick(letter) {
    if (letter.classList.contains('selected')) {
        deselectLetter(letter);
    } else {
        selectLetter(letter);
    }
    updateTextArea(textAreaContent);
}

/**
 * Sélectionne une lettre et met à jour le contenu de la zone de texte.
 * @param {HTMLElement} letter - Élément HTML de la lettre à sélectionner.
 */
function selectLetter(letter) {
    letter.classList.add('selected');
    letter.style.backgroundColor = '#4b0082';
    textAreaContent += letter.textContent;
    selectedLetters.push(letter);
}

/**
 * Désélectionne une lettre et met à jour le contenu de la zone de texte.
 * @param {HTMLElement} letter - Élément HTML de la lettre à désélectionner.
 */
function deselectLetter(letter) {
    letter.classList.remove('selected');
    letter.style.backgroundColor = '#1a1a1a';
    textAreaContent = textAreaContent.replace(letter.textContent, '');
    selectedLetters = selectedLetters.filter(l => l !== letter);
}

/**
 * Met à jour le contenu de la zone de texte affichée.
 * @param {string} text - Le texte à afficher dans la zone de texte.
 */
function updateTextArea(text) {
    const textArea = document.querySelector('.text-area');
    textArea.textContent = text;
}

/**
 * Configure les boutons des power-ups et leurs événements.
 */
function setupPowerUpButtons() {
    document.querySelector('.power-up.validate').addEventListener('click', validateWord);
    document.querySelector('.power-up.reset').addEventListener('click', resetTextAreaAndLetters);
    document.querySelector('.power-up.flush').addEventListener('click', shuffleLetters);
    document.querySelector('.power-up.definition').addEventListener('click', () => alert('Utilisation du power-up Définition...'));
    document.querySelector('.power-up.hint').addEventListener('click', () => alert('Utilisation du power-up Indice...'));
}

/**
 * Valide le mot formé dans la zone de texte.
 */
async function validateWord() {
    const word = document.querySelector('.text-area').textContent;
    const id = document.querySelector('h2.id').textContent;
    if (word.length > 0) {
        const result = await getDataWord(word, id);
        if (result) {
            const coordonnees = {
                coord: `${parseInt(result.Xcoord)},${parseInt(result.Ycoord)}`,
                isVertical: result.is_vertical
            };

            const cell = document.getElementById(coordonnees.coord);
            const isVertical = coordonnees.isVertical;

            if (cell) {
                cell.classList.remove('empty');
                cell.classList.add('filled');
                cell.textContent = word[0];
            }
            if (!isVertical) {
                for (let i = 1; i < word.length; i++) {
                    const nextCell = document.getElementById(`${parseInt(coordonnees.coord.split(',')[0]) + i},${parseInt(coordonnees.coord.split(',')[1])}`);
                    if (nextCell) {
                        nextCell.classList.remove('empty');
                        nextCell.classList.add('filled');
                        nextCell.textContent = word[i];
                    }
                }
            } else {
                for (let i = 1; i < word.length; i++) {
                    const nextCell = document.getElementById(`${parseInt(coordonnees.coord.split(',')[0])},${parseInt(coordonnees.coord.split(',')[1]) + i}`);
                    if (nextCell) {
                        nextCell.classList.remove('empty');
                        nextCell.classList.add('filled');
                        nextCell.textContent = word[i];
                    }
                }
            }
            console.log(result);
        } else {
            console.log('Gros NUL ;p');
        }
    } else {
        alert('La zone de texte est vide.');
    }
    resetTextAreaAndLetters();
}

/**
 * Réinitialise la zone de texte et les lettres sélectionnées.
 */
function resetTextAreaAndLetters() {
    document.querySelector('.text-area').textContent = '';
    selectedLetters.forEach(letter => {
        letter.classList.remove('selected');
        letter.style.backgroundColor = '#1a1a1a';
    });
    selectedLetters = [];
    textAreaContent = '';
}

/**
 * Mélange les lettres dans la sélection.
 */
function shuffleLetters() {
    const letterSelection = document.querySelector('.letter-selection');
    const letters = Array.from(letterSelection.children);
    for (let i = letters.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [letters[i], letters[j]] = [letters[j], letters[i]];
    }
    letterSelection.innerHTML = '';
    letters.forEach(letter => letterSelection.appendChild(letter));
}

/**
 * Configure le basculement du menu.
 */
function setupMenuToggle() {
    const menuToggle = document.getElementById('menu-toggle');
    const menu = document.querySelector('.menu');
    menuToggle.addEventListener('change', () => {
        menu.style.display = menuToggle.checked ? 'block' : 'none';
    });
}

/**
 * Fonction pour obtenir les données du mot.
 * @param {string} word - Le mot à valider.
 * @param {string} id - L'ID du mot.
 * @returns {Promise} - Les données du mot.
 */
async function getDataWord(word, id) {
    const url = "";
    try {
        const response = await fetch("http://localhost:63342/serveur_ubihard/Site/src/php/verification.php?word=" + word + "&id=" + id);
        if (!response.ok) {
            throw new Error(`Response status: ${response.status}`);
        }

        const json = await response.json();
        return json; // Ensure the data is returned
    } catch (error) {
        console.error(error.message);
    }
}