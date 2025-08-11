import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def scrape_forex_headlines():
    url = 'https://www.investing.com/news/forex-news'
    headers = {'User-Agent': 'Mozilla/5.0'}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    headlines = soup.find_all('a', class_='title')

    news_list = [h.text.strip() for h in headlines if h.text.strip()]

    # Crear carpeta si no existe
    os.makedirs('data', exist_ok=True)

    # Guardar en CSV
    df_news = pd.DataFrame({'headline': news_list})
    df_news.to_csv('data/news_headlines.csv', index=False)

    print(f"{len(news_list)} titulares guardados en: data/news_headlines.csv")

if __name__ == "__main__":
    scrape_forex_headlines()
