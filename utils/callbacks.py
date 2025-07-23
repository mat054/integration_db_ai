import json
import pandas as pd
from typing import Dict, List, Any
from langchain.callbacks.base import BaseCallbackHandler

class SQLCapturerCallback(BaseCallbackHandler):
    """Callback customizado para capturar SQL queries e resultados"""
    
    def __init__(self):
        self.queries_executadas = []
        self.resultados_brutos = []
        self.ultimo_sql = None
        self.ultimo_resultado = None

    def on_tool_start(self, serialized: Dict[str, Any], input_str: str, **kwargs) -> None:
        """Captura quando uma tool SQL é chamada"""
        tool_name = serialized.get("name", "")
        
        if "sql_db_query" in tool_name or "query" in tool_name.lower():
            # Extrai o SQL da string de input
            sql_query = input_str.strip()
            self.ultimo_sql = sql_query
            self.queries_executadas.append(sql_query)

    def on_tool_end(self, output: str, **kwargs) -> None:
        """Captura o resultado da execução SQL"""
        if self.ultimo_sql and output:
            self.ultimo_resultado = output
            self.resultados_brutos.append({
                'sql': self.ultimo_sql,
                'resultado_bruto': output
            })

    def get_ultimo_dados(self):
        """Retorna os últimos dados capturados"""
        return {
            'sql': self.ultimo_sql,
            'resultado_bruto': self.ultimo_resultado,
            'historico_completo': self.resultados_brutos
        }

def processar_resultado_para_dataframe(resultado_bruto: str) -> pd.DataFrame:
    """Converte resultado SQL bruto em DataFrame"""
    try:
        # Tenta interpretar como lista de tuplas primeiro
        if resultado_bruto.startswith('[') and resultado_bruto.endswith(']'):
            dados = eval(resultado_bruto)
            
            if dados and isinstance(dados[0], tuple):
                # Se são tuplas, converte para DataFrame
                df = pd.DataFrame(dados)
                return df
            elif dados and isinstance(dados[0], dict):
                # Se são dicionários, converte diretamente
                df = pd.DataFrame(dados)
                return df
        
        # Tenta JSON
        try:
            dados_json = json.loads(resultado_bruto)
            df = pd.DataFrame(dados_json)
            return df
        except:
            pass
        
        # Fallback: retorna DataFrame com resultado como string
        df = pd.DataFrame({'resultado': [resultado_bruto]})
        return df
        
    except Exception as e:
        print(f"Erro ao converter para DataFrame: {e}")
        return pd.DataFrame({'resultado_bruto': [resultado_bruto]}) 