from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import logging
import os

# Importar funciones desde los módulos
from modules.data_from_webScrapping import create_directory, download_historical_data, get_tickers
from modules.extract_data import extract_data
from modules.clean_data import clean_dataset
from modules.load_data import load_data_to_db
from modules.validate_credentials import validate_credentials
from dotenv import load_dotenv

load_dotenv()  # Corrección del error tipográfico

# Funciones de la pipeline

def download_all_data(**kwargs):
    datasets_path = 'datasets/'
    tickers_dict = get_tickers()
    start_date = '2023-01-01'
    end_date = datetime.today().strftime('%Y-%m-%d')

    # Crear carpeta para datasets
    create_directory(datasets_path)

    # Descargar datos para cada ticker
    for key, ticker in tickers_dict.items():
        output_file = os.path.join(datasets_path, f'{key}_historical_data.csv')
        download_historical_data(ticker, start_date, end_date, output_file)

def validate_credentials_task(**kwargs):
    if not validate_credentials():
        raise ValueError("Las credenciales no están configuradas correctamente.")

def extract_data_task(**kwargs):
    directory = kwargs['file_path']
    all_data = []
    for file_name in os.listdir(directory):
        if file_name.endswith('.csv'):
            file_path = os.path.join(directory, file_name)
            data = extract_data(file_path)
            all_data.append(data)
    return all_data

def clean_data_task(**kwargs):
    data = kwargs['task_instance'].xcom_pull(task_ids='extract_data')
    return clean_dataset(data)

def load_data_task(**kwargs):
    directory = 'datasets'
    for file_name in os.listdir(directory):
        if file_name.endswith('.csv'):
            file_path = os.path.join(directory, file_name)
            load_data_to_db(file_path)
            logging.info(f'Datos cargados en la tabla para el archivo {file_name}')

# Configuración del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Definir el DAG
default_args = {
    'owner': 'C20-71-N-DATA-BI',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
}

dag = DAG(
    'etl_pipeline',
    default_args=default_args,
    description='Pipeline ETL',
    schedule_interval='@daily',
)

# Tareas en el DAG

validate_credentials_op = PythonOperator(
    task_id='validate_credentials',
    python_callable=validate_credentials_task,
    dag=dag,
)

download_data_op = PythonOperator(
    task_id='download_data',
    python_callable=download_all_data,
    dag=dag,
)

extract_data_op = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data_task,
    op_kwargs={'file_path': 'datasets'},
    dag=dag,
)

clean_data_op = PythonOperator(
    task_id='clean_data',
    python_callable=clean_data_task,
    dag=dag,
)

load_data_op = PythonOperator(
    task_id='load_data',
    python_callable=load_data_task,
    dag=dag,
)

# Definir la secuencia de tareas
validate_credentials_op >> download_data_op >> extract_data_op >> clean_data_op >> load_data_op

