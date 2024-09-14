import psycopg2
import os, sys
sys.path.append(os.getcwd)

from training.config import REDSHIFT_CONFIG

def connect_to_redshift(config):
    try:
        conn = psycopg2.connect(
            host=config["HOST"],
            user=config["USER"],
            password=config["PASSWORD"],
            port=config["PORT"],
            dbname=config["DBNAME"]
        )
        print("Conexión exitosa")
        return conn
    except Exception as e:
        print(f"No fue posible conectar. Error: {e}")
        return None