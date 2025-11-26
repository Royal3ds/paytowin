import sqlite3
from flask import Flask, render_template, request, redirect, url_for


DATABASE = 'usuarios.db'

app_id = locals().get('__app_id', 'default-app')

app = Flask(__name__)

# --- Funções de Banco de Dados ---

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row 
    return conn


# --- Rotas da Aplicação ---

@app.route('/')
def index():
    """Rota para a página inicial (index.html)."""
    # Exibe o ID do aplicativo no console para fins de debug
    print(f"App ID: {app_id}")
    return render_template('index.html')

@app.route('/cconta', methods=['GET'])
def cconta_page():
    return render_template('cconta.html')

@app.route('/registrar', methods=['POST'])
def registrar_usuario():
    """Rota para processar o envio do formulário de criação de conta (via POST)."""
    
    # 1. Coleta os dados do formulário
    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')
    
    # Validação básica
    if not nome or not email or not senha:
        return render_template('cconta.html', erro="Todos os campos são obrigatórios.")

    conn = get_db_connection()
    try:
        # 2. Verifica se o email já existe
        cursor = conn.execute('SELECT id FROM usuarios WHERE email = ?', (email,))
        usuario_existente = cursor.fetchone()
        
        if usuario_existente:
            # Se o usuário já existe, retorna um erro
            return render_template('cconta.html', erro="Este email já está registrado. Tente outro.")

        # 3. Insere o novo usuário no banco de dados
        # IMPORTANTE: Em uma aplicação real, a senha DEVE ser hasheada antes de ser salva (ex: com bcrypt).
        # Aqui, estamos salvando a senha como texto simples apenas para fins de demonstração.
        conn.execute('INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)',
                     (nome, email, senha))
        conn.commit()
        
        # 4. Redireciona o usuário para a página de criação de conta com uma mensagem de sucesso
        # O argumento 'mensagem' será passado para o cconta.html via render_template
        return render_template('cconta.html', mensagem=f"Conta criada com sucesso para: {nome}!")

    except sqlite3.IntegrityError as e:
        # Captura erros de integridade (como NOT NULL constraint)
        print(f"Erro de integridade ao registrar: {e}")
        return render_template('cconta.html', erro="Erro de banco de dados. Verifique os dados e tente novamente.")
    except Exception as e:
        # Captura outros erros
        print(f"Erro inesperado: {e}")
        return render_template('cconta.html', erro="Ocorreu um erro inesperado durante o registro.")
    finally:
        # Garante que a conexão com o banco de dados seja fechada
        conn.close()

# Bloco para rodar a aplicação Flask
if __name__ == '__main__':
    # Rodar o Flask em modo debug (útil para desenvolvimento)
    # Host '0.0.0.0' permite acesso externo, e port 8080 é comum para testes
    app.run(host='0.0.0.0', port=8080, debug=True)