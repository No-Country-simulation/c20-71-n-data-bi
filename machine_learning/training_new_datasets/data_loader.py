import pandas as pd
import os, sys
sys.path.append(os.getcwd)

# Función para cargar los datos del archivo CSV
def load_data(file_path):
    df = pd.read_csv(file_path)
    
    # Convierte la columna Date en un datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Convierte la columna Date en el index y lo ordena. Esto asegura que el dataset está ordena de forma descendente
    df.set_index('Date', inplace=True)
    df.sort_index(inplace=True)
    
    return df

df = load_data('datasets_modelo/3r_petroleum_model_data.csv')
print(df.head(5))