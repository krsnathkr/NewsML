import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def analyze_sentiment(articles):
    if not articles:
        raise ValueError("No articles provided")

    try:
        article_keys = articles[0].keys()
    except IndexError:
        raise ValueError("Articles list is empty")
    except AttributeError:
        raise ValueError("Invalid article structure")

    # Creating DataFrame with all keys as columns
    df = pd.DataFrame(articles, columns=article_keys)

    cols_to_remove = ['source', 'url', 'urlToImage', 'publishedAt']
    df = df.drop(cols_to_remove, axis=1, errors='ignore')
    df = df[df['description'].notna()]

    # Fill None or NaN values in 'content' with an empty string
    df['content'] = df['content'].fillna('')

    vader = SentimentIntensityAnalyzer()

    f = lambda content: vader.polarity_scores(content)['compound']
    df['compound'] = df['content'].apply(f)

    return df
