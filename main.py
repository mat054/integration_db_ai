from chains.langchain_sql_chain import criar_chain
from sqlalchemy import create_engine
import pandas as pd
from config.settings import DB_URI
from sql_engine.materializer import criar_tabela_materializada
from utils.validators import sanitizar_nome_tabela

def main():
    pergunta = input("Pergunta em linguagem natural: ")
    chain = criar_chain()

    resposta = chain.run(pergunta)  # Executa a query e retorna o resultado como string
    print("\n✅ Resposta da LLM + SQL executada com sucesso:\n")
    print(resposta)

    # Opcional: também podemos acessar os dados com pandas e salvar
    db_engine = create_engine(DB_URI)
    df = pd.read_sql(chain.intermediate_steps[-1]['query'], db_engine)

    nome_tabela = sanitizar_nome_tabela("resultado_" + pergunta[:30])
    with db_engine.raw_connection() as conn:
        criar_tabela_materializada(conn, df, nome_tabela)

    print(f"\n📁 Tabela materializada criada: {nome_tabela}")

if __name__ == "__main__":
    main()
