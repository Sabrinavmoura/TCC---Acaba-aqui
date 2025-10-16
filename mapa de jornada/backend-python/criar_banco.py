import sqlite3


NOME_BANCO_DADOS = '../tcc_dados.db'

def criar_banco():
    print("Conectando ao banco de dados...")
    conn = sqlite3.connect(NOME_BANCO_DADOS)
    cursor = conn.cursor()
    print("Conexão bem-sucedida.")

    # --- APAGANDO TABELAS ANTIGAS (para recomeçar do zero) ---
    print("Apagando tabelas antigas, se existirem...")
    cursor.execute("DROP TABLE IF EXISTS respostas_diarias")
    cursor.execute("DROP TABLE IF EXISTS perguntas")
    print("Tabelas antigas apagadas.")

    # --- CRIANDO A NOVA TABELA DE PERGUNTAS ---
    print("Criando a nova tabela 'perguntas'...")
    cursor.execute("""
    CREATE TABLE perguntas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ordem INTEGER NOT NULL,
        titulo TEXT NOT NULL,
        tipo TEXT NOT NULL,
        opcoes TEXT
    );
    """)
    print("Tabela 'perguntas' criada com sucesso.")

    # --- CRIANDO A NOVA TABELA DE RESPOSTAS ---
    print("Criando a nova tabela 'respostas_diarias'...")
    cursor.execute("""
    CREATE TABLE respostas_diarias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT NOT NULL,
        id_pergunta INTEGER NOT NULL,
        resposta_selecionada TEXT,
        resposta_texto_livre TEXT,
        FOREIGN KEY (id_pergunta) REFERENCES perguntas (id)
    );
    """)
    print("Tabela 'respostas_diarias' criada com sucesso.")

    # --- INSERINDO AS NOVAS PERGUNTAS (COM EMOJIS CORRIGIDOS) ---
    print("Inserindo as novas perguntas do protótipo...")
    perguntas_para_inserir = [
        (1, 'Como você se sentiu hoje?', 'escala_emocao', '[{"emoji": "😞", "texto": "Triste"}, {"emoji": "😟", "texto": "Ansioso(a)"}, {"emoji": "😐", "texto": "Neutro(a)"}, {"emoji": "😊", "texto": "Esperançoso(a)"}]'),
        (2, 'Qual foi o seu nível de desejo de usar álcool/cigarro hoje?', 'escala_desejo', '[{"emoji": "🔴", "texto": "Alto"}, {"emoji": "🟠", "texto": "Médio"}, {"emoji": "🟡", "texto": "Baixo"}, {"emoji": "🟢", "texto": "Nenhum"}]'),
        (3, 'Qual foi sua maior dificuldade hoje?', 'multipla_escolha', '[{"emoji": "😫", "texto": "Estresse e cansaço extremo"}, {"emoji": "🌙", "texto": "Insônia ou sono ruim"}, {"emoji": "💔", "texto": "Discussões com familiares ou amigos"}, {"emoji": "🤯", "texto": "Ansiedade ou pensamento acelerado"}, {"emoji": "😶", "texto": "Solidão ou isolamento"}, {"emoji": "📉", "texto": "Falta de motivação"}, {"emoji": "💭", "texto": "Pensamentos de recaída"}, {"emoji": "❌", "texto": "Nenhuma dificuldade específica"}]'),
        (4, 'Você realizou alguma ação de autocuidado?', 'multipla_colha', '[{"emoji": "📖", "texto": "Leu conteúdos no blog"}, {"emoji": "💬", "texto": "Interagiu no fórum"}, {"emoji": "🧘", "texto": "Praticou meditação ou oração"}, {"emoji": "🚶", "texto": "Caminhou ou se movimentou fisicamente"}, {"emoji": "🎨", "texto": "Fez algo criativo (arte, escrita, etc.)"}, {"emoji": "💚", "texto": "Respirou fundo ou ficou em silêncio"}, {"emoji": "🗣️", "texto": "Conversou com alguém próximo"}, {"emoji": "😴", "texto": "Dormiu melhor do que no dia anterior"}, {"emoji": "❌", "texto": "Não realizou autocuidado"}]'),
        (5, 'Quer escrever algo sobre o seu dia? (Opcional)', 'texto_livre', '[]')
    ]

    cursor.executemany("INSERT INTO perguntas (ordem, titulo, tipo, opcoes) VALUES (?, ?, ?, ?)", perguntas_para_inserir)
    print(f"{cursor.rowcount} perguntas foram inseridas com sucesso.")

    
    conn.commit()
    conn.close()
    print("Banco de dados criado e populado com sucesso!")

if __name__ == '__main__':
    criar_banco()