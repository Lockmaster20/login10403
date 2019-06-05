from flask import Flask, render_template, request

app = Flask(__name__)


def gravar(v1, v2, v3):
    import sqlite3
    ficheiro = sqlite3.connect('db/Utilizadores.db')
    db = ficheiro.cursor()
    db.execute("CREATE TABLE IF NOT EXISTS usr (nome text, email text, passe text)")
    db.execute("INSERT INTO usr VALUES (?, ?, ?)", (v1, v2, v3))
    ficheiro.commit()
    ficheiro.close()

def existe(v1):
    import sqlite3
    ficheiro = sqlite3.connect('db/Utilizadores.db')
    db = ficheiro.cursor()
    db.execute("SELECT * FROM usr WHERE nome= ?", (v1,))
    valor = db.fetchone()
    ficheiro.close()
    return valor

#////////////////////NÃO FUNCIONA////////////////////NÃO FUNCIONA////////////////////NÃO FUNCIONA////////////////////
def login(v1, v3):
    import sqlite3
    ficheiro = sqlite3.connect('db/Utilizadores.db')
    db = ficheiro.cursor()
    db.execute("SELECT * FROM usr WHERE nome= ? AND password= ? ", (v1, v3))
    valor = db.fetchmany(v1, v3)
    ficheiro.close()
    return valor
#////////////////////NÃO FUNCIONA////////////////////NÃO FUNCIONA////////////////////NÃO FUNCIONA////////////////////

#////////////////////NÃO FUNCIONA////////////////////NÃO FUNCIONA////////////////////NÃO FUNCIONA////////////////////
@app.route('/login', methods=['GET', 'POST'])
def login():
    erro = None
    if request.method == 'POST':
        v1 = request.form['utilizador']
        v3 = request.form['passe']
        if not existe(v1):
            erro = 'O utilizador não existe'
        elif not login(v1, v3):
            erro = 'O utilizador e a palavra passe não coincidem'
    return render_template('login.html', erro=erro)
#////////////////////NÃO FUNCIONA////////////////////NÃO FUNCIONA////////////////////NÃO FUNCIONA////////////////////

@app.route('/registo', methods=['GET', 'POST'])
def route():
    erro = None
    if request.method == 'POST':
        v1 = request.form['utilizador']
        v2 = request.form['email']
        v3 = request.form['passe']
        v4 = request.form['cpasse']
        if existe(v1):
            erro = 'O utilizador já existe'
        elif v3 != v4:
            erro = 'A palavra passe não coincide.'
        else:
            gravar(v1, v2, v3)
    return render_template('registo.html', erro=erro)


def alterar(v1, v2):
    import sqlite3
    ficheiro = sqlite3.connect('db/Utilizadores.db')
    db = ficheiro.cursor()
    db.execute("UPDATE usr SET passe = ? WHERE nome= ?", (v2, v1))
    ficheiro.commit()
    ficheiro.close()

@app.route('/', methods=['GET', 'POST'])
def npasse():
    erro = None
    if request.method == 'POST':
        v1 = request.form['utilizador']
        v2 = request.form['passe']
        v3 = request.form['cpasse']
        if not existe(v1):
            erro = 'O utilizador não existe'
        if v2 != v3:
            erro = 'A palavra passe não coincide.'
        else:
            alterar(v1, v2)
    return render_template('npasse.html', erro=erro)


if __name__ == ('__main__'):
    app.run(debug=True)
