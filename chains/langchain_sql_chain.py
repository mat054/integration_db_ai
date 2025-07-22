from langchain.chains import SQLDatabaseChain
from langchain.chat_models import ChatOpenAI
from langchain.sql_database import SQLDatabase
from config.settings import OPENAI_API_KEY, DB_URI

def criar_chain():
    # Cria um objeto de conexão SQL reconhecido pelo LangChain
    db = SQLDatabase.from_uri(DB_URI)

    # Cria um objeto da LLM da OpenAI
    llm = ChatOpenAI(
        temperature=0,
        openai_api_key=OPENAI_API_KEY
    )

    # Cria a "cadeia inteligente" que conecta a LLM ao banco
    chain = SQLDatabaseChain.from_llm(
        llm=llm,
        db=db,
        verbose=True,
        return_intermediate_steps=True
    )

    return chain


# chain = criar_chain()
# resposta = chain.run("Quantas vendas foram feitas em janeiro?")

