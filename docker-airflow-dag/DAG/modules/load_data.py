import psycopg2
from psycopg2 import sql
from modules.parameters import POSTGRES_USERNAME, POSTGRES_PASSWORD, POSTGRES_DB, POSTGRES_PORT

def load_data_to_db(data, table_name):
    try:
        # Conexión a la base de datos PostgreSQL
        conn = psycopg2.connect(
            dbname=POSTGRES_DB,
            user=POSTGRES_USERNAME,
            password=POSTGRES_PASSWORD,
            host="localhost",  # Cambia según sea necesario
            port=POSTGRES_PORT
        )
        cursor = conn.cursor()

        # Cargar los datos en la tabla correspondiente
        for i, row in data.iterrows():
            columns = list(row.index)
            values = [row[col] for col in columns]

            insert = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
                sql.Identifier(table_name),
                sql.SQL(', ').join(map(sql.Identifier, columns)),
                sql.SQL(', ').join(sql.Placeholder() * len(values))
            )

            cursor.execute(insert, values)

        conn.commit()
        cursor.close()
        conn.close()
        print(f"Datos cargados en la tabla {table_name} correctamente.")

    except psycopg2.Error as e:
        print(f"Error al cargar los datos en la base de datos: {e}")
    except Exception as e:
        print(f"Error general: {e}")

# Ejemplo de uso
# load_data_to_db(cleaned_data, 'nombre_de_la_tabla')
