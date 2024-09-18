import yfinance as yf
import datetime
import os
import logging
import pandas as pd

# Configuración del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        logging.info(f'Carpeta creada: {path}')
    else:
        logging.info(f'Carpeta ya existe: {path}')

def download_historical_data(ticker, start_date, end_date, output):
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(start=start_date, end=end_date)
        df = df.reset_index()
        df['Company'] = ticker  # Añadir columna de empresa
        df.to_csv(output, index=False)
        logging.info(f'Se ha guardado el dataset de {ticker}')
        return df
    except Exception as e:
        logging.error(f'Error al descargar datos para {ticker}: {e}')
        return None

def get_tickers():
    return {
        'ypf':'YPF', 'pampa_energia':'PAM', 'ecopetrol':'EC', 'petrobras':'PBR', 'interconexion_electrica':'IESFY',
        'minas_buenaventura':'BVN', 'eletrobras':'EBR', 'engie_brasil_energia':'EGIE3.SA', 'vista_energy':'VIST',
        'aes_andes':'AES'
    }

def main():
    # Crear directorio para los datasets si no existe
    current_dir = os.path.dirname(os.path.abspath(__file__))
    datasets_path = os.path.abspath(os.path.join(current_dir, '..', 'datasets'))
    create_directory(datasets_path)

    # Definir fechas de inicio y fin
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=365)  # Datos del último año

    all_data = []

    for company, ticker in get_tickers().items():
        output_file = os.path.join(datasets_path, f'{company}_stock_data.csv')
        df = download_historical_data(ticker, start_date, end_date, output_file)
        if df is not None:
            all_data.append(df)

    # Combinar todos los datos en un solo DataFrame
    if all_data:
        combined_data = pd.concat(all_data, ignore_index=True)
        combined_data.to_csv(os.path.join(datasets_path, 'latam_energy_stock_data.csv'), index=False)
        logging.info(f"Datos combinados guardados en '{os.path.join(datasets_path, 'latam_energy_stock_data.csv')}'")
    else:
        logging.warning("No se pudo descargar ningún dato")

if __name__ == "__main__":
    main()