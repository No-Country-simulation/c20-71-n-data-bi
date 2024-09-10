import psycopg2
from config import REDSHIFT_CONFIG

def connect_to_redshift(config):
    try:
        conn = psycopg2.connect(
            host=config["HOST"],
            user=config["USER"],
            password=config["PASSWORD"],
            port=config["PORT"],
            dbname=config["DBNAME"]
        )
        print("Connected to Redshift successfully!")
        return conn
    except Exception as e:
        print(f"No fue posible conectar. Error: {e}")
        return None