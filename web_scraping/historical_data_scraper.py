import yfinance as yf
import datetime
import os
import sys
sys.path.append(os.getcwd())

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
    df.to_csv(output, index=False)
    
# Diccionario de nombres de empresas con su NYSE
tickers_dict = {'bbva':'BBVA', 'santander':'SAN', 'jpmorgan':'JPM', 'goldman_sachs':'GSBD', 'citi':'C',
                'mercado_libre':'MELI', 'globant':'GLOB', 'ypf':'YPF', 'gurpo_financiero_galicia':'GGAL', 'banco_macro':'BMA',
                'tenaris':'TS', 'pampa_energía':'PAM', 'despegar':'DESP', 'cresud_sociedad_anonima':'CRESY', 'transportadora_de_gas':'TGS',
                'cemex':'CX', 'grupo_bimbo':'BIMBOA.MX', 'cocacola_femsa':'KOF'
                }

# Fecha de inicio fija
start_date = '2023-01-01'

# Fecha de fin se actualiza a la fecha actual
end_date = datetime.date.today().strftime('%Y-%m-%d')

# Ciclo para iterar sobre todas las empresas
for key, ticker in tickers_dict.items():
    output_file = f'datasets/{key}_historical_data.csv'
    download_historical_data(ticker, start_date, end_date, output_file)
    print(f'Se ha guardado el dataset de {key}')

print(f'Datos actualizados hasta: {end_date}')