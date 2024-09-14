# from dotenv import load_dotenv
import os
import logging
from parameters import POSTGRES_USERNAME, POSTGRES_PASSWORD, POSTGRES_DB, POSTGRES_PORT, POSTGRES_HOST

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Cargar variables de entorno desde .env
# dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
# load_dotenv(dotenv_path)

def validate_credentials():
    credentials = {
        "POSTGRES_USERNAME": POSTGRES_USERNAME, #os.getenv('POSTGRES_USERNAME'),
        "POSTGRES_PASSWORD":POSTGRES_PASSWORD, #os.getenv('POSTGRES_PASSWORD'),
        "POSTGRES_DB":POSTGRES_DB, #os.getenv('POSTGRES_DB'),
        "POSTGRES_PORT":POSTGRES_PORT, #os.getenv('POSTGRES_PORT'),
        "POSTGRES_HOST":POSTGRES_HOST #os.getenv('POSTGRES_HOST')
    }

    for key, value in credentials.items():
        if not value or value == '':
            logging.error(f"Error: {key} is not set properly.")
            raise EnvironmentError(f"{key} is not set properly.")
    
    logging.info("All credentials are set properly.")
    return True
