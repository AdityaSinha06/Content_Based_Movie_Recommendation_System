// ===============================
// CONFIG
// ===============================

// Local development
const API_URL = "http://127.0.0.1:8000";

// When deployed, replace with Railway URL
// const API_URL = "https://your-app.up.railway.app";


// ===============================
// ELEMENT REFERENCES
// ===============================

const queryInput = document.getElementById("queryInput");
const resultsContainer = document.getElementById("results");
const loader = document.getElementById("loader");
const messageDiv = document.getElementById("message");
const searchBtn = document.getElementById("searchBtn");

// ===============================
// SEARCH FUNCTION
// ===============================

async function searchMovies() {

    const query = queryInput.value.trim();
    
    if (!query) {
        messageDiv.textContent = "Please enter a movie name";
        resultsContainer.innerHTML = "";
        return;
    }

    queryInput.value = "";
    searchBtn.disabled = true;

    // Reset UI
    resultsContainer.innerHTML = "";
    messageDiv.textContent = "";
    loader.classList.remove("hidden");

    
    try {
        const response = await fetch(
            `${API_URL}/recommend?query=${encodeURIComponent(query)}&top_n=10`
        );

        if (!response.ok) {
            throw new Error("Backend error");
        }

        const data = await response.json();

        loader.classList.add("hidden");

        if (!data.results || data.results.length === 0) {
            messageDiv.textContent = "No similar movies found";
            return;
        }

        renderResults(data.results);

    } catch (error) {
        messageDiv.textContent = "Error connecting to backend";
        console.error(error);
    } finally {
        loader.classList.add("hidden");
        searchBtn.disabled = false;
    }
}


// ===============================
// RENDER CARDS
// ===============================

function renderResults(movies) {

    movies.forEach((movie, index) => {

        const card = document.createElement("div");
        card.className = "card";
        
        if(index === 0) {
            card.style.border = "4px solid #2d89ef";
        }

        card.innerHTML = `
            <img 
                src="${movie.poster_url || 'https://via.placeholder.com/300x450?text=No+Image'}" 
                alt="${movie.title}"
            />
            <h3>${movie.title}</h3>
            <a href="${movie.wikipedia_url}" target="_blank">
                View on Wikipedia
            </a>
        `;

        resultsContainer.appendChild(card);
    });
}


// ===============================
// ENTER KEY SUPPORT
// ===============================

queryInput.addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        searchMovies();
    }
});