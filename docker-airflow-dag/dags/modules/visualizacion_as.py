import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import warnings
import os

# Ignorar el warning 
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Ajustar las rutas de los archivos
current_dir = os.path.dirname(os.path.abspath(__file__))
base_path = os.path.abspath(os.path.join(current_dir, '..', 'datasets'))
sentiment_file = os.path.join(base_path, 'daily_sentiment_summary_latam_energy.csv')
stock_file = os.path.join(base_path, 'latam_energy_stock_data.csv')

# Cargar los datos
sentiment_data = pd.read_csv(sentiment_file)
stock_data = pd.read_csv(stock_file)

# Convertir las fechas a datetime
sentiment_data['Date'] = pd.to_datetime(sentiment_data['Date']).dt.strftime('%Y-%m-%d')
stock_data['Date'] = pd.to_datetime(stock_data['Date'], utc=True).dt.strftime('%Y-%m-%d')

# Datos ordenados por fecha
sentiment_data = sentiment_data.sort_values('Date')
stock_data = stock_data.sort_values('Date')

# Función para calcular el cambio porcentual diario
def calculate_daily_change(group):
    group['Daily_Change'] = group['Close'].pct_change() * 100
    return group

# Calcular el cambio porcentual diario para cada empresa
stock_data = stock_data.groupby('Company', group_keys=False).apply(calculate_daily_change)

# Función para graficar la comparación para una empresa
def plot_sentiment_vs_stock(company):
    company_sentiment = sentiment_data[sentiment_data['Company'] == company]
    company_stock = stock_data[stock_data['Company'] == company]
    
    # Combinar los datos de sentimiento y acciones
    merged_data = pd.merge(company_sentiment, company_stock, on=['Date', 'Company'], how='inner')
    
    if merged_data.empty:
        print(f"No hay datos coincidentes para {company}")
        return
    
    # Convertir la fecha de nuevo a datetime para la gráfica
    merged_data['Date'] = pd.to_datetime(merged_data['Date'])
    
    # Crear la gráfica
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    # Graficar el sentimiento
    ax1.plot(merged_data['Date'], merged_data['Avg_Sentiment'], color='blue', label='Sentimiento Promedio')
    ax1.set_xlabel('Fecha')
    ax1.set_ylabel('Sentimiento Promedio', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    
    # Crear un segundo eje y para el cambio porcentual de las acciones
    ax2 = ax1.twinx()
    ax2.plot(merged_data['Date'], merged_data['Daily_Change'], color='red', label='Cambio % Diario')
    ax2.set_ylabel('Cambio % Diario', color='red')
    ax2.tick_params(axis='y', labelcolor='red')
    
    # Añadir título y leyenda
    plt.title(f'Sentimiento vs Cambio % Diario de Acciones - {company}')
    fig.legend(loc="upper right", bbox_to_anchor=(1,1), bbox_transform=ax1.transAxes)
    
    # Ajustar el diseño
    plt.tight_layout()
    
    # Guardar la gráfica
    plt.savefig(os.path.join(base_path, f'{company}_sentiment_vs_stock.png'))
    
    # Mostrar la gráfica
    plt.show()

# Graficar para cada empresa
for company in sentiment_data['Company'].unique():
    plot_sentiment_vs_stock(company)

# Calcular la correlación entre sentimiento y cambio de acciones para cada empresa
correlations = []
for company in sentiment_data['Company'].unique():
    company_sentiment = sentiment_data[sentiment_data['Company'] == company]
    company_stock = stock_data[stock_data['Company'] == company]
    
    merged_data = pd.merge(company_sentiment, company_stock, on=['Date', 'Company'], how='inner')
    
    if not merged_data.empty:
        correlation = merged_data['Avg_Sentiment'].corr(merged_data['Daily_Change'])
        correlations.append({'Company': company, 'Correlation': correlation})
    else:
        print(f"No hay datos coincidentes para calcular la correlación de {company}")

correlation_df = pd.DataFrame(correlations)
correlation_df = correlation_df.sort_values('Correlation', ascending=False)

print("Correlaciones entre Sentimiento y Cambio % Diario de Acciones:")
print(correlation_df)

# Guardar las correlaciones en un archivo CSV
correlation_df.to_csv(os.path.join(base_path, 'sentiment_stock_correlations_latam_energy.csv'), index=False)
print(f"Las correlaciones se han guardado en '{os.path.join(base_path, 'sentiment_stock_correlations_latam_energy.csv')}'")

# Crear un gráfico de barras para las correlaciones
plt.figure(figsize=(12, 6))
plt.bar(correlation_df['Company'], correlation_df['Correlation'])
plt.title('Correlación entre Sentimiento y Cambio % Diario de Acciones por Empresa de Energía')
plt.xlabel('Empresa')
plt.ylabel('Correlación')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(os.path.join(base_path, 'correlations_bar_chart_latam_energy.png'))
plt.show()