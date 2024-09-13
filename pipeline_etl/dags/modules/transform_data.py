import pandas as pd
import os
import logging

# Configuración del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def transform_data(file_path):
    """Reemplaza los valores vacíos o nulos en una de las columnas con el dato del día anterior."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"El archivo {file_path} no existe.")
    
    try:
        # Leer el archivo CSV en un DataFrame
        data = pd.read_csv(file_path)
        
        # Reemplazar valores nulos en la columna 'Close' con el valor del día anterior
        data['Close'].fillna(method='ffill', inplace=True)
        
        # Guardar los datos transformados
        data.to_csv(file_path, index=False)
        logging.info(f"Datos transformados y guardados en {file_path}")
        
        return file_path  # Retornar la ruta del archivo para usar con XCom
    except Exception as e:
        logging.error(f"Error al transformar los datos en {file_path}: {e}")
        raise

def transform_all_data(directory):
    """Aplica la transformación a todos los archivos CSV en el directorio dado."""
    dags_folder = os.path.dirname(os.path.abspath(__file__))
    directory_path = os.path.join(dags_folder, directory)

    for file_name in os.listdir(directory_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(directory_path, file_name)
            transform_data(file_path)
