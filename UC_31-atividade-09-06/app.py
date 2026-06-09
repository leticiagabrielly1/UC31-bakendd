import os
from flask import Flask, render_template, request, redirect, url_for, make_response

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static')
)

@app.route('/')
def inicio():
    nome = request.cookies.get('nome', '')
    tema = request.cookies.get('tema', 'claro')
    return render_template('inicio.html', nome=nome, tema=tema)


@app.route('/salvar-nome', methods=['POST'])
def salvar_nome():
    nome = request.form.get('nome', '').strip()
    tema = request.cookies.get('tema', 'claro')

    resposta = make_response(redirect(url_for('inicio')))

    if nome:
        resposta.set_cookie('nome', nome, max_age=60 * 60 * 24 * 365)

    resposta.set_cookie('tema', tema, max_age=60 * 60 * 24 * 365)
    return resposta


@app.route('/alterar-tema')
def alterar_tema():
    tema_atual = request.cookies.get('tema', 'claro')
    novo_tema = 'escuro' if tema_atual == 'claro' else 'claro'

    resposta = make_response(redirect(url_for('inicio')))
    resposta.set_cookie('tema', novo_tema, max_age=60 * 60 * 24 * 365)
    return resposta


@app.route('/limpar')
def limpar():
    resposta = make_response(redirect(url_for('inicio')))
    resposta.delete_cookie('nome')
    resposta.delete_cookie('tema')
    return resposta


if __name__ == '__main__':
    app.run(debug=True)