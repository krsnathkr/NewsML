import os
import streamlit as st
import requests
import pycountry
from streamlit_navigation_bar import st_navbar
from dotenv import load_dotenv

load_dotenv()
# API_KEY = os.getenv(f'{env.API_KEY}')

st.title('News App')
st.write('This is a simple news app that displays the latest news from around the world.')
q = st.text_input('Enter search query')
st.write(q)

st.sidebar.title('Choose News Category')
st.sidebar.radio('Categories:', ['Business', 'Entertainment', 'General', 'Health', 'Science', 'Sports', 'Technology'])
btn = st.sidebar.button('Get News')
if btn:
    url = f'https://newsapi.org/v2/top-headlines?country=de&category=business&apiKey={API_KEY}'


st.sidebar.title('Choose Country')
st.sidebar.text_input('Enter Country Name')
