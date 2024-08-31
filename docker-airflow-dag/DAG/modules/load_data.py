# import psycopg2
# from psycopg2 import sql
from modules.parameters import POSTGRES_USERNAME, POSTGRES_PASSWORD, POSTGRES_DB, POSTGRES_PORT
import pandas as pd
from sqlalchemy import create_engine
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



def load_data_to_db(file_path):
    # Extraer el nombre del archivo sin la extensión
    table_name = os.path.splitext(os.path.basename(file_path))[0]

    # Leer el archivo CSV en un DataFrame
    data = pd.read_csv(file_path)

    # Crear la conexión a la base de datos
    conn_string = f"postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@localhost:{POSTGRES_PORT}/{POSTGRES_DB}"
    engine = create_engine(conn_string)

    # Cargar los datos en la base de datos en una tabla con el nombre de la empresa
    try:
        data.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"Datos cargados en la tabla {table_name} correctamente.")
    except Exception as e:
        print(f"Error al cargar datos: {e}")

# Función para cargar todos los archivos CSV en la carpeta datasets
def load_all_data_from_directory(directory):
    for file_name in os.listdir(directory):
        if file_name.endswith('.csv'):
            file_path = os.path.join(directory, file_name)
            load_data_to_db(file_path)
