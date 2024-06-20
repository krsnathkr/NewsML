import os
import streamlit as st
from dotenv import load_dotenv
import api
import sentiment
import model
import pycountry
from newsapi import NewsApiClient

load_dotenv()

# Initialize NewsAPI
newsapi = NewsApiClient(api_key=os.getenv('API_KEY'))

# Streamlit interface
st.title('News App')
st.write('This is a simple news app that displays the latest news from around the world.')

query = st.text_input('Enter search query')

def fetch_and_analyze_news(query):
    articles = api.fetch_news(query)
    if not articles:
        st.error("No articles found for the query.")
        return None, None
    df = sentiment.analyze_sentiment(articles)
    return articles, df

if 'recommendations' not in st.session_state:
    st.session_state.recommendations = {}

def display_articles(articles, df):
    titles = []
    for i, article in enumerate(articles):
        st.header(article['title'])
        titles.append(article['title'])

        # Check if the title exists in the DataFrame
        if df[df['title'] == article['title']].empty:
            st.subheader("Sentiment Score: Not Available")
        else:
            sentiment_score = df.loc[df['title'] == article['title'], 'compound'].values[0]
            st.subheader(f"Sentiment Score: {sentiment_score}")

        st.write(article['description'])
        st.write(f"[Read more]({article['url']})")
    
    return titles

# Get and display recommendations based on selected article
def show_recommendations(df, selected_article):
    get_recommendations, _ = model.prepare_recommendation_system(df)
    recommendations = get_recommendations(selected_article)
    st.write("Recommended Articles:")
    for rec in recommendations:
        st.write(rec)

if st.button('Get News'):
    if query:
        articles, df = fetch_and_analyze_news(query)
        if articles and df is not None and not df.empty:
            titles = display_articles(articles, df)
            
            # Add dropdown to select article for recommendations
            selected_article = st.selectbox("Select an article for recommendations", titles)
            if selected_article:
                show_recommendations(df, selected_article)

st.sidebar.title('Choose News Category')
categories = ['Business', 'Entertainment', 'General', 'Health', 'Science', 'Sports', 'Technology']
selected_category = st.sidebar.radio('Categories:', categories)
if selected_category:
    if st.sidebar.button('Get Category News'):
        category_articles = api.fetch_news(selected_category)
        if category_articles:
            df = sentiment.analyze_sentiment(category_articles)
            if not df.empty:
                titles = display_articles(category_articles, df)
                
                # Add dropdown to select article for recommendations
                selected_article = st.selectbox("Select an article for recommendations", titles, key='category_select')
                if selected_article:
                    show_recommendations(df, selected_article)

st.sidebar.title('Choose Country')
country_name = st.sidebar.text_input('Enter Country Name')
if country_name:
    country_code = pycountry.countries.get(name=country_name).alpha_2.lower()
    if st.sidebar.button('Get Country News'):
        country_articles = api.fetch_news(country_code)
        if country_articles:
            df = sentiment.analyze_sentiment(country_articles)
            if not df.empty:
                titles = display_articles(country_articles, df)
                
                # Add dropdown to select article for recommendations
                selected_article = st.selectbox("Select an article for recommendations", titles, key='country_select')
                if selected_article:
                    show_recommendations(df, selected_article)
