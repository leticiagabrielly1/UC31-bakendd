from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)

app.secret_key = '123'

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form.get('email')
        senha = request.form.get('senha')

        if not email or not senha:

            flash('Preencha todos os campos.', 'erro')
            return redirect(url_for('login'))

        if email != 'admin@gmail.com' or senha != '123':

            flash('E-mail ou senha inválidos.', 'erro')
            return redirect(url_for('login'))

        return redirect(url_for('painel'))

    return render_template('login.html')

@app.route('/painel')
def painel():
    return render_template('painel.html')

if __name__ == '__main__':
    app.run(debug=True)