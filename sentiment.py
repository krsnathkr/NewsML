import api
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd

article_keys = api.data['articles'][0].keys()

# Creating DataFrame with all keys as columns
df = pd.DataFrame(api.data['articles'], columns=article_keys)

cols_to_remove = ['source', 'url', 'urlToImage', 'publishedAt']
df = df.drop(cols_to_remove, axis=1)
df = df[df['description'].notna()]

vader = SentimentIntensityAnalyzer()

f= lambda content: vader.polarity_scores(content)['compound'] 
df['compound'] = df['content'].apply(f)

# print(df.columns)
# print(df.head(5))