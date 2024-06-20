import pandas as pd
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

def prepare_recommendation_system(df):
    tfidf = TfidfVectorizer(stop_words='english')
    df['content'] = df['content'].fillna('')
    tfidf_matrix = tfidf.fit_transform(df['content'])

    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    indices = pd.Series(df.index, index=df['title']).drop_duplicates()

    def get_recommendations(title):
        if title not in indices:
            return ["Title not found"]
        
        idx = indices[title]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:11]
        news_indices = [i[0] for i in sim_scores]
        recommended_titles = df['title'].iloc[news_indices].tolist()
        return recommended_titles

    df['tags'] = df['content'].copy()
    ps = PorterStemmer()

    def stems(text):
        return ' '.join(ps.stem(word) for word in text.split())

    df['tags'] = df['tags'].apply(stems)

    cv = CountVectorizer(max_features=5000, stop_words='english')
    vector = cv.fit_transform(df['tags']).toarray()
    similarity = cosine_similarity(vector)

    def recommend(news):
        if news not in df['title'].values:
            return ["Title not found"]
        
        index = df[df['title'] == news].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_titles = [df.iloc[i[0]].title for i in distances[1:6]]
        return recommended_titles

    return get_recommendations, recommend
