import re

def sanitizar_nome_tabela(nome: str) -> str:
    return re.sub(r'[^a-zA-Z0-9_]', '_', nome.lower())
