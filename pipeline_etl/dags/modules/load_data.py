import psycopg2
from psycopg2 import sql
from parameters import POSTGRES_USERNAME, POSTGRES_PASSWORD, POSTGRES_DB, POSTGRES_PORT, POSTGRES_HOST
import pandas as pd
#from sqlalchemy import create_engine
import os


def load_data_to_db(file_path, table_name):
    
    # Extraer el nombre del archivo sin la extensión
    table_name = os.path.splitext(os.path.basename(file_path))[0]

    # Leer el archivo CSV en un DataFrame
    data = pd.read_csv(file_path)

    try:
        # Conexión a Amazon Redshift
        conn = psycopg2.connect(
            dbname=POSTGRES_DB,
            user=POSTGRES_USERNAME,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT
        )
        cursor = conn.cursor()

        # Crear la tabla si no existe
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            "Date" DATE,
            "Open" FLOAT,
            "High" FLOAT,
            "Low" FLOAT,
            "Close" FLOAT,
            "Volume" BIGINT,
            "Dividends" FLOAT,
            "Stock_Splits" FLOAT
        );
        """
        cursor.execute(create_table_query)
        conn.commit()

        # Inserción de datos usando Prepared Statements para mayor seguridad
        insert_query = f"""
            INSERT INTO {table_name} ("Date", "Open", "High", "Low", "Close", "Volume", "Dividends", "Stock_Splits")
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """


        # Insertar los datos por bloques (batch insert) para mejor rendimiento
        records = data[['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits']].values.tolist()
        cursor.executemany(insert_query, records)

        # Confirmar los cambios en la base de datos
        conn.commit()
        print(f"Datos cargados en la tabla {table_name} correctamente.")

    except psycopg2.Error as e:
        print(f"Error al cargar los datos en la base de datos: {e}")
    except Exception as e:
        print(f"Error general: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def load_all_data_from_directory(directory):
    dags_folder = os.path.dirname(os.path.abspath(__file__))
    directory_path = os.path.join(dags_folder, directory)

    for file_name in os.listdir(directory_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(directory_path, file_name)
            load_data_to_db(file_path)
