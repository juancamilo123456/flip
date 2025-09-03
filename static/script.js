document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("search-input");
    const suggestionsBox = document.getElementById("suggestions");
    const form = document.querySelector("form");

    if (!input) return;

    input.addEventListener("input", () => {
        const query = input.value.trim();
        if (query.length === 0) {
            suggestionsBox.innerHTML = "";
            suggestionsBox.style.display = "none";
            return;
        }

        fetch(`/autocomplete?term=${encodeURIComponent(query)}`)
            .then(res => res.json())
            .then(data => {
                suggestionsBox.innerHTML = "";
                if (data.length > 0) {
                    data.forEach(item => {
                        const li = document.createElement("li");
                        li.textContent = item;
                        li.onclick = () => {
                            input.value = item;
                            form.submit();
                        };
                        suggestionsBox.appendChild(li);
                    });
                    suggestionsBox.style.display = "block";
                } else {
                    suggestionsBox.style.display = "none";
                }
            })
            .catch(err => console.error("Error en autocompletado:", err));
    });

    // Ocultar sugerencias si se hace clic afuera
    document.addEventListener("click", (e) => {
        if (!suggestionsBox.contains(e.target) && e.target !== input) {
            suggestionsBox.style.display = "none";
        }
    });
});
