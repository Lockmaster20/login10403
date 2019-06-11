from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

#Base de Dados Início
def herokudb():
    Host='ec2-54-75-235-28.eu-west-1.compute.amazonaws.com'
    Database='d2g7rqemchqt6o'
    User='xgssvwgmdlwadz'
    Password='83903b481d14d35e2c52100414d54b0def77b4ee05adc41b43e8a0ef0996a958'
    return psycopg2.connect(host=Host, database=Database, user=User, password=Password, sslmode='require')
def existe(v1):
    try:
        ficheiro = herokudb()
        db = ficheiro.cursor()
        db.execute("SELECT * FROM usr WHERE nome= %s", (v1,))
        valor = db.fetchone()
        ficheiro.close()
    except:
        valor=None
    return valor

def gravar(v1, v2, v3):
    ficheiro = herokudb()
    db = ficheiro.cursor()
    db.execute("CREATE TABLE IF NOT EXISTS usr (nome text, email text, passe text)")
    db.execute("INSERT INTO usr VALUES (%s, %s, %s)", (v1, v2, v3))
    ficheiro.commit()
    ficheiro.close()

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

def log(v1, v2):
    ficheiro = herokudb()
    db = ficheiro.cursor()
    db.execute("SELECT * FROM usr WHERE nome = %s AND passe = %s ", (v1, v2,))
    valor = db.fetchone()
    ficheiro.close()
    return valor

@app.route('/login', methods=['GET', 'POST'])
def login():
    erro = None
    if request.method == 'POST':
        v1 = request.form['utilizador']
        v2 = request.form['passe']
        if not existe(v1):
            erro = 'O utilizador não existe'
        elif not log(v1, v2):
            erro = 'O utilizador e a palavra passe não coincidem'
        else:
            erro = 'Bem-vindo.'
    return render_template('login.html', erro=erro)

def alterar(v1, v2):
    import sqlite3
    ficheiro = sqlite3.connect('db/Utilizadores.db')
    db = ficheiro.cursor()
    db.execute("UPDATE usr SET passe = %s WHERE nome= %s", (v2, v1))
    ficheiro.commit()
    ficheiro.close()

@app.route('/newpasse', methods=['GET', 'POST'])
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

def apagar(v1):
    ficheiro = herokudb()
    db = ficheiro.cursor()
    db.execute("DELETE FROM usr WHERE nome= %s", (v1,))
    ficheiro.commit()
    ficheiro.close()

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    erro = None
    if request.method == 'POST':
        v1 = request.form['utilizador']
        v2 = request.form['passe']
        if not existe(v1):
            erro = 'O utilizador não existe'
        elif not log(v1, v2):
            erro = 'O utilizador e a palavra passe não coincidem'
        else:
            apagar(v1)
            erro = 'Utilizador eliminado.'
    return render_template('delete.html', erro=erro)

#Base de Dados Fim

if __name__ == ('__main__'):
    app.run(debug=True)
