import pandas as pd

def fetch_data_from_redshift(connection, query):
    try:
        df = pd.read_sql_query(query, connection)
        print(f"Extracción exitosa, hay {len(df)} líneas en la tabla.")
        return df
    except Exception as e:
        print(f"Error extraer la tabla: {e}")
        return None
