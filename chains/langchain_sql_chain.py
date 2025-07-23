from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_openai import ChatOpenAI  # Versão atualizada
from config.settings import OPENAI_API_KEY, DB_URI

def criar_chain():
    try:
        # Cria um objeto de conexão SQL reconhecido pelo LangChain
        db = SQLDatabase.from_uri(DB_URI)

        # Cria um objeto da LLM da OpenAI (versão atualizada)
        llm = ChatOpenAI(
            temperature=0,
            api_key=OPENAI_API_KEY,  # Parâmetro atualizado
            model="gpt-3.5-turbo"  # Especificar modelo explicitamente
        )

        # Cria o toolkit SQL
        toolkit = SQLDatabaseToolkit(db=db, llm=llm)

        # Cria o agente SQL que substitui o SQLDatabaseChain
        agent = create_sql_agent(
            llm=llm,
            toolkit=toolkit,
            verbose=True,
            return_intermediate_steps=True,
            agent_type="openai-tools"  # Especificar tipo do agente
        )

        return agent

    except Exception as e:
        print(f"Erro ao criar agente: {e}")
        
        # Diagnóstico específico para diferentes tipos de erro
        if "connection" in str(e).lower() or "timeout" in str(e).lower():
            print("Possíveis soluções para erro de conexão:")
            print("  1. Verifique se o banco de dados está online")
            print("  2. Confirme as credenciais no DB_URI")
            print("  3. Verifique sua conexão com internet")
            print("  4. Teste se consegue conectar diretamente ao banco")
        
        elif "api" in str(e).lower() or "openai" in str(e).lower():
            print("Possíveis soluções para erro da OpenAI:")
            print("  1. Verifique se OPENAI_API_KEY está correto")
            print("  2. Confirme se há créditos na conta OpenAI")
            print("  3. Teste a chave em https://platform.openai.com/")
        
        raise  # Re-raise o erro para ser capturado no main






