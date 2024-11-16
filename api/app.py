from flask import Flask, render_template, request, jsonify
import mysql.connector
from datetime import datetime

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

# Rota para exibir a página principal com a rodada e valor
@app.route('/')
def index():
    # Conectando ao banco de dados e buscando o último resultado
    conexao = conectar_db()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT valor, rodada FROM resultados ORDER BY id DESC LIMIT 1")
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()

    if resultado:
        valor_atual = resultado['valor']
        rodada_atual = resultado['rodada']
    else:
        valor_atual = "N/A"
        rodada_atual = 0

    return render_template('index.html', valor=valor_atual, rodada=rodada_atual)

# Rota para alterar a rodada no banco de dados
@app.route('/alterar_rodada', methods=['POST'])
def alterar_rodada():
    nova_rodada = request.form['rodada']
    
    # Conectando ao banco de dados e atualizando a rodada
    conexao = conectar_db()
    cursor = conexao.cursor()
    cursor.execute("UPDATE rodada SET numero = %s WHERE id = 1", (nova_rodada,))
    conexao.commit()
    cursor.close()
    conexao.close()

    return jsonify({'status': 'sucesso', 'nova_rodada': nova_rodada})

# Para o Vercel funcionar com Flask, você precisa expor a função Flask no padrão serverless
def handler(environ, start_response):
    """Converte o Flask app para ser executado no formato WSGI"""
    from werkzeug.serving import run_simple
    return app.wsgi_app(environ, start_response)

if __name__ == '__main__':
    app.run(debug=True)
