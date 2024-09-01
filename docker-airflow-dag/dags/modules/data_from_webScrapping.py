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

def get_tickers():
    return {
        'bbva':'BBVA', 'santander':'SAN', 'jpmorgan':'JPM', 'goldman_sachs':'GSBD', 'citi':'C',
        'mercado_libre':'MELI', 'globant':'GLOB', 'ypf':'YPF', 'gurpo_financiero_galicia':'GGAL', 'banco_macro':'BMA',
        'tenaris':'TS', 'pampa_energía':'PAM', 'despegar':'DESP', 'cresud_sociedad_anonima':'CRESY', 'transportadora_de_gas':'TGS',
        'cemex':'CX', 'grupo_bimbo':'BIMBOA.MX', 'cocacola_femsa':'KOF'
    }
