# The Echo Chamber

Welcome to **The Echo Chamber**, a platform designed to offer a multifaceted perspective on current events by diversifying your news feed and challenging your views with a spectrum of viewpoints. Here, critical thinking is ignited, and informed decisions are made. Listen, learn, and engage in dynamic conversations.

## Features

- **News Fetching**: Retrieve news articles based on search queries or categories using the NewsAPI.
- **Sentiment Analysis**: Analyze the sentiment of news articles to understand the overall tone.
- **Recommendation System**: Get recommendations for similar news articles based on content similarity.

## Installation

### Prerequisites

- Python 3.7 or higher
- Virtual Environment (optional but recommended)

### Setup

1. **Clone the repository**:
    ```bash
    git clone https://github.com/krsnathkr/NewsML.git
    cd NewsML
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:
    Create a `.env` file in the root directory and add your NewsAPI key:
    ```env
    API_KEY=your_newsapi_key_here
    ```

## Usage

### Running the Application

Start the Streamlit application by running:
```bash
streamlit run app.py
```

### Functionality

1. **Search for News**:
    - Enter a search query to fetch relevant news articles.
    - The articles will be displayed along with their sentiment analysis.
    - Select an article to get recommendations for similar articles.

2. **Category News**:
    - Select a news category from the sidebar to fetch top headlines in that category.
    - The articles will be displayed along with their sentiment analysis.
    - Select an article to get recommendations for similar articles.

## Code Overview

### `api.py`

Handles fetching news articles from the NewsAPI based on query or category.

```python
def fetch_news(query):
    # Fetches news articles based on a search query.

def fetch_news_by_category(category):
    # Fetches top headlines based on a category.
```

### `sentiment.py`

Performs sentiment analysis on the fetched news articles.

```python
def analyze_sentiment(articles):
    # Analyzes the sentiment of the provided articles.
```

### `model.py`

Prepares and operates the recommendation system for suggesting similar news articles.

```python
def prepare_recommendation_system(df):
    # Prepares the recommendation system based on article content.
```

### `app.py`

The main application script that integrates the news fetching, sentiment analysis, and recommendation features using Streamlit for the user interface.

## Contributing

We welcome contributions to enhance The Echo Chamber. Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
