from transformers import pipeline

sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="cardiffnlp/twitter-roberta-base-sentiment-latest"
)

def detect_sentiment(text):

    result = sentiment_pipeline(text)[0]

    sentiment = result["label"]

    # Convert labels if necessary
    mapping = {
        "LABEL_0": "negative",
        "LABEL_1": "neutral",
        "LABEL_2": "positive"
    }

    sentiment = mapping.get(sentiment, sentiment.lower())

    confidence = round(result["score"] * 100, 2)

    return sentiment, confidence