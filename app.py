from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3, os

SECRET_KEY = "c306f97a5d1bcea528d5c180370323cc"

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")  # necessário para mensagens flash

# Função para conectar ao banco
def get_db_connection():
    conn = sqlite3.connect('usuarios.db')
    conn.row_factory = sqlite3.Row
    return conn

# Página inicial - lista usuários
@app.route('/')
def index():
    conn = get_db_connection()
    usuarios = conn.execute('SELECT * FROM usuarios').fetchall()
    conn.close()
    return render_template('index.html', usuarios=usuarios)

# Criar usuário
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        if not nome or not email:
            flash("⚠️ Nome, Email e Senha são obrigatórios!", "warning")
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)', (nome, email, senha))
            conn.commit()
            conn.close()
            flash("✅ Usuário adicionado com sucesso!", "success")
            return redirect(url_for('index'))
    return render_template('create.html')

# Editar usuário
@app.route('/update/<int:id>', methods=('GET', 'POST'))
def update(id):
    conn = get_db_connection()
    usuario = conn.execute('SELECT * FROM usuarios WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']

        if not nome or not email:
            flash("⚠️ Nome e Email não podem estar vazios!", "warning")
        else:
            conn.execute('UPDATE usuarios SET nome = ?, email = ?, senha = ? WHERE id = ?', (nome, email, id))
            conn.commit()
            conn.close()
            flash("✏️ Usuário atualizado com sucesso!", "info")
            return redirect(url_for('index'))
    conn.close()
    return render_template('update.html', usuario=usuario)

# Excluir usuário
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM usuarios WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash("🗑️ Usuário excluído com sucesso!", "danger")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
