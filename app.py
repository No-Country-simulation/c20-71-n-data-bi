import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

# Configuración de la página
st.set_page_config(page_title="Análisis de Sentimiento y Acciones de Energía en LATAM", layout="wide")

# Carga de datos
@st.cache_data
def load_data():
    correlations = pd.read_csv('analisis_sentimiento/negative_sentiment_stock_correlations_latam_energy.csv')
    daily_sentiment = pd.read_csv('analisis_sentimiento/daily_negative_sentiment_summary_latam_energy.csv')
    stock_data = pd.read_csv('datasets/latam_energy_stock_data.csv')
    return correlations, daily_sentiment, stock_data

correlations, daily_sentiment, stock_data = load_data()

# Título principal
st.title("Análisis de Sentimiento y Acciones de Empresas de Energía en Latinoamérica")

# Barra lateral para navegación
page = st.sidebar.selectbox("Seleccione una página", ["Resumen General", "Análisis por Empresa", "Correlaciones"])

if page == "Resumen General":
    st.header("Resumen General")
    
    # Mostrar gráfico de correlaciones
    st.subheader("Correlaciones entre Sentimiento Negativo y Cambio % Diario de Acciones")
    correlation_chart = Image.open('analisis_sentimiento/negative_correlations_bar_chart_latam_energy.png')
    st.image(correlation_chart, use_column_width=True)
    
    # Estadísticas globales
    st.subheader("Estadísticas Globales")
    total_companies = len(correlations)
    avg_correlation = correlations['Correlation'].mean()
    st.write(f"Número total de empresas analizadas: {total_companies}")
    st.write(f"Correlación promedio: {avg_correlation:.2f}")

elif page == "Análisis por Empresa":
    st.header("Análisis por Empresa")
    
    # Selector de empresa
    company = st.selectbox("Seleccione una empresa", correlations['Company'].unique())
    
    # Mostrar correlación para la empresa seleccionada
    company_corr = correlations[correlations['Company'] == company]['Correlation'].values[0]
    st.write(f"Correlación para {company}: {company_corr:.2f}")
    
    # Gráfico de sentimiento vs cambio de acciones
    st.subheader("Sentimiento Negativo vs Cambio % Diario de Acciones")
    company_sentiment = daily_sentiment[daily_sentiment['Company'] == company]
    company_stock = stock_data[stock_data['Company'] == company]
    
    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax1.plot(company_sentiment['Date'], company_sentiment['Avg_Sentiment'], color='blue', label='Sentimiento Negativo Promedio')
    ax1.set_xlabel('Fecha')
    ax1.set_ylabel('Sentimiento Negativo Promedio', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    
    ax2 = ax1.twinx()
    ax2.plot(company_stock['Date'], company_stock['Close'].pct_change() * 100, color='red', label='Cambio % Diario')
    ax2.set_ylabel('Cambio % Diario', color='red')
    ax2.tick_params(axis='y', labelcolor='red')
    
    plt.title(f'Sentimiento Negativo vs Cambio % Diario de Acciones - {company}')
    fig.legend(loc="upper right", bbox_to_anchor=(1,1), bbox_transform=ax1.transAxes)
    st.pyplot(fig)

elif page == "Correlaciones":
    st.header("Tabla de Correlaciones")
    
    # Mostrar tabla de correlaciones
    st.dataframe(correlations.sort_values('Correlation', ascending=False))
    
    # Permitir descarga de CSV
    st.download_button(
        label="Descargar datos de correlaciones",
        data=correlations.to_csv(index=False),
        file_name="correlaciones_sentimiento_acciones.csv",
        mime="text/csv",
    )

# Pie de página
st.sidebar.markdown("---")
st.sidebar.markdown("Desarrollado por EnergySmart Invest")