# integration_db_ai


## Estrutura do projeto

```graphql
llm_sql_materializer/
│
├── config/
│   └── settings.py               # Configurações do banco e API
│
├── chains/
│   └── langchain_sql_chain.py   # Criação e uso do SQLDatabaseChain
│
├── sql_engine/
│   └── materializer.py          # Continua responsável por salvar resultado
│
├── utils/
│   └── validators.py            # Validação de nomes de tabelas
│
├── prompts/
│   └── system_prompt.txt        # Prompt customizado (opcional)
│
├── main.py                      # Entrada principal
├── requirements.txt
└── README.md


```