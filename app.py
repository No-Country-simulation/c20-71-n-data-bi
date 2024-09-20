import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuración de la página
st.set_page_config(page_title="Análisis de Sentimiento y Modelo Predictivo - Energía LATAM", layout="wide")

# Carga de datos
@st.cache_data
def load_data():
    correlations = pd.read_csv('analisis_sentimiento/negative_sentiment_stock_correlations_latam_energy.csv')
    daily_sentiment = pd.read_csv('analisis_sentimiento/daily_negative_sentiment_summary_latam_energy.csv')
    stock_data = pd.read_csv('datasets/latam_energy_stock_data.csv')
    predicciones = pd.read_csv('predicciones.csv')
    return correlations, daily_sentiment, stock_data, predicciones

correlations, daily_sentiment, stock_data, predicciones = load_data()

# Título principal 
st.title("Análisis de Sentimiento y Modelo Predictivo para Empresas de Energía en Latinoamérica")

# Barra lateral para navegación
page = st.sidebar.selectbox("Seleccione una página", ["Resumen Análisis de Sentimiento", "Resultados del Modelo"])

if page == "Resumen Análisis de Sentimiento":
    st.header("Resumen Análisis de Sentimiento")
    
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

elif page == "Resultados del Modelo":
    st.header("Resultados del Modelo Predictivo")

    # Crear la tabla con iconos
    fig = go.Figure(data=[go.Table(
        header=dict(values=['Empresa', 'Predicción'],
                    fill_color='darkgrey',
                    align='left'),
        cells=dict(values=[predicciones['Nombre de la empresa'], 
                           predicciones['Predicción']],
                   align='left',
                   font_size=12,
                   height=30)
    )])

    # Añadir los iconos
    for i, pred in enumerate(predicciones['Predicción']):
        if pred == 'Up':
            fig.add_annotation(
                x=1, y=i,
                xref="x", yref="y",
                text="▲",
                font=dict(size=20, color="green"),
                showarrow=False,
            )
        else:  # 'Down'
            fig.add_annotation(
                x=1, y=i,
                xref="x", yref="y",
                text="▼",
                font=dict(size=20, color="red"),
                showarrow=False,
            )

    fig.update_layout(
        title="Predicciones para las Empresas de Energía",
        height=35*len(predicciones)+50,  # Ajustar altura según número de empresas
        margin=dict(l=0, r=0, t=30, b=0),
        xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
        yaxis=dict(showticklabels=False, showgrid=False, zeroline=False)
    )

    # Mostrar la figura en Streamlit
    st.plotly_chart(fig, use_container_width=True)

    # Permitir descarga del CSV de predicciones
    st.download_button(
        label="Descargar datos de predicciones",
        data=predicciones.to_csv(index=False),
        file_name="predicciones_empresas_energia.csv",
        mime="text/csv",
    )

# Pie de página
st.sidebar.markdown("---")
st.sidebar.markdown("Desarrollado por EnergySmart Invest")