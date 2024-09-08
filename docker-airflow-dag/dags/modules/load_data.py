import psycopg2
from psycopg2 import sql
from parameters import POSTGRES_USERNAME, POSTGRES_PASSWORD, POSTGRES_DB, POSTGRES_PORT, POSTGRES_HOST
import pandas as pd
#from sqlalchemy import create_engine
import os
# def load_data_to_db(data, table_name):
#     try:
#         # Conexión a la base de datos PostgreSQL
#         conn = psycopg2.connect(
#             dbname=POSTGRES_DB,
#             user=POSTGRES_USERNAME,
#             password=POSTGRES_PASSWORD,
#             host="localhost",  # Cambia según sea necesario
#             port=POSTGRES_PORT
#         )
#         cursor = conn.cursor()

#         # Cargar los datos en la tabla correspondiente
#         for i, row in data.iterrows():
#             columns = list(row.index)
#             values = [row[col] for col in columns]

#             insert = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
#                 sql.Identifier(table_name),
#                 sql.SQL(', ').join(map(sql.Identifier, columns)),
#                 sql.SQL(', ').join(sql.Placeholder() * len(values))
#             )

#             cursor.execute(insert, values)

#         conn.commit()
#         cursor.close()
#         conn.close()
#         print(f"Datos cargados en la tabla {table_name} correctamente.")

#     except psycopg2.Error as e:
#         print(f"Error al cargar los datos en la base de datos: {e}")
#     except Exception as e:
#         print(f"Error general: {e}")

# Ejemplo de uso
# load_data_to_db(cleaned_data, 'nombre_de_la_tabla')



# def load_data_to_db(file_path):
#     # Extraer el nombre del archivo sin la extensión
#     table_name = os.path.splitext(os.path.basename(file_path))[0]

#     # Leer el archivo CSV en un DataFrame
#     data = pd.read_csv(file_path)

#     # Crear la conexión a la base de datos
#     conn_string = f"postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
#     engine = create_engine(conn_string)

#     # Cargar los datos en la base de datos en una tabla con el nombre de la empresa
#     try:
#         data.to_sql(table_name, engine, if_exists='replace', index=False)
#         print(f"Datos cargados en la tabla {table_name} correctamente.")
#     except Exception as e:
#         print(f"Error al cargar datos: {e}")

def load_data_to_db(file_path):
    # Extraer el nombre del archivo sin la extensión
    table_name = os.path.splitext(os.path.basename(file_path))[0]

    # Leer el archivo CSV en un DataFrame
    data = pd.read_csv(file_path)

    # Crear la conexión a Amazon Redshift
    try:
        conn = psycopg2.connect(
            dbname=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT
        )
        cursor = conn.cursor()

        # Crear la tabla si no existe
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            Date DATE,
            Open FLOAT,
            High FLOAT,
            Low FLOAT,
            Close FLOAT,
            Volume BIGINT,
            Dividends FLOAT,
            Stock_Splits FLOAT
        );
        """
        cursor.execute(create_table_query)

        # Insertar los datos fila por fila
        for index, row in data.iterrows():
            insert_query = f"""
            INSERT INTO {table_name} (Date, Open, High, Low, Close, Volume, Dividends, Stock_Splits)
            VALUES ('{row['Date']}', {row['Open']}, {row['High']}, {row['Low']}, {row['Close']}, {row['Volume']}, {row['Dividends']}, {row['Stock Splits']});
            """
            cursor.execute(insert_query)

        conn.commit()
        cursor.close()
        conn.close()
        print(f"Datos cargados en la tabla {table_name} correctamente.")
    
    except Exception as e:
        print(f"Error al cargar datos: {e}")


def load_all_data_from_directory(directory):
    dags_folder = os.path.dirname(os.path.abspath(__file__))
    directory_path = os.path.join(dags_folder, directory)

    for file_name in os.listdir(directory_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(directory_path, file_name)
            load_data_to_db(file_path)
