import requests
import os
from pprint import pprint
from newsapi import NewsApiClient
from dotenv import load_dotenv
load_dotenv()

# api = os.environ.get('api')
api = NewsApiClient(api_key = '5cecce8e503d43faaeea7e2e96710466')
# url = f"https://newsapi.org/v2/everything?q=tesla&from=2024-05-03&sortBy=publishedAt&apiKey={api}"

# response = requests.get(url)

# data = response.json()

# articles = data['articles']
# print(len(articles))
# print(articles[0])

data = api.get_everything(q='russia',
                            sources='bbc-news,the-verge',
                            language='en',
                            sort_by='relevancy')
# pprint(data)
pprint(data)
pprint(data['articles'][0]['title'])