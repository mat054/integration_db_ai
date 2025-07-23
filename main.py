from chains.langchain_sql_chain import criar_chain
from sqlalchemy import create_engine
import pandas as pd
from config.settings import DB_URI, OPENAI_API_KEY
from sql_engine.materializer import criar_tabela_materializada
from utils.validators import sanitizar_nome_tabela
from utils.callbacks import SQLCapturerCallback, processar_resultado_para_dataframe
import re
import os
import json

def verificar_configuracoes():
    """Verifica se todas as configurações necessárias estão definidas"""
    print("Verificando configurações...")
    
    # Verificar variáveis de ambiente
    if not OPENAI_API_KEY:
        print("OPENAI_API_KEY não encontrada!")
        return False
    
    if not DB_URI:
        print("DB_URI não encontrada!")
        return False
    
    return True

def main():
    # Verificar configurações antes de prosseguir
    if not verificar_configuracoes():
        print("Falha na verificação das configurações.")
        return
    
    try:
        with open("prompts/system_prompt.txt", "r", encoding="utf-8") as f:
            pergunta = f.read()

        print("Prompt coletado!")
        
        print("Criando agente LangChain...")
        agent = criar_chain()
        print("Agente criado com sucesso!")
        
        # Criar callback para capturar SQL e resultados
        sql_capturer = SQLCapturerCallback()
        
        print("Executando consulta...")
        resultado = agent.invoke(
            {"input": pergunta},
            config={"callbacks": [sql_capturer]}
        )
        resposta = resultado["output"]

        print("Resposta coletada!")
        
        print("\n" + "="*50)
        print("RESPOSTA FINAL:")
        print("="*50)
        print(resposta)
        print("="*50)
        
        # Obter dados capturados
        dados_capturados = sql_capturer.get_ultimo_dados()
        
        if dados_capturados['sql']:
            print(f"\nSQL EXECUTADO:")
            print(dados_capturados['sql'])
            
            print(f"\nRESULTADO BRUTO:")
            print(dados_capturados['resultado_bruto'])
            
            # Converter para DataFrame
            print(f"\nCriando DataFrame...")
            df = processar_resultado_para_dataframe(dados_capturados['resultado_bruto'])
            print(f"DataFrame criado - Formato: {df.shape}")
            print(f"Colunas: {list(df.columns)}")
            print("\nPrimeiras linhas:")
            print(df.head())
            
            # Salvar dados para análise posterior
            print(f"\nSalvando arquivos...")
            
            # Salvar SQL
            with open("ultimo_sql.sql", "w", encoding="utf-8") as f:
                f.write(dados_capturados['sql'])
            
            # Salvar DataFrame
            df.to_csv("resultado_consulta.csv", index=False)
            df.to_json("resultado_consulta.json", orient="records", indent=2)
            
            # Salvar dados completos
            dados_completos = {
                'pergunta': pergunta.strip(),
                'resposta_final': resposta,
                'sql_executado': dados_capturados['sql'],
                'resultado_bruto': dados_capturados['resultado_bruto'],
                'dataframe_info': {
                    'shape': df.shape,
                    'columns': list(df.columns),
                    'data': df.to_dict('records')
                },
                'historico_consultas': dados_capturados['historico_completo']
            }
            
            with open("dados_completos.json", "w", encoding="utf-8") as f:
                json.dump(dados_completos, f, indent=2, ensure_ascii=False)
            
            print("Arquivos salvos: ultimo_sql.sql, resultado_consulta.csv, resultado_consulta.json, dados_completos.json")
            
        else:
            print("Nenhum SQL foi capturado durante a execução")

    except FileNotFoundError:
        print("Arquivo prompts/system_prompt.txt não encontrado!")
    except Exception as e:
        print(f"Erro durante execução: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
