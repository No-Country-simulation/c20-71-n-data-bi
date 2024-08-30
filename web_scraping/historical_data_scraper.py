import yfinance as yf
import datetime as datetime
import os, sys
sys.path.append(os.getcwd)

# Verifica si existe una carpeta 'datasets', si no existe la crea
if not os.path.exists('datasets/'):
    os.makedirs('datasets/')

def download_historical_data(ticker, start_date, end_date, output):
    # Crea el ticker
    stock = yf.Ticker(ticker)
    
    # Descarga los datos históricos
    df = stock.history(start=start_date, end=end_date)
    
    # Reinicia el índice para que las fechas sean columnas
    df = df.reset_index()
    
    # Guarda el dataset
    output
    df.to_csv(output, index=False)
    
# Diccionario de nombres de empresas con su NYSE
tickers_dict = {'bbva':'BBVA', 'santander':'SAN', 'jpmorgan':'JPM', 'goldman_sachs':'GSBD', 'citi':'C',
                'mercado_libre':'MELI', 'globant':'GLOB', 'ypf':'YPF', 'gurpo_financiero_galicia':'GGAL', 'banco_macro':'BMA',
                'tenaris':'TS', 'pampa_energía':'PAM', 'despegar':'DESP', 'cresud_sociedad_anonima':'CRESY', 'transportadora_de_gas':'TGS',
                'cemex':'CX', 'grupo_bimbo':'BIMBOA.MX', 'cocacola_femsa':'KOF'
                }

start_date = '2023-01-01'
end_date = '2024-08-30'

# Ciclo para iterar sobre todas las empresas
for key, ticker in tickers_dict.items():
    output_file = f'datasets/{key}_historical_data.csv'
    download_historical_data(ticker, start_date, end_date, output_file)
    print(f'se ha guardado el dataset de {key}')