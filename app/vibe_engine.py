def analyze_review(text: str):
    # Simple mock logic for sentiment analysis
    text = text.lower()
    score = 5.0
    sentiment = "Neutral"
    keywords = ["general"]

    if any(word in text for word in ["good", "great", "amazing", "love"]):
        score = 9.0
        sentiment = "Positive"
        keywords = ["positive", "vibes"]
    elif any(word in text for word in ["bad", "terrible", "hate", "awful"]):
        score = 2.0
        sentiment = "Negative"
        keywords = ["negative", "vibes"]

    return {
        "vibe_score": score,
        "sentiment": sentiment,
        "keywords": keywords
    }