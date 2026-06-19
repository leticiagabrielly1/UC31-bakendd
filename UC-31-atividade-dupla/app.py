from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = "copa2026"

ARQUIVO_HISTORICO = "historico.json"


def carregar_historico():
    if os.path.exists(ARQUIVO_HISTORICO):
        with open(ARQUIVO_HISTORICO, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def salvar_historico(historico):
    with open(ARQUIVO_HISTORICO, "w", encoding="utf-8") as f:
        json.dump(historico, f, indent=2, ensure_ascii=False)

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
    session["acertos"] = 0        
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
        nome=session["nome"],
        pontos=session["pontos"]     
    )

@app.route("/responder", methods=["POST"])
def responder():
    resposta = request.form["resposta"]
    indice = session["indice"]

    if resposta == perguntas[indice]["resposta"]:
        session["pontos"] += 10       
        session["acertos"] = session.get("acertos", 0) + 1

    session["indice"] += 1
    return redirect(url_for("quiz"))

@app.route("/resultado")
def resultado():
    nome = session["nome"]
    pontos = session["pontos"]
    acertos = session.get("acertos", 0)

    
    historico = carregar_historico()
    historico.append({
        "nome": nome,
        "pontos": pontos,
        "acertos": acertos
    })
    salvar_historico(historico)

    return render_template(
        "resultado.html",
        nome=nome,
        pontos=pontos,
        acertos=acertos
    )

@app.route("/historico")
def historico():
    historico = carregar_historico()
    return render_template("historico.html", historico=historico)

@app.route("/ranking")
def ranking():
    historico = carregar_historico()
    
    ranking = sorted(historico, key=lambda x: x["pontos"], reverse=True)
    return render_template("ranking.html", ranking=ranking)

if __name__ == "__main__":
    app.run(debug=True)