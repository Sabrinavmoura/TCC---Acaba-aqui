import sqlite3
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

# Nome do arquivo do banco de dados
NOME_BANCO_DADOS = '../tcc_dados.db'

app = Flask(__name__)
# Habilita o CORS para permitir a comunicação entre o front-end e o back-end
CORS(app)

# Função para se conectar ao banco de dados
def get_db_connection():
    conn = sqlite3.connect(NOME_BANCO_DADOS)
    conn.row_factory = sqlite3.Row
    return conn

# Rota para obter todas as perguntas do banco de dados
@app.route('/obter-perguntas', methods=['GET'])
def obter_perguntas():
    try:
        conn = get_db_connection()
        perguntas_db = conn.execute('SELECT * FROM perguntas ORDER BY ordem').fetchall()
        conn.close()

        perguntas_lista = []
        for p in perguntas_db:
            pergunta_dict = dict(p)
            pergunta_dict['opcoes'] = json.loads(pergunta_dict['opcoes'])
            perguntas_lista.append(pergunta_dict)
        
        return jsonify(perguntas_lista)
    except Exception as e:
        print(f"Erro ao obter perguntas: {e}")
        return jsonify({"erro": "Não foi possível carregar as perguntas do banco de dados."}), 500


# Rota para salvar as respostas enviadas pelo formulário
@app.route('/salvar-respostas', methods=['POST'])
def salvar_respostas():
    try:
        respostas = request.json.get('respostas')
        data_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        conn = get_db_connection()
        cursor = conn.cursor()

        for resposta in respostas:
            cursor.execute("""
                INSERT INTO respostas_diarias (data, id_pergunta, resposta_selecionada, resposta_texto_livre)
                VALUES (?, ?, ?, ?)
            """, (data_atual, resposta['id_pergunta'], resposta.get('resposta_selecionada'), resposta.get('resposta_texto_livre')))

        conn.commit()
        conn.close()
        
        return jsonify({"sucesso": "Respostas salvas com sucesso!"}), 200
    except Exception as e:
        print(f"Erro ao salvar respostas: {e}")
        return jsonify({"erro": "Ocorreu um erro ao salvar as respostas."}), 500



# Rota para buscar o histórico de respostas para o dashboard
@app.route('/obter-historico-respostas', methods=['GET'])
def obter_historico():
    try:
        conn = get_db_connection()
        # Este comando busca as respostas e junta com as informações da pergunta original
        respostas_db = conn.execute("""
            SELECT 
                rd.data, 
                p.titulo,
                p.tipo,
                rd.resposta_selecionada,
                p.opcoes
            FROM 
                respostas_diarias rd
            JOIN 
                perguntas p ON rd.id_pergunta = p.id
            ORDER BY 
                rd.id ASC
        """).fetchall()
        conn.close()

        # Transforma os dados em um formato fácil para o JavaScript usar
        historico_lista = []
        for r in respostas_db:
            resposta_dict = dict(r)
            # Precisamos "traduzir" o texto da resposta para o emoji correspondente
            opcoes_lista = json.loads(resposta_dict['opcoes'])
            emoji_correspondente = ''
            for opcao in opcoes_lista:
                if opcao['texto'] == resposta_dict['resposta_selecionada']:
                    emoji_correspondente = opcao['emoji']
                    break
            
            resposta_dict['emoji'] = emoji_correspondente
            historico_lista.append(resposta_dict)

        return jsonify(historico_lista)

    except Exception as e:
        print(f"Erro ao obter histórico: {e}")
        return jsonify({"erro": "Ocorreu um erro ao buscar o histórico de respostas."}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)