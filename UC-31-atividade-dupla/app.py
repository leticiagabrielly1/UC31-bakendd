from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "copa2026"

perguntas = [
    {
        "pergunta": "Qual seleção é a maior campeã da Copa do Mundo?",
        "opcoes": ["Alemanha", "Brasil", "Argentina", "Itália"],
        "resposta": "Brasil"
    },
    {
        "pergunta": "Em que ano o Brasil conquistou o pentacampeonato?",
        "opcoes": ["1998", "2002", "2006", "2010"],
        "resposta": "2002"
    },
    {
        "pergunta": "Qual país sediou a Copa do Mundo de 2014?",
        "opcoes": ["Brasil", "Rússia", "Alemanha", "África do Sul"],
        "resposta": "Brasil"
    },
    {
        "pergunta": "Quem marcou os dois gols do Brasil na final da Copa de 2002?",
        "opcoes": ["Ronaldo", "Rivaldo", "Ronaldinho", "Kaká"],
        "resposta": "Ronaldo"
    },
    {
        "pergunta": "Quem venceu a Copa do Mundo de 2022?",
        "opcoes": ["Argentina", "França", "Brasil", "Croácia"],
        "resposta": "Argentina"
    }
]

@app.route("/")
def inicio():
    session.clear()
    return render_template("index.html")

@app.route("/iniciar", methods=["POST"])
def iniciar():

    session["nome"] = request.form["nome"]
    session["pontos"] = 0
    session["indice"] = 0

    return redirect(url_for("quiz"))

@app.route("/quiz")
def quiz():

    indice = session.get("indice", 0)

    if indice >= len(perguntas):
        return redirect(url_for("resultado"))

    return render_template(
        "quiz.html",
        pergunta=perguntas[indice],
        numero=indice + 1,
        nome=session["nome"]
    )

@app.route("/responder", methods=["POST"])
def responder():

    resposta = request.form["resposta"]

    indice = session["indice"]

    if resposta == perguntas[indice]["resposta"]:
        session["pontos"] += 1

    session["indice"] += 1

    return redirect(url_for("quiz"))
    
@app.route("/resultado")
def resultado():

    nome = session["nome"]
    pontos = session["pontos"]

    historico = session.get("historico", [])

    historico.append({
        "nome": nome,
        "pontos": pontos
    })

    session["historico"] = historico

    return render_template(
        "resultado.html",
        nome=nome,
        pontos=pontos
    )
@app.route("/historico")
def historico():

    historico = session.get("historico", [])

    return render_template(
        "historico.html",
        historico=historico
    )

if __name__ == "__main__":
    app.run(debug=True)