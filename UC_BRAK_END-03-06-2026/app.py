from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def inicio():
    return render_template('formulario.html')


@app.route('/cadastro', methods=['POST'])
def cadastro():

    nome = request.form.get('nome', '').strip().title()
    email = request.form.get('email', '').strip().lower()
    telefone = request.form.get('telefone', '').replace('(', '').replace(')', '').replace(' ', '').replace('-', '')
    cpf = request.form.get('cpf', '').replace('.', '').replace('-', '').strip()
    cidade = request.form.get('cidade', '').strip()
    estado = request.form.get('estado', '').strip().upper()
    curso = request.form.get('curso', '').strip()
    idade = request.form.get('idade', '').strip()
    senha = request.form.get('senha', '')

    erros = []

    if len(nome) < 8:
        erros.append("Nome inválido (mínimo 8 caracteres).")

    if "@" not in email or ".com" not in email:
        erros.append("E-mail inválido.")

    if len(telefone) != 11 or not telefone.isdigit():
        erros.append("Telefone inválido (11 dígitos).")

    if len(cpf) != 11 or not cpf.isdigit():
        erros.append("CPF inválido (11 dígitos).")

    if len(cidade) < 3:
        erros.append("Cidade inválida.")

    if len(estado) != 2:
        erros.append("Estado inválido.")

    if not curso:
        erros.append("Selecione um curso.")

    if not idade.isdigit() or int(idade) < 16:
        erros.append("Idade mínima de 16 anos.")

    if len(senha) < 8 or not any(c.isdigit() for c in senha):
        erros.append("Senha deve ter 8 caracteres e pelo menos 1 número.")

    if erros:
        return render_template(
            'formulario.html',
            erros=erros,
            dados=request.form
        )

    return render_template(
        'sucesso.html',
        nome=nome,
        email=email,
        telefone=telefone,
        cpf=cpf,
        cidade=cidade,
        estado=estado,
        curso=curso,
        idade=idade
    )


if __name__ == '__main__':
    app.run(debug=True)