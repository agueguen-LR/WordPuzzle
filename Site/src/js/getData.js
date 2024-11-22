async function getData() {
    const url = "https://example.org/products.json";
    try {
        const response = await fetch("http://localhost/Projet_Ubihard/Site/src/php/loadPuzzle.php?type=0&lang=0");
        if (!response.ok) {
            throw new Error(`Response status: ${response.status}`);
        }

        const json= await response.json();
        return json;
    } catch (error) {
        console.error(error.message);
    }
}

console.log(getData());
