import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

DB_URI = os.getenv("DB_URI")

def testar_conexao_banco():
    """
    Testa a conexão com o banco de dados usando a URI definida em DB_URI.
    Retorna True se a conexão for bem-sucedida, False caso contrário.
    """
    from sqlalchemy import create_engine
    try:
        engine = create_engine(DB_URI)
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        print("✅ Conexão com o banco de dados bem-sucedida.")
        return True
    except Exception as e:
        print(f"❌ Erro ao conectar ao banco de dados: {e}")
        return False


