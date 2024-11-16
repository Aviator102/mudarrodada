from flask import Flask, send_from_directory, request, jsonify
import mysql.connector
import os

app = Flask(__name__)

# Configurações do banco de dados
db_config = {
    'host': '18.209.111.107',
    'user': 'painelrodada2',
    'password': 'painelrodada2',
    'database': 'painelrodada2'
}

# Função para conectar ao banco de dados
def conectar_db():
    return mysql.connector.connect(**db_config)

# Rota para servir o arquivo index.html
@app.route('/')
def index():
    # Serve o arquivo index.html diretamente da raiz do projeto
    return send_from_directory(os.path.join(app.root_path), 'index.html')

# Rota para alterar a rodada no banco de dados
@app.route('/alterar_rodada', methods=['POST'])
def alterar_rodada():
    nova_rodada = request.form['rodada']
    
    conexao = conectar_db()
    cursor = conexao.cursor()
    cursor.execute("UPDATE rodada SET numero = %s WHERE id = 1", (nova_rodada,))
    conexao.commit()
    cursor.close()
    conexao.close()

    return jsonify({'status': 'sucesso', 'nova_rodada': nova_rodada})

# Função necessária para o Vercel
def handler(environ, start_response):
    from werkzeug.wsgi import DispatcherMiddleware
    from werkzeug.serving import run_simple

    # Vercel precisa que a função seja exposta de forma adequada
    return app.wsgi_app(environ, start_response)

if __name__ == '__main__':
    app.run(debug=True)
