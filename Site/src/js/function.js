let selectedLetters = [];
let textAreaContent = '';

document.querySelectorAll('.letter').forEach(letter => {
    letter.addEventListener('click', () => {
        if (letter.classList.contains('selected')) {
            // Deselect the letter
            letter.classList.remove('selected');
            letter.style.backgroundColor = 'white';
            textAreaContent = textAreaContent.replace(letter.textContent, '');
            selectedLetters = selectedLetters.filter(l => l !== letter);
        } else {
            // Select the letter
            letter.classList.add('selected');
            letter.style.backgroundColor = 'green';
            textAreaContent += letter.textContent;
            selectedLetters.push(letter);
        }
        updateTextArea(textAreaContent);
    });
});

function updateTextArea(text) {
    const textArea = document.querySelector('.text-area');
    textArea.textContent = text;
}

let listeMots = ['DURE', 'RUDE', 'DUR', 'RUE', 'PRUDE'];

document.querySelector('.power-up.validate').addEventListener('click', () => {
    const textArea = document.querySelector('.text-area');
    const word = textArea.textContent;
    if (listeMots.includes(word)) {
        const letterTiles = document.querySelectorAll('.tile');
        let found = false;

        // Check horizontally
        for (let i = 0; i < letterTiles.length; i++) {
            if (letterTiles[i].textContent === word[0]) {
                let match = true;
                for (let j = 0; j < word.length; j++) {
                    if (i + j >= letterTiles.length || letterTiles[i + j].textContent !== word[j]) {
                        match = false;
                        break;
                    }
                }
                if (match && (i === 0 || letterTiles[i - 1].classList.contains('hidden')) && (i + word.length >= letterTiles.length || letterTiles[i + word.length].classList.contains('hidden'))) {
                    for (let j = 0; j < word.length; j++) {
                        letterTiles[i + j].classList.remove('empty');
                        letterTiles[i + j].classList.add('filled');
                    }
                    found = true;
                    break;
                }
            }
        }

        // Check vertically
        if (!found) {
            const columns = 6; // Assuming a 6-column grid
            for (let i = 0; i < letterTiles.length; i++) {
                if (letterTiles[i].textContent === word[0]) {
                    let match = true;
                    for (let j = 0; j < word.length; j++) {
                        if (i + j * columns >= letterTiles.length || letterTiles[i + j * columns].textContent !== word[j]) {
                            match = false;
                            break;
                        }
                    }
                    if (match && (i < columns || letterTiles[i - columns].classList.contains('hidden')) && (i + word.length * columns >= letterTiles.length || letterTiles[i + word.length * columns].classList.contains('hidden'))) {
                        for (let j = 0; j < word.length; j++) {
                            letterTiles[i + j * columns].classList.remove('empty');
                            letterTiles[i + j * columns].classList.add('filled');
                        }
                        break;
                    }
                }
            }
        }
    } else {
        alert('Ce mot n\'existe pas !');
    }
    resetTextAreaAndLetters();
});

document.querySelector('.power-up.reset').addEventListener('click', () => {
    resetTextAreaAndLetters();
});

function resetTextAreaAndLetters() {
    const textArea = document.querySelector('.text-area');
    textArea.textContent = '';
    selectedLetters.forEach(letter => {
        letter.classList.remove('selected');
        letter.style.backgroundColor = 'white';
    });
    selectedLetters = [];
    textAreaContent = '';
}

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

document.querySelector('.power-up.flush').addEventListener('click', shuffleLetters);

// Utilisation des power-ups
document.querySelector('.power-up.definition').addEventListener('click', () => {
    alert('Utilisation du power-up Définition...');
});

document.querySelector('.power-up.hint').addEventListener('click', () => {
    alert('Utilisation du power-up Indice...');
});
