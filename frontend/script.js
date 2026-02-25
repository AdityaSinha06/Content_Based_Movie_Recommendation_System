async function searchMovies() {
    const query = document.getElementById("queryInput").value.trim();
    const resultsDiv = document.getElementById("results");
    const messageDiv = document.getElementById("message");

    resultsDiv.innerHTML = "";
    messageDiv.innerText = "";

    if (!query) {
        messageDiv.innerText = "Please enter a movie name.";
        return;
    }

    try {
        const response = await fetch(
            `http://127.0.0.1:8000/recommend?query=${encodeURIComponent(query)}&top_n=10`
        );

        const data = await response.json();

        
        console.dir(data.results)
        if(data.results.length == 0) {
            messageDiv.innerText = "Movie not found"
            return;
        }

        if (data.message) {
            messageDiv.innerText = data.message;
            return;
        }

        data.results.forEach((movie, index) => {
            const card = document.createElement("div");
            card.className = "card";

            if (index === 0) {
                card.style.border = "2px solid #2d89ef";
            }

            card.innerHTML = `
                <h3>${movie.title}</h3>
                <a href="${movie.wikipedia_url}" target="_blank">
                    View on Wikipedia &#8599;
                </a>
            `;

            resultsDiv.appendChild(card);
        });

    } catch (error) {
        messageDiv.innerText = "Error connecting to backend.";
        console.error(error);
    }
}