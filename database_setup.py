import sqlite3
import os

DB_FILE = "vagas.db"

def setup_database():
    """Função principal para configurar o banco de dados."""
    
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        print(f"Conexão com '{DB_FILE}' estabelecida.")
        # --- Dados dos Perfis a serem inseridos ---
        perfis_para_inserir = [
            (
                'Rafael - Vagas ML/Dev',
                'rafarostps4@gmail.com',
                '("Engenheiro de Machine Learning" OR "Machine Learning Engineer" OR "Desenvolvedor de Software" OR "Software Developer" OR "Engenheiro de Backend")',
                'Brasil'
            )
        ]

# --- Criar Tabela Perfis ---
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Perfis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email_destino TEXT NOT NULL,
            palavras_chave TEXT NOT NULL,
            localidade TEXT
        );
        """)
        print("Tabela 'Perfis' criada.")
        print("Tabelas serão criadas aqui...")

# --- Criar Tabela Vagas ---
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Vagas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url_vaga TEXT NOT NULL UNIQUE,
            titulo TEXT NOT NULL,
            data_coleta TEXT NOT NULL
        );
        """)
        print("Tabela 'Vagas' criada.")

        # --- Criar Tabela Alertas_Enviados ---
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Alertas_Enviados (
            id_perfil INTEGER NOT NULL,
            id_vaga INTEGER NOT NULL,
            PRIMARY KEY (id_perfil, id_vaga),
            FOREIGN KEY (id_perfil) REFERENCES Perfis (id),
            FOREIGN KEY (id_vaga) REFERENCES Vagas (id)
        );
        """)
        print("Tabela 'Alertas_Enviados' criada.")

# --- Inserir os perfis na tabela ---
        query_inserir_perfil = "INSERT INTO Perfis (nome, email_destino, palavras_chave, localidade) VALUES (?, ?, ?, ?)"
        
        cursor.executemany(query_inserir_perfil, perfis_para_inserir)
        print(f"{cursor.rowcount} perfis foram inseridos na tabela 'Perfis'.")

# Salva (commita) as alterações no banco de dados
        conn.commit()
        print("Estrutura do banco de dados salva com sucesso!")

    except sqlite3.Error as e:
        # Se qualquer erro de SQL ocorrer, ele será capturado e impresso aqui.
        print(f"Ocorreu um erro ao configurar o banco de dados: {e}")
    finally:
        # Este bloco SEMPRE será executado, garantindo que a conexão seja fechada.
        if conn:
            conn.close()
            print("Conexão com o banco de dados fechada.")

if __name__ == "__main__":
    setup_database()