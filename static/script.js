// Función para usar historial como nueva búsqueda
function useSuggestion(text) {
    document.getElementById("search-input").value = text;
    document.querySelector("form").submit();
}

// Autocompletado con AJAX
document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("search-input");
    const suggestionsBox = document.getElementById("suggestions");

    if (!input) return;

    input.addEventListener("input", () => {
        const query = input.value.trim();
        if (query.length === 0) {
            suggestionsBox.style.display = "none";
            return;
        }

        fetch(`/autocomplete?term=${query}`)
            .then(res => res.json())
            .then(data => {
                suggestionsBox.innerHTML = "";
                if (data.length > 0) {
                    data.forEach(item => {
                        const li = document.createElement("li");
                        li.textContent = item;
                        li.onclick = () => {
                            input.value = item;
                            document.querySelector("form").submit();
                        };
                        suggestionsBox.appendChild(li);
                    });
                    suggestionsBox.style.display = "block";
                } else {
                    suggestionsBox.style.display = "none";
                }
            });
    });

    // Ocultar sugerencias si se hace clic afuera
    document.addEventListener("click", (e) => {
        if (!suggestionsBox.contains(e.target) && e.target !== input) {
            suggestionsBox.style.display = "none";
        }
    });
});
