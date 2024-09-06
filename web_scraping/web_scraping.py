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

# Diccionario de nombres de empresas con su ticker
tickers_dict = {
    'ypf':'YPF', 'pampa_energía':'PAM', 'ecopetrol':'EC', 'petrobras':'PBR', 
    'interconexion_electrica':'IESFY', 'minas_buenaventura':'BVN', 'eletrobras':'EBR', 
    'engie_brasil_energia':'EGIE3.SA', 'vista_energy':'VIST', 'eas_andes':'AES'
}

# Calcula las fechas de inicio y fin (últimos 30 días)
end_date = datetime.now()
start_date = end_date - timedelta(days=30)

# Convertir las fechas a formato string
start_date_str = start_date.strftime('%Y-%m-%d')
end_date_str = end_date.strftime('%Y-%m-%d')

# Dataframe para almacenar todos los datos
all_data = pd.DataFrame()

# Ciclo para iterar sobre todas las empresas
for company, ticker in tickers_dict.items():
    df = download_historical_data(ticker, start_date_str, end_date_str)
    df['Company'] = company
    df['Ticker'] = ticker
    all_data = pd.concat([all_data, df], ignore_index=True)
    print(f'Se han descargado los datos de {company}')

# Guardar todos los datos en un solo archivo CSV en la carpeta datasets2
output_file = 'datasets2/all_companies_stock_data.csv'
all_data.to_csv(output_file, index=False)
print(f'Se han guardado todos los datos en {output_file}')
print(f'Datos actualizados hasta: {end_date_str}')