import pandas as pd

def criar_tabela_materializada(conn, df: pd.DataFrame, nome_tabela: str):
    with conn.cursor() as cur:
        colunas = ", ".join(f"{col} TEXT" for col in df.columns)
        cur.execute(f"DROP TABLE IF EXISTS {nome_tabela}")
        cur.execute(f"CREATE TABLE {nome_tabela} ({colunas})")

        for _, row in df.iterrows():
            values = tuple(str(v) for v in row)
            placeholders = ", ".join(["%s"] * len(values))
            cur.execute(f"INSERT INTO {nome_tabela} VALUES ({placeholders})", values)

    conn.commit()
