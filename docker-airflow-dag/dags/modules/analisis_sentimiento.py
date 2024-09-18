import requests
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd
from datetime import datetime, timedelta
import os

nltk.download('vader_lexicon', quiet=True)

sia = SentimentIntensityAnalyzer()

API_KEY = 'f436f3063b6a49ddb099ab1ded54b6a0'

# Diccionario actualizado con las empresas del web scraping
energy_companies_dict = {
    'ypf': 'YPF',
    'pampa_energia': 'PAM',
    'ecopetrol': 'EC',
    'petrobras': 'PBR',
    'interconexion_electrica': 'IESFY',
    'minas_buenaventura': 'BVN',
    'eletrobras': 'EBR',
    'engie_brasil_energia': 'EGIE3.SA',
    'vista_energy': 'VIST',
    'aes_andes': 'AES'
}

def get_news(company_name, days=30, max_results=100):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    query = f'"{company_name}" OR "{energy_companies_dict[company_name]}"'
    
    url = f'https://newsapi.org/v2/everything?q={query}&from={start_date.date()}&to={end_date.date()}&sortBy=publishedAt&language=en&pageSize={max_results}&apiKey={API_KEY}'
    
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error al obtener noticias para {company_name}. Código de estado: {response.status_code}")
        return []
    
    data = response.json()
    articles = data.get('articles', [])
    
    if not articles:
        print(f"No se encontraron noticias para {company_name}")
    else:
        print(f"Se encontraron {len(articles)} noticias para {company_name}")
    
    return articles

def analyze_sentiment(text):
    return sia.polarity_scores(text)['compound']

def analyze_company_sentiment(company_name, ticker):
    news = get_news(company_name)
    sentiment_data = []
    
    for article in news:
        title = article.get('title', '')
        description = article.get('description', '')
        content = article.get('content', '')
        date = article.get('publishedAt', '')[:10]
        
        full_text = f"{title} {description} {content}"
        sentiment = analyze_sentiment(full_text)
        
        sentiment_data.append({
            'Date': date,
            'Company': company_name,
            'Ticker': ticker,
            'Sentiment': sentiment,
            'Title': title
        })
    
    return pd.DataFrame(sentiment_data)

def main():
    all_sentiment_data = pd.DataFrame()

    for company_name, ticker in energy_companies_dict.items():
        company_sentiment = analyze_company_sentiment(company_name, ticker)
        if not company_sentiment.empty:
            all_sentiment_data = pd.concat([all_sentiment_data, company_sentiment], ignore_index=True)
            print(f"Análisis completado para {company_name}. Noticias encontradas: {len(company_sentiment)}")
        else:
            print(f"No se encontraron noticias para {company_name}")

    if all_sentiment_data.empty:
        print("No se encontraron noticias para ninguna empresa.")
    else:
        all_sentiment_data['Date'] = pd.to_datetime(all_sentiment_data['Date'])
        all_sentiment_data = all_sentiment_data.sort_values('Date')

        daily_sentiment = all_sentiment_data.groupby(['Date', 'Company', 'Ticker']).agg({
            'Sentiment': ['mean', 'min', 'max', 'count'],
            'Title': lambda x: x.iloc[0]
        }).reset_index()

        daily_sentiment.columns = ['Date', 'Company', 'Ticker', 'Avg_Sentiment', 'Min_Sentiment', 'Max_Sentiment', 'News_Count', 'Sample_Title']

        # Guardando en la carpeta datasets
        current_dir = os.path.dirname(os.path.abspath(__file__))
        datasets_path = os.path.abspath(os.path.join(current_dir, '..', 'datasets'))
        if not os.path.exists(datasets_path):
            os.makedirs(datasets_path)

        all_sentiment_data.to_csv(os.path.join(datasets_path, 'all_news_sentiment_latam_energy.csv'), index=False)
        daily_sentiment.to_csv(os.path.join(datasets_path, 'daily_sentiment_summary_latam_energy.csv'), index=False)

        print(f"Análisis de sentimiento completado. Los resultados se han guardado en '{datasets_path}'")
        print(f"Total de noticias analizadas: {len(all_sentiment_data)}")

if __name__ == "__main__":
    main()