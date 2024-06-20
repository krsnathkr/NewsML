import os
from newsapi import NewsApiClient
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')

newsapi = NewsApiClient(api_key=API_KEY)

def fetch_news(query):
    data = newsapi.get_everything(qintitle=query, sort_by='relevancy', language='en')
    return data['articles']
