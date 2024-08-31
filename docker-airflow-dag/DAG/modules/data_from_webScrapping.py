import yfinance as yf
import datetime
import os
import logging

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
        df.to_csv(output, index=False)
        logging.info(f'Se ha guardado el dataset de {ticker}')
    except Exception as e:
        logging.error(f'Error al descargar datos para {ticker}: {e}')

def main():
    # Configuración
    datasets_path = 'datasets/'
    tickers_dict = {
        'bbva':'BBVA', 'santander':'SAN', 'jpmorgan':'JPM', 'goldman_sachs':'GSBD', 'citi':'C',
        'mercado_libre':'MELI', 'globant':'GLOB', 'ypf':'YPF', 'gurpo_financiero_galicia':'GGAL', 'banco_macro':'BMA',
        'tenaris':'TS', 'pampa_energía':'PAM', 'despegar':'DESP', 'cresud_sociedad_anonima':'CRESY', 'transportadora_de_gas':'TGS',
        'cemex':'CX', 'grupo_bimbo':'BIMBOA.MX', 'cocacola_femsa':'KOF'
    }
    start_date = '2023-01-01'
    end_date = datetime.date.today().strftime('%Y-%m-%d')

    # Crear carpeta para datasets
    create_directory(datasets_path)

    # Descargar datos para cada ticker
    for key, ticker in tickers_dict.items():
        output_file = os.path.join(datasets_path, f'{key}_historical_data.csv')
        download_historical_data(ticker, start_date, end_date, output_file)

    logging.info(f'Datos actualizados hasta: {end_date}')

if __name__ == '__main__':
    main()
