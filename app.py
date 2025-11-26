import sqlite3, os
from flask import Flask, render_template, request, redirect, url_for, flash, g


DATABASE = 'usuarios.db'

app_id = locals().get('__app_id', 'default-app')

app = Flask(__name__)# ...

app.config['SECRET_KEY'] = '326cb9eea14a4e7d7987349969a05a625a5f689b704c15fcd675aef7a89bf7fa' 


# --- Funções de Banco de Dados ---

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row 
    return conn


# --- Rotas da Aplicação ---

@app.route('/')
def index():
  conn = get_db_connection()
  try:
        usuarios = conn.execute('SELECT id, nome, email FROM usuarios').fetchall()
        return render_template('index.html', usuarios=usuarios)

  except Exception as e:
        # Em caso de erro, mostre o erro no terminal e no flash
        app.logger.error("Erro ao carregar INDEX:", e)
        flash('Erro ao carregar usuários.', 'error')
        return render_template('index.html', usuarios=[])

  finally:
        # É crucial fechar a conexão, mas o @app.teardown_appcontext já faz isso
        pass


@app.route('/create', methods=('GET', 'POST'))
def cadastro():
    # Bloco POST: Processa a submissão do formulário
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        if not nome or not email or not senha:
            flash('⚠️ Todos os campos são obrigatórios!', 'warning')
            return redirect(url_for('cadastro'))
        
        # AQUI usamos try/except para gerenciar erros do DB
        try:
            conn = get_db_connection()
            conn.execute('INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)',
                         (nome, email, senha))
            conn.commit()
            
            flash(f'🎉 Conta para {nome} criada com sucesso!', 'success')
            return redirect(url_for('index'))
            
        except sqlite3.IntegrityError:
            flash('❌ Erro: O email fornecido já está em uso.', 'error')
            return redirect(url_for('cadastro'))
        except Exception as e:
            app.logger.error("Erro ao inserir usuário:", e)
            flash(f'❌ Erro interno ao cadastrar: {e}', 'error')
            return redirect(url_for('cadastro'))

    return render_template('cconta.html')


@app.route('/test')
def page_test():
    return "<h1>A ROTA DE TESTE FUNCIONOU!</h1>"


# Bloco para rodar a aplicação Flask
if __name__ == '__main__':
    # Rodar o Flask em modo debug (útil para desenvolvimento)
    # Host '0.0.0.0' permite acesso externo, e port 8080 é comum para testes
    app.run(host='0.0.0.0', port=8080, debug=True)


@app.route('/entrar', methods=('GET', 'POST'))
def login():

    return render_template('login.html')
