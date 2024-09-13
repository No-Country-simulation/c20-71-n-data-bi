import yfinance as yf
import datetime
import os
import sys
import pandas as pd
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
    
    # Guarda el dataset en formato CSV
    df.to_csv(output, index=False)
    
# Diccionario de nombres de empresas con su símbolo en NYSE
tickers_dict = {
    'ypf': 'YPF',  # Argentina - Petróleo y gas
    'pampa_energia': 'PAM',  # Argentina - Energía integrada
    'ecopetrol': 'EC',  # Colombia - Petróleo y gas
    'petrobras': 'PBR',  # Brasil - Petróleo y gas
    'interconexion_electrica': 'IESFY',  # Colombia - Transmisión de energía
    'eletrobras': 'EBR',  # Brasil - Generación y transmisión de energía
    'engie_brasil_energia': 'EGIE3.SA',  # Brasil - Generación y distribución de energía
    'vista_energy': 'VIST',  # Argentina - Petróleo y gas
    'aes_andes': 'AES',  # Chile - Generación de energía
    'cemig': 'CIG',  # Brasil - Generación y distribución de energía
    'copel': 'ELP',  # Brasil - Generación y distribución de energía
    'enel_chile': 'ENIC',  # Chile - Generación y distribución de energía
    'cosan': 'CSAN',  # Brasil - Energía y logística
    'ultrapar': 'UGP',  # Brasil - Distribución de combustibles
    'companhia_siderurgica_nacional': 'SID',  # Brasil - Acero y minería (con componente energético)
    'vale': 'VALE',  # Brasil - Minería (importante en el sector energético)
    'braskem': 'BAK',  # Brasil - Petroquímica
    'centrais_eletricas_brasileiras': 'EBR',  # Brasil - Generación y transmisión de energía
    'companhia_paranaense_de_energia': 'ELP',  # Brasil - Generación y distribución de energía
    'light': 'LGSXY',  # Brasil - Distribución de energía
    'transmissora_alianca_de_energia_eletrica': 'TAEE11.SA',  # Brasil - Transmisión de energía
    'alupar_investimento': 'ALUP11.SA',  # Brasil - Transmisión de energía
    'eneva': 'ENEV3.SA',  # Brasil - Generación de energía
    'raizen': 'RAIZ4.SA',  # Brasil - Biocombustibles y distribución
    'petrorio': 'PRIO3.SA',  # Brasil - Petróleo y gas
    '3r_petroleum': 'RRRP3.SA',  # Brasil - Petróleo y gas
    'enauta_participacoes': 'ENAT3.SA',  # Brasil - Petróleo y gas
    'pinfra': 'PINFRA.MX',  # México - Infraestructura y energía
    'geb': 'GEB.CL',  # Colombia - Energía y gas natural
}

# Fecha de inicio fija
start_date = '2023-01-01'

# Fecha de fin se actualiza a la fecha actual
end_date = datetime.date.today().strftime('%Y-%m-%d')

# Dataframe para almacenar todos los datos históricos
all_historical_data = pd.DataFrame()

# Ciclo para iterar sobre todas las empresas
for key, ticker in tickers_dict.items():
    output_file = f'datasets/{key}_historical_data.csv'
    try:
        download_historical_data(ticker, start_date, end_date, output_file)
        print(f'Se ha guardado el dataset de {key}')
        
        # Leer el CSV recién creado
        df = pd.read_csv(output_file)
        df['Company'] = key  # Añadir una columna con el nombre de la empresa
        all_historical_data = pd.concat([all_historical_data, df], ignore_index=True)
    except Exception as e:
        print(f'Error al descargar datos de {key}: {str(e)}')

# Guardar todos los datos históricos en un solo archivo CSV
all_historical_data.to_csv('datasets/latam_energy_stock_data.csv', index=False)

print(f'Datos actualizados hasta: {end_date}')
print(f'Se ha guardado el dataset completo en datasets/latam_energy_stock_data.csv')