import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os

# Verifica si existe una carpeta 'datasets2', si no existe la crea
if not os.path.exists('datasets2/'):
    os.makedirs('datasets2/')

def download_historical_data(ticker, start_date, end_date):
    # Crea el ticker
    stock = yf.Ticker(ticker)
    
    # Descarga los datos históricos
    df = stock.history(start=start_date, end=end_date)
    
    # Reinicia el índice para que las fechas sean columnas
    df = df.reset_index()
    
    # Convierte la columna 'Date' a datetime si no lo está ya
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Selecciona solo las columnas que necesitamos
    df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
    
    return df

# Diccionario actualizado de nombres de empresas de energía con su ticker
tickers_dict = {
    'petrobras': 'PBR',
    'ecopetrol': 'EC',
    'eletrobras': 'EBR',
    'cemig': 'CIG',
    'pampa_energia': 'PAM',
    'ypf': 'YPF',
    'enel_chile': 'ENIC',
    'companhia_paranaense_de_energia': 'ELP',
    'centrais_eletricas_brasileiras': 'EBR',
    'geopark': 'GPRK',
    'vista_energy': 'VIST',
    'transportadora_de_gas_del_sur': 'TGS',
    'ultrapar_participacoes': 'UGP',
    'central_puerto': 'CEPU',
    'companhia_de_transmissao_de_energia_eletrica_paulista': 'CTPZY',
    'eneva': 'ENVAF',
    'grupo_energia_bogota': 'GGBR4.SA',
    'aes_brasil': 'AESB3.SA',
    'cosan': 'CSAN3.SA',
    'engie_brasil': 'EGIE3.SA'
}

# Calcula las fechas de inicio y fin (últimos 30 días)
end_date = datetime.now()
start_date = end_date - timedelta(days=30)

# Convertir las fechas a formato string
start_date_str = start_date.strftime('%Y-%m-%d')
end_date_str = end_date.strftime('%Y-%m-%d')

# Dataframe para almacenar todos los datos
all_data = pd.DataFrame()

# Ciclo para iterar sobre todas las empresas de energía
for company, ticker in tickers_dict.items():
    try:
        df = download_historical_data(ticker, start_date_str, end_date_str)
        df['Company'] = company
        df['Ticker'] = ticker
        all_data = pd.concat([all_data, df], ignore_index=True)
        print(f'Se han descargado los datos de {company}')
    except Exception as e:
        print(f'Error al descargar datos de {company}: {e}')

# Guardar todos los datos en un solo archivo CSV en la carpeta datasets2
output_file = 'datasets2/latam_energy_companies_stock_data.csv'
all_data.to_csv(output_file, index=False)
print(f'Se han guardado todos los datos en {output_file}')
print(f'Datos actualizados hasta: {end_date_str}')