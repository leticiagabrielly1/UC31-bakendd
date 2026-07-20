from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

ARQUIVO = "livros.json"


def carregar_livros():
    if not os.path.exists(ARQUIVO):
        with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
            json.dump([], arquivo)

    with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def salvar_livros(livros):
    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(livros, arquivo, indent=4, ensure_ascii=False)


@app.route("/", methods=["GET", "POST"])
def cadastro():

    erro = ""

    if request.method == "POST":

        titulo = request.form["titulo"].strip()
        autor = request.form["autor"].strip()
        ano = request.form["ano"].strip()
        categoria = request.form["categoria"].strip()
        quantidade = request.form["quantidade"].strip()

        if not titulo or not autor or not ano or not categoria or not quantidade:
            erro = "Preencha todos os campos."

        elif not ano.isdigit():
            erro = "O ano deve conter apenas números."

        elif not quantidade.isdigit() or int(quantidade) <= 0:
            erro = "Quantidade inválida."

        else:

            livros = carregar_livros()

            livros.append({
                "titulo": titulo,
                "autor": autor,
                "ano": int(ano),
                "categoria": categoria,
                "quantidade": int(quantidade)
            })

            salvar_livros(livros)

            return redirect(url_for("livros"))

    return render_template("cadastro.html", erro=erro)


@app.route("/livros")
def livros():

    lista = carregar_livros()

    return render_template("livros.html", livros=lista)


@app.route("/buscar", methods=["GET", "POST"])
def buscar():

    livro = None
    mensagem = ""

    if request.method == "POST":

        titulo = request.form["titulo"].lower()

        livros = carregar_livros()

        for l in livros:
            if l["titulo"].lower() == titulo:
                livro = l
                break

        if livro is None:
            mensagem = "Livro não encontrado."

    return render_template("buscar.html", livro=livro, mensagem=mensagem)


@app.route("/editar/<int:indice>", methods=["GET", "POST"])
def editar(indice):

    livros = carregar_livros()

    if request.method == "POST":

        livros[indice]["titulo"] = request.form["titulo"]
        livros[indice]["autor"] = request.form["autor"]
        livros[indice]["ano"] = int(request.form["ano"])
        livros[indice]["categoria"] = request.form["categoria"]
        livros[indice]["quantidade"] = int(request.form["quantidade"])

        salvar_livros(livros)

        return redirect(url_for("livros"))

    return render_template("editar.html", livro=livros[indice], indice=indice)


@app.route("/excluir/<int:indice>")
def excluir(indice):

    livros = carregar_livros()

    livros.pop(indice)

    salvar_livros(livros)

    return redirect(url_for("livros"))


if __name__ == "__main__":
    app.run(debug=True)