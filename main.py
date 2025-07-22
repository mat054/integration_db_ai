from chains.langchain_sql_chain import criar_chain
from sqlalchemy import create_engine
import pandas as pd
from config.settings import DB_URI
from sql_engine.materializer import criar_tabela_materializada
from utils.validators import sanitizar_nome_tabela
import re

def main():
    with open("prompts/system_prompt.txt", "r", encoding="utf-8") as f:
        pergunta = f.read()
    
    agent = criar_chain()

    # Usar invoke em vez de run (método atualizado)
    resultado = agent.invoke({"input": pergunta})
    resposta = resultado["output"]
    
    print("\n✅ Resposta da LLM + SQL executada com sucesso:\n")
    print(resposta)

    # Extrair a query SQL da resposta ou usar uma query padrão
    try:
        db_engine = create_engine(DB_URI)
        
        # Tentar extrair a query SQL da resposta
        # Procurar por padrões de SQL na resposta
        sql_pattern = r'SELECT.*?FROM.*?(?:WHERE.*?)?(?:ORDER BY.*?)?(?:LIMIT.*?)?;?'
        sql_matches = re.findall(sql_pattern, resposta, re.IGNORECASE | re.DOTALL)
        
        if sql_matches:
            query_sql = sql_matches[-1].strip()  # Pegar a última query encontrada
            print(f"\n🔍 Query SQL extraída: {query_sql}")
        else:
            # Se não encontrar SQL na resposta, usar uma query padrão baseada na pergunta
            if "townhome" in pergunta.lower() or "single family" in pergunta.lower() or "apartment" in pergunta.lower():
                query_sql = 'SELECT COUNT(*) FROM test_1 WHERE "hdpData/homeInfo/homeType" IN (\'TOWNHOME\', \'SINGLE_FAMILY\', \'APARTMENT\')'
            else:
                query_sql = 'SELECT * FROM test_1 LIMIT 10'
            print(f"\n🔍 Usando query padrão: {query_sql}")
        
        df = pd.read_sql(query_sql, db_engine)
        
        # Salvar CSV
        nome_arquivo = f"resultado_{pergunta[:20].replace(' ', '_')}.csv"
        df.to_csv(nome_arquivo, index=False)
        print(f"\n📁 Arquivo CSV salvo: {nome_arquivo}")
        
        # Mostrar primeiras linhas do resultado
        print(f"\n📊 Primeiras linhas do resultado:")
        print(df.head())
        
    except Exception as e:
        print(f"❌ Erro ao processar dados: {e}")
        return

if __name__ == "__main__":
    main()
