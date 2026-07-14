"""
MindMate AI
Intent Detection Module
Version 2
"""

def detect_intent(text):

    text = text.lower()

    # Highest Priority
    emotional_support = [
        "lonely", "alone", "worthless", "hopeless",
        "sad", "cry", "depressed", "empty",
        "heartbroken", "rejected"
    ]

    wellness = [
        "stress", "stressed", "pressure",
        "burnout", "overwhelmed",
        "sleep", "can't sleep", "insomnia",
        "anxiety", "panic", "nervous",
        "worried", "tired"
    ]

    coding = [
        "python", "java", "c++", "bug",
        "error", "coding", "programming",
        "debug", "leetcode", "algorithm"
    ]

    academics = [
        "exam", "assignment", "cgpa",
        "grades", "semester", "study",
        "homework", "test"
    ]

    career = [
        "placement", "internship",
        "resume", "interview",
        "job"
    ]

    if any(word in text for word in emotional_support):
        return "emotional_support"

    if any(word in text for word in wellness):
        return "wellness"

    if any(word in text for word in coding):
        return "coding"

    if any(word in text for word in academics):
        return "academics"

    if any(word in text for word in career):
        return "career"

    return "general"