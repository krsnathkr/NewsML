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

if st.button('Get News'):
    if query:
        articles, df = fetch_and_analyze_news(query)
        if articles and not df.empty:
            # Prepare the recommendation system with the sentiment-analyzed data
            get_recommendations, recommend = model.prepare_recommendation_system(df)

            # Display articles
            for i, article in enumerate(articles):
                st.header(article['title'])
                sentiment_score = df.loc[df['title'] == article['title'], 'compound'].values[0]
                st.subheader(f"Sentiment Score: {sentiment_score}")
                st.write(article['description'])
                st.write(f"[Read more]({article['url']})")

                # Add a unique key for each button
                button_key = f"recommend_btn_{i}"
                if st.button(f"Recommend based on '{article['title']}'", key=button_key):
                    recommendations = get_recommendations(article['title'])
                    st.session_state.recommendations[button_key] = recommendations
                    st.write(f"Recommendations for {article['title']} generated")
                    st.write(f"Generated Recommendations: {recommendations}")

                # Check and display recommendations if they exist
                if button_key in st.session_state.recommendations:
                    st.write("Recommended Articles:")
                    for rec in st.session_state.recommendations[button_key]:
                        st.write(rec)

st.sidebar.title('Choose News Category')
categories = ['Business', 'Entertainment', 'General', 'Health', 'Science', 'Sports', 'Technology']
selected_category = st.sidebar.radio('Categories:', categories)
if selected_category:
    if st.sidebar.button('Get Category News'):
        category_articles = api.fetch_news(selected_category)
        if category_articles:
            df = sentiment.analyze_sentiment(category_articles)
            
            if not df.empty:
                # Prepare the recommendation system with the sentiment-analyzed data
                get_recommendations, recommend = model.prepare_recommendation_system(df)

                for i, article in enumerate(category_articles):
                    st.header(article['title'])
                    sentiment_score = df.loc[df['title'] == article['title'], 'compound'].values[0]
                    st.subheader(f"Sentiment Score: {sentiment_score}")
                    st.write(article['description'])
                    st.write(f"[Read more]({article['url']})")
                    
                    button_key = f"recommend_btn_category_{i}"
                    if st.button(f"Recommend based on '{article['title']}'", key=button_key):
                        recommendations = get_recommendations(article['title'])
                        st.session_state.recommendations[button_key] = recommendations
                        st.write(f"Recommendations for {article['title']} generated")
                        st.write(f"Generated Recommendations: {recommendations}")
                    
                    if button_key in st.session_state.recommendations:
                        st.write("Recommended Articles:")
                        for rec in st.session_state.recommendations[button_key]:
                            st.write(rec)

st.sidebar.title('Choose Country')
country_name = st.sidebar.text_input('Enter Country Name')
if country_name:
    country_code = pycountry.countries.get(name=country_name).alpha_2.lower()
    if st.sidebar.button('Get Country News'):
        country_articles = api.fetch_news(country_code)
        if country_articles:
            df = sentiment.analyze_sentiment(country_articles)
            
            if not df.empty:
                # Prepare the recommendation system with the sentiment-analyzed data
                get_recommendations, recommend = model.prepare_recommendation_system(df)

                for i, article in enumerate(country_articles):
                    st.header(article['title'])
                    sentiment_score = df.loc[df['title'] == article['title'], 'compound'].values[0]
                    st.subheader(f"Sentiment Score: {sentiment_score}")
                    st.write(article['description'])
                    st.write(f"[Read more]({article['url']})")
                    
                    button_key = f"recommend_btn_country_{i}"
                    if st.button(f"Recommend based on '{article['title']}'", key=button_key):
                        recommendations = get_recommendations(article['title'])
                        st.session_state.recommendations[button_key] = recommendations
                        st.write(f"Recommendations for {article['title']} generated")
                        st.write(f"Generated Recommendations: {recommendations}")
                    
                    if button_key in st.session_state.recommendations:
                        st.write("Recommended Articles:")
                        for rec in st.session_state.recommendations[button_key]:
                            st.write(rec)
