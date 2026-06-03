from flask import Flask, render_template, request

app = Flask(_name_)

@app.route('/')
def formulario():
    return render_template('index.html')


@app.route('/validacao', methods=['POST','GET'])
def cadastro():

    nome = request.form.get('Nome completo', '').strip().title()
    email = request.form.get('email','').strip().lower()
    Telefone = request.form.get('Telefone','').strip().title()
    CPF= request.form.get('CPF', '').strip().title()
    Cidade = request.form.get('Cidade','').strip().lower()
    Estado = request.form.get('Estado','').strip().title()
    Curso = request.form.get('Curso','').strip().title()
    Idade = request.form.get('Idade','').strip().title()
    Senha =request.form.get('Senha','').strip().title()
    

    return f"""
    Nome: {nome}<br>
    Email: {email}<br>
    Cidade: {cidade}<br>
    """


if __name__ == '__main__':
    app.run(debug=True)