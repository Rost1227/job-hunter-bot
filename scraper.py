import sqlite3
from urllib.parse import quote
import requests
from bs4 import BeautifulSoup

# O nome do nosso arquivo de banco de dados
DB_FILE = "vagas.db"

def fetch_search_profile(profile_id: int):
    """
    Busca um perfil de busca específico no banco de dados pelo seu ID.

    Args:
        profile_id (int): O ID do perfil a ser buscado.

    Returns:
        tuple: Uma tupla contendo (palavras_chave, localidade) ou None se não encontrado.
    """
    conn = None
    try:
        # Conecta ao banco de dados em modo somente leitura (uri=True)
        conn = sqlite3.connect(f"file:{DB_FILE}?mode=ro", uri=True)
        cursor = conn.cursor()
        print(f"Conectado ao banco de dados para ler o perfil ID: {profile_id}")

        # Query SQL para selecionar as colunas que nos interessam de um perfil específico
        query = "SELECT palavras_chave, localidade FROM Perfis WHERE id = ?"
        cursor.execute(query, (profile_id,))
        profile_data = cursor.fetchone()
        
        if profile_data:
            print("Perfil encontrado.")
            return profile_data
        else:
            print("Perfil não encontrado.")
            return None

    except sqlite3.Error as e:
        print(f"Ocorreu um erro ao ler o banco de dados: {e}")
        return None
    finally:
        if conn:
            conn.close()
            print("Conexão de leitura com o banco de dados fechada.")

def build_linkedin_url(keywords: str, location: str):
    """
    Constrói uma URL de busca de vagas para o LinkedIn.

    Args:
        keywords (str): As palavras-chave para a busca.
        location (str): A localização para a busca.
    
    Returns:
        str: A URL completa para a busca no LinkedIn.
    """
# Formata as palavras-chave e a localização para serem seguras para URL
    formatted_keywords = quote(keywords)
    formatted_location = quote(location)
    linkedin_url = f"https://www.linkedin.com/jobs/search/?keywords={formatted_keywords}&location={formatted_location}&f_WT=2"
    return linkedin_url
    
    pass

def parse_html_file(filename: str):
    """
    Carrega e analisa um arquivo HTML local usando BeautifulSoup.

    Args:
        filename (str): O caminho para o arquivo HTML a ser lido.

    Returns:
        BeautifulSoup: Um objeto 'soup' que pode ser pesquisado, ou None se ocorrer um erro.
    """
    print(f"Lendo o arquivo HTML local: {filename}")
    try:
        with open("pagina.html", "r", encoding="utf-8") as f:
                html_content = f.read()
        soup = BeautifulSoup(html_content, 'lxml')
        print("Arquivo HTML analisado com sucesso.")
        return soup
    except FileNotFoundError:
        print(f"Erro: O arquivo '{filename}' não foi encontrado. Execute a Tarefa 2.3 primeiro.")
        return None
    except Exception as e:
        print(f"Ocorreu um erro inesperado ao analisar o arquivo: {e}")
        return None

# --- Bloco de Teste ---
##TESTE SCRAPER
"""if __name__ == "__main__":
    print("--- INICIANDO PROCESSO DE TESTE DO SCRAPER ---")

    # --- PASSO 1: Buscar o perfil de busca no banco de dados ---
    print("\n[PASSO 1/4] Buscando perfil do banco de dados...")
    profile_to_search = fetch_search_profile(profile_id=1)

    # O script só continua se o perfil for encontrado com sucesso
    if profile_to_search:
        palavras_chave, localidade = profile_to_search
        print("-> Perfil encontrado com sucesso.")

        # --- PASSO 2: Construir a URL de busca ---
        print("\n[PASSO 2/4] Construindo URL de busca para o LinkedIn...")
        url_de_busca = build_linkedin_url(palavras_chave, localidade)
        print(f"-> URL gerada: {url_de_busca[:70]}...") # Mostra apenas o início da URL

        # --- PASSO 3: Fazer a requisição HTTP para o LinkedIn ---
        print("\n[PASSO 3/4] Fazendo requisição HTTP com autenticação...")
        
        # O cookie 'li_at' que você pegou da sua conta robô
        linkedin_cookie = "AQEDAVzGZEADIL92AAABmB5qooQAAAGYQncmhE4AG8zNNllZFU-FeEP1NuXARwMpviEVEOfm5FRZe8jhLsYIjPdFtOx6nsbWL0PfmVyhYcpgrzx8MOaskm5qDYGq0ArNryCtHgTvqW8ypPoVk3l2mYrM"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Cookie": f"li_at={linkedin_cookie}"
        }
        
        try:
            response = requests.get(url_de_busca, headers=headers)
            # Lança um erro se a resposta não for bem-sucedida (ex: 404, 403)
            response.raise_for_status() 
            print(f"-> Status da Resposta: {response.status_code} (Sucesso)")

            # --- PASSO 4: Salvar o conteúdo HTML em um arquivo ---
            print("\n[PASSO 4/4] Salvando o conteúdo HTML em 'pagina.html'...")
            with open("pagina.html", "w", encoding="utf-8") as f:
                f.write(response.text)
            print("-> Arquivo 'pagina.html' salvo com sucesso na pasta do projeto.")

        except requests.exceptions.RequestException as e:
            print(f"-> Falha na requisição: {e}")

    else:
        print("-> ERRO: Não foi possível continuar pois o perfil com id=1 não foi encontrado.")
    
    print("\n--- PROCESSO DE TESTE FINALIZADO ---")"""

# Bloco de teste para a Tarefa 2.4
if __name__ == "__main__":
    print("--- INICIANDO TESTE DA TAREFA 2.4: PARSING DE HTML ---")

    # Chama a função para ler e analisar o arquivo local
    soup = parse_html_file("pagina.html")

    if soup:
        # Teste simples para verificar o sucesso do parsing
        if soup.title:
            print(f"Título da Página Encontrado: '{soup.title.string.strip()}'")
        else:
            print("O objeto soup foi criado, mas nenhum título foi encontrado.")

        print("\nTarefa 2.4 parece ter sido executada com sucesso.")
        print(soup)
    else:
        print("\nFalha ao executar a Tarefa 2.4.")

    print("\n--- TESTE FINALIZADO ---")