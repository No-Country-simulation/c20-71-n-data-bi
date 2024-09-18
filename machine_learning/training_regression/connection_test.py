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
        print(f"Unable to connect to Redshift. Error: {e}")
        return None

# Establish the connection
connection = connect_to_redshift(REDSHIFT_CONFIG)

if connection:
    # Perform operations with the connection here
    cursor = connection.cursor()
    cursor.execute("SELECT VERSION()")
    version = cursor.fetchone()
    print(f"Connected to: {version[0]}")

    # Don't forget to close the connection when you're done
    cursor.close()
    connection.close()
    print("Connection closed.")