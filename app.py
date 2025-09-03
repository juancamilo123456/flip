from flask import Flask, render_template, request, jsonify
import wikipedia

app = Flask(__name__)

# Configurar Wikipedia en español
wikipedia.set_lang("es")

# Resultados ficticios iniciales
FAKE_RESULTS = [
    {"title": "Wikipedia", "url": "https://wikipedia.org", "snippet": "La enciclopedia libre."},
    {"title": "YouTube", "url": "https://youtube.com", "snippet": "Videos y entretenimiento."},
    {"title": "OpenAI", "url": "https://openai.com", "snippet": "Inteligencia artificial avanzada."},
    {"title": "React", "url": "https://reactjs.org", "snippet": "Biblioteca para construir interfaces."},
]


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        query = request.form.get("query")
        results = []

        if query:
            # Buscar en base ficticia
            results = [r for r in FAKE_RESULTS if query.lower() in r["title"].lower() or query.lower() in r["snippet"].lower()]

            # Si no se encuentra, intentar con Wikipedia
            if not results:
                try:
                    summary = wikipedia.summary(query, sentences=2)
                    page = wikipedia.page(query)
                    results.append({
                        "title": page.title,
                        "url": page.url,
                        "snippet": summary
                    })
                except wikipedia.exceptions.DisambiguationError as e:
                    options = e.options[:5]
                    for opt in options:
                        results.append({
                            "title": opt,
                            "url": f"https://es.wikipedia.org/wiki/{opt.replace(' ', '_')}",
                            "snippet": "Artículo sugerido de Wikipedia."
                        })
                except wikipedia.exceptions.PageError:
                    results.append({
                        "title": "Sin resultados",
                        "url": "#",
                        "snippet": "No se encontró información en Wikipedia."
                    })

            return render_template("results.html", query=query, results=results)

    return render_template("index.html")


# 🔹 Ruta para autocompletado
@app.route("/autocomplete")
def autocomplete():
    term = request.args.get("term", "").lower()
    suggestions = []

    if term:
        # Buscar en FAKE_RESULTS
        suggestions = [r["title"] for r in FAKE_RESULTS if term in r["title"].lower()]

        # Si no hay, intentar con Wikipedia (solo títulos sugeridos)
        if not suggestions:
            try:
                search_results = wikipedia.search(term, results=5)
                suggestions.extend(search_results)
            except:
                pass

    return jsonify(suggestions[:5])  # máximo 5 sugerencias


if __name__ == "__main__":
    app.run(debug=True)
