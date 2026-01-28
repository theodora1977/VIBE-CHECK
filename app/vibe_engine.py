import re
import string
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer

sia = SentimentIntensityAnalyzer()

def preprocess_text(text):
    text = text.lower()
    text = re.sub(f"[{re.escape(string.punctuation)}]", "", text)
    stop_words = set(stopwords.words("english"))
    words = text.split()
    words = [word for word in words if word not in stop_words]
    return " ".join(words)

def analyze_sentiment(text):
    scores = sia.polarity_scores(text)
    compound = scores["compound"]

    if compound >= 0.05:
        sentiment = "positive"
    elif compound <= -0.05:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    return sentiment, compound

def calculate_vibe_score(compound):
    # Maps compound score from VADER (-1 to 1) to a vibe score (0 to 200)
    return int((compound + 1) * 100)

def extract_keywords(text, top_n=5):
    vectorizer = TfidfVectorizer(stop_words="english")
    X = vectorizer.fit_transform([text])
    feature_names = vectorizer.get_feature_names_out()
    scores = X.toarray()[0]
    sorted_indices = scores.argsort()[::-1]
    return [feature_names[i] for i in sorted_indices[:top_n]]

def analyze_review(review_text):
    cleaned = preprocess_text(review_text)
    sentiment, compound = analyze_sentiment(cleaned)
    vibe_score = calculate_vibe_score(compound)
    keywords = extract_keywords(cleaned)

    return {
        "vibe_score": vibe_score,
        "sentiment": sentiment,
        "keywords": keywords
    }
