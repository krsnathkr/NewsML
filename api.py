import requests
import os
from pprint import pprint
from newsapi import NewsApiClient
from dotenv import load_dotenv
load_dotenv()

api = NewsApiClient(api_key = '5cecce8e503d43faaeea7e2e96710466')

data = api.get_everything(q='russia',
                            sources='bbc-news,the-verge',
                            language='en',
                            sort_by='relevancy')

pprint(data['articles'][0]['title'])
print('-------------------------------------------------------------------------------------')
pprint(data['articles'][0:5])