import os
from newsapi import NewsApiClient
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')

newsapi = NewsApiClient(api_key=API_KEY)

def fetch_news(query):
    # if not query:
    #     raise ValueError("Query parameter is required")
    data = newsapi.get_everything(qintitle=query, sort_by='relevancy', language='en')
    return data['articles']

def fetch_news_by_category(category):
    valid_categories = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']
    if category not in valid_categories:
        raise ValueError("Invalid category")
    data = newsapi.get_top_headlines(category=category, language='en', country='us')
    return data['articles']
