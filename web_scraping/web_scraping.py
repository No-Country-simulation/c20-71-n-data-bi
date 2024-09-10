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

# Diccionario de nombres de bancos con su ticker
tickers_dict = {
    'banco_santander_brasil': 'BSBR',
    'banco_de_chile': 'BCH',
    'credicorp': 'BAP',
    'grupo_financiero_galicia': 'GGAL',
    'banco_macro': 'BMA',
    'bbva_argentina': 'BBAR',
    'grupo_aval': 'AVAL',
    'bancolombia': 'CIB',
    'grupo_financiero_banorte': 'GBOOY',
    'banco_inter': 'INTR',
    'xp_inc': 'XP',
    'nu_holdings': 'NU',
    'banco_santander_chile': 'BSAC',
    'grupo_supervielle': 'SUPV',
    'banco_latinoamericano_comercio_exterior': 'BLX',
    'stone_co': 'STNE',
    'pagseguro_digital': 'PAGS',
    'mercadolibre': 'MELI',
    'banco_de_bogota': 'BOGOTA.CL',
    'banco_hipotecario': 'BHIP.BA',
    'banco_de_valores': 'VALO.BA',
    'banco_patagonia': 'BPAT.BA',
    'banco_santander_rio': 'BRIO.BA'
}

# Calcula las fechas de inicio y fin (últimos 30 días)
end_date = datetime.now()
start_date = end_date - timedelta(days=30)

# Convertir las fechas a formato string
start_date_str = start_date.strftime('%Y-%m-%d')
end_date_str = end_date.strftime('%Y-%m-%d')

# Dataframe para almacenar todos los datos
all_data = pd.DataFrame()

# Ciclo para iterar sobre todos los bancos
for bank, ticker in tickers_dict.items():
    try:
        df = download_historical_data(ticker, start_date_str, end_date_str)
        if df is not None and not df.empty:
            df['Bank'] = bank
            df['Ticker'] = ticker
            all_data = pd.concat([all_data, df], ignore_index=True)
            print(f'Se han descargado los datos de {bank} ({ticker})')
        else:
            print(f'No se encontraron datos para {bank} ({ticker})')
    except Exception as e:
        print(f'Error al descargar datos de {bank} ({ticker}): {e}')

# Guardar todos los datos en un solo archivo CSV en la carpeta datasets2
if not all_data.empty:
    output_file = 'datasets2/latam_banks_stock_data.csv'
    all_data.to_csv(output_file, index=False)
    print(f'Se han guardado todos los datos en {output_file}')
    print(f'Datos actualizados hasta: {end_date_str}')
else:
    print('No se pudieron obtener datos para ningún banco.')