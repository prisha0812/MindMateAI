from transformers import pipeline

# Load the emotion detection model once
emotion_pipeline = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    top_k=None
)

def detect_emotion(text):
    """
    Detect the dominant emotion in the input text.
    Returns:
        emotion (str)
        confidence (float)
    """

    results = emotion_pipeline(text)[0]

    results = sorted(results, key=lambda x: x["score"], reverse=True)

    emotion = results[0]["label"]
    confidence = round(results[0]["score"] * 100, 2)

    return emotion, confidence