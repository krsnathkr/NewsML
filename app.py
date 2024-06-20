import os
import api
import model
import sentiment
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from newsapi import NewsApiClient

load_dotenv()
newsapi = NewsApiClient(api_key=os.getenv('API_KEY'))

st.title('The Echo Chamber :newspaper:')
st.write('*Dive deeper into the world of news with The Echo Chamber, a platform where diverse voices collide.  Here, you won\'t find information simply echoing back what you already believe.*')
st.write('The Echo Chamber amplifies a spectrum of viewpoints, challenging your news feed and offering a multifaceted perspective on current events. This is where critical thinking is ignited and informed decisions are made. So, listen, learn, and engage in the dynamic conversations happening within **The Echo Chamber** :rolled_up_newspaper:.')

query = st.text_input('Enter search query')

# Initialize session state variables if they don't exist
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = {}

if 'titles' not in st.session_state:
    st.session_state.titles = []

if 'articles_df' not in st.session_state:
    st.session_state.articles_df = pd.DataFrame()

def fetch_and_analyze_news(query):
    if not query:
        st.error("Query parameter is required")
        return None, None
    articles = api.fetch_news(query)
    if not articles:
        st.error("No articles found for the query.")
        return None, None

    df = pd.DataFrame(articles)
    df['content'] = df['content'].fillna('')
    try:
        df = sentiment.analyze_sentiment(articles)
    except ValueError as e:
        st.error(f"Error in sentiment analysis: {e}")
        return articles, None
    return articles, df

def fetch_and_analyze_news_by_category(category):
    if not category:
        st.sidebar.error("Category parameter is required")
        return None, None
    articles = api.fetch_news_by_category(category)
    if not articles:
        st.sidebar.error("No articles found for the category.")
        return None, None

    df = pd.DataFrame(articles)
    df['content'] = df['content'].fillna('')
    try:
        df = sentiment.analyze_sentiment(articles)
    except ValueError as e:
        st.sidebar.error(f"Error in sentiment analysis: {e}")
        return articles, None
    return articles, df

def display_articles(articles, df):
    titles = []
    for i, article in enumerate(articles):
        st.subheader(article['title'])
        titles.append(article['title'])
        st.write(article['description'])
        st.write(f"[Read more]({article['url']})")
        st.write("---")
    # st.write("Debug - Titles:", titles)
    return titles

def show_recommendations(df, selected_article):
    # Debugging print statements
    # st.write("DataFrame used for recommendations:")
    # st.write(df.head())
    # st.write("Selected article:", selected_article)

    get_recommendations, _ = model.prepare_recommendation_system(df)
    recommendations = get_recommendations(selected_article)
    # st.write("Recommended Articles:")
    for rec in recommendations:
        st.subheader(f"{rec['title']}")
        st.write(f"{rec['content']}")
        st.write(f"[Read more]({rec['url']})")
        st.write("---")

selected_article = st.selectbox("Select an article for recommendations", st.session_state.titles)

if st.button('Get News'):
    if query:
        articles, df = fetch_and_analyze_news(query)
        if articles and df is not None and not df.empty:
            titles = display_articles(articles, df)
            st.session_state.titles = titles
            st.session_state.articles_df = df  # Save the DataFrame to session state
            st.rerun()

st.sidebar.title('Choose News Category')
categories = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']
selected_category = st.sidebar.radio('Categories:', categories)

if st.sidebar.button('Get Category News'):
    if selected_category:
        articles, df = fetch_and_analyze_news_by_category(selected_category)
        if articles and df is not None and not df.empty:
            titles = display_articles(articles, df)
            st.session_state.titles = titles
            st.session_state.articles_df = df  # Save the DataFrame to session state
            st.rerun()

if selected_article:
    if 'titles' in st.session_state and selected_article in st.session_state.titles:
        if 'articles_df' in st.session_state:
            df = st.session_state.articles_df  # Use the saved DataFrame
            if df is not None and not df.empty:
                show_recommendations(df, selected_article)
        else:
            st.error("Articles DataFrame not found in session state.")
