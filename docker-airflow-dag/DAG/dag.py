from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import logging

# Importar funciones desde los módulos
from modules.data_from_webScrapping import download_historical_data
from modules.extract_data import extract_data
from modules.data_transformation import transform_data
from modules.clean_data import clean_dataset
from modules.load_data import load_data_to_db
from modules.validate_credentials import validate_credentials
from dotenv

loead_dotenv()

# Funciones de la pipeline

def download_data_task(**kwargs):
    tickers_dict = {'bbva':'BBVA', 'santander':'SAN', 'jpmorgan':'JPM', 'goldman_sachs':'GSBD', 'citi':'C',
                    'mercado_libre':'MELI', 'globant':'GLOB', 'ypf':'YPF', 'gurpo_financiero_galicia':'GGAL', 'banco_macro':'BMA',
                    'tenaris':'TS', 'pampa_energía':'PAM', 'despegar':'DESP', 'cresud_sociedad_anonima':'CRESY', 'transportadora_de_gas':'TGS',
                    'cemex':'CX', 'grupo_bimbo':'BIMBOA.MX', 'cocacola_femsa':'KOF'
                    }
    
    start_date = '2023-01-01'
    end_date = datetime.today().strftime('%Y-%m-%d')
    
    for key, ticker in tickers_dict.items():
        output_file = f'datasets/{key}_historical_data.csv'
        download_historical_data(ticker, start_date, end_date, output_file)
        logging.info(f'Se ha guardado el dataset de {key}')

def validate_credentials_task(**kwargs):
    if not validate_credentials():
        raise ValueError("Las credenciales no están configuradas correctamente.")

def extract_data_task(**kwargs):
    file_path = kwargs['file_path']
    return extract_data(file_path)

def transform_data_task(**kwargs):
    data = kwargs['task_instance'].xcom_pull(task_ids='extract_data')
    return transform_data(data)

def clean_data_task(**kwargs):
    data = kwargs['task_instance'].xcom_pull(task_ids='transform_data')
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
    python_callable=download_data_task,
    dag=dag,
)

extract_data_op = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data_task,
    op_kwargs={'directory': 'datasets'},
    dag=dag,
)

transform_data_op = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data_task,
    provide_context=True,
    dag=dag,
)

clean_data_op = PythonOperator(
    task_id='clean_data',
    python_callable=clean_data_task,
    provide_context=True,
    dag=dag,
)

load_data_op = PythonOperator(
    task_id='load_data',
    python_callable=load_data_task,
    provide_context=True,
    dag=dag,
)

# Definir la secuencia de tareas
validate_credentials_op >> download_data_op >> extract_data_op >> transform_data_op >> clean_data_op >> load_data_op
