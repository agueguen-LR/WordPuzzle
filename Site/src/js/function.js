// Liste des mots valides
const listeMots = [];
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
function validateWord() {
    const word = document.querySelector('.text-area').textContent;
    if (listeMots.includes(word)) {
        alert('Mot valide !');
    } else {
        alert('Ce mot n\'existe pas !');
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
        letter.style.backgroundColor = 'white';
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