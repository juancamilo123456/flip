from flask import Flask, render_template, request
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

search_history = []  # historial de búsquedas


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        query = request.form.get("query")
        if query:
            search_history.insert(0, query)  # guardar historial

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
                    # Si la búsqueda es ambigua, mostrar algunas opciones
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

            return render_template("results.html", query=query, results=results, history=search_history)

    return render_template("index.html", history=search_history)


if __name__ == "__main__":
    app.run(debug=True)
