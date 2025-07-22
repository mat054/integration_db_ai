from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.chat_models import ChatOpenAI
from config.settings import OPENAI_API_KEY, DB_URI

def criar_chain():
    # Cria um objeto de conexão SQL reconhecido pelo LangChain
    db = SQLDatabase.from_uri(DB_URI)

    # Cria um objeto da LLM da OpenAI
    llm = ChatOpenAI(
        temperature=0,
        openai_api_key=OPENAI_API_KEY
    )

    # Cria o toolkit SQL
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    # Cria o agente SQL que substitui o SQLDatabaseChain
    agent = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        return_intermediate_steps=True
    )

    return agent


# chain = criar_chain()
# resposta = chain.run("Quantas vendas foram feitas em janeiro?")

