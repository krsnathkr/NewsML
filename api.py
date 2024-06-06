import requests
import os
from pprint import pprint
from newsapi import NewsApiClient
from dotenv import load_dotenv
import app

load_dotenv()
API_KEY = os.getenv('API_KEY')

API_KEY = NewsApiClient(api_key = f'{API_KEY}')

q = app.q

data = API_KEY.get_everything(qintitle = 'adani',
                            sort_by='relevancy',
                            language='en')

# pprint(data['articles'][0]['content'])
# print('-------------------------------------------------------------------------------------')
# pprint(data['articles'][0:5])