import tweepy
import pandas as pd
import re
from nltk.sentiment import SentimentIntensityAnalyzer

# Replace with your Bearer Token
client = tweepy.Client(bearer_token="YOUR_TOKEN")

query = "AI OR Data Science -is:retweet lang:en"
tweets = client.search_recent_tweets(query=query, max_results=50)

data = [tweet.text for tweet in tweets.data]

def clean_text(text):
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"#", "", text)
    return text.lower()

cleaned = [clean_text(t) for t in data]

sia = SentimentIntensityAnalyzer()

def get_sentiment(text):
    score = sia.polarity_scores(text)
    if score['compound'] >= 0.05:
        return "Positive"
    elif score['compound'] <= -0.05:
        return "Negative"
    else:
        return "Neutral"

sentiments = [get_sentiment(t) for t in cleaned]

df = pd.DataFrame({"Tweet": cleaned, "Sentiment": sentiments})
print(df.head())
print(df['Sentiment'].value_counts())
