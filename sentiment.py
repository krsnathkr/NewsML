# sentiment.py

import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def analyze_sentiment(articles):
    article_keys = articles[0].keys()

    # Creating DataFrame with all keys as columns
    df = pd.DataFrame(articles, columns=article_keys)

    cols_to_remove = ['source', 'url', 'urlToImage', 'publishedAt']
    df = df.drop(cols_to_remove, axis=1)
    df = df[df['description'].notna()]

    vader = SentimentIntensityAnalyzer()

    f = lambda content: vader.polarity_scores(content)['compound']
    df['compound'] = df['content'].apply(f)

    return df
