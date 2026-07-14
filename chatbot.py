"""
MindMate AI
Conversation Engine
"""

import random
import re

from emotion import detect_emotion
from sentiment import detect_sentiment

from prompts import (
    EMPATHY_MESSAGES,
    FOLLOW_UP_QUESTIONS
)

from resources import (
    COPING_STRATEGIES,
    LEARNING_RESOURCES,
    CRISIS_MESSAGE
)


# ==========================================================
# GREETINGS
# ==========================================================

GREETINGS = {
    "hi",
    "hello",
    "hey",
    "good morning",
    "good afternoon",
    "good evening"
}

GOODBYES = {
    "bye",
    "goodbye",
    "see you",
    "take care"
}

THANKS = {
    "thanks",
    "thank you",
    "thx"
}


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower().strip())


def is_greeting(text):
    return normalize(text) in GREETINGS


def is_goodbye(text):
    return normalize(text) in GOODBYES


def is_thanks(text):
    return normalize(text) in THANKS


# ==========================================================
# CRISIS DETECTION
# ==========================================================

CRISIS_KEYWORDS = [

    "suicide",

    "kill myself",

    "end my life",

    "self harm",

    "hurt myself",

    "don't want to live",

    "i want to die"

]


def is_crisis(text):

    text = normalize(text)

    return any(word in text for word in CRISIS_KEYWORDS)


# ==========================================================
# TOPIC DETECTION
# ==========================================================

CODING_KEYWORDS = {

    "python",
    "java",
    "javascript",
    "c++",
    "c",
    "html",
    "css",
    "react",
    "node",
    "sql",
    "mongodb",
    "bug",
    "error",
    "exception",
    "debug",
    "coding",
    "programming",
    "leetcode",
    "algorithm"
}

STUDY_KEYWORDS = {

    "exam",
    "assignment",
    "college",
    "semester",
    "study",
    "marks",
    "cgpa",
    "placement",
    "internship",
    "project",
    "deadline",
    "class"
}


def is_coding_related(text):

    words = set(normalize(text).split())

    return len(words.intersection(CODING_KEYWORDS)) > 0


def is_study_related(text):

    words = set(normalize(text).split())

    return len(words.intersection(STUDY_KEYWORDS)) > 0


# ==========================================================
# AI ANALYSIS
# ==========================================================

def analyze_message(text):

    emotion, emotion_score = detect_emotion(text)

    sentiment, sentiment_score = detect_sentiment(text)

    wellness_score = 100

    if sentiment.lower() == "negative":
        wellness_score -= 20

    if emotion == "sadness":
        wellness_score -= 15

    elif emotion == "fear":
        wellness_score -= 15

    elif emotion == "anger":
        wellness_score -= 10

    wellness_score = max(0, min(100, wellness_score))

    return {

        "emotion": emotion,

        "emotion_score": round(emotion_score, 2),

        "sentiment": sentiment,

        "sentiment_score": round(sentiment_score, 2),

        "wellness_score": wellness_score

    }


# ==========================================================
# RESPONSE HELPERS
# ==========================================================

def empathy_response(emotion):

    if emotion in EMPATHY_MESSAGES:

        return random.choice(EMPATHY_MESSAGES[emotion])

    return random.choice(EMPATHY_MESSAGES["neutral"])


def follow_up():

    return random.choice(FOLLOW_UP_QUESTIONS)


def greeting_response():

    return (
        "Hello! 😊\n\n"
        "I'm MindMate.\n\n"
        "I'm here to listen, support you, and help whenever I can.\n\n"
        "How have you been feeling today?"
    )


def goodbye_response():

    return (
        "Take care of yourself. 🌸\n\n"
        "Thank you for talking with me today.\n\n"
        "You're always welcome back."
    )


def thanks_response():

    return (
        "You're very welcome. 💙\n\n"
        "I'm glad I could be here for you."
    )

def detect_context(text):

    text = normalize(text)

    contexts = {

        "accident": [
            "accident",
            "crash",
            "bike",
            "car",
            "injured",
            "hospital",
            "hurt"
        ],

        "relationship": [
            "boyfriend",
            "girlfriend",
            "breakup",
            "partner",
            "relationship",
            "love"
        ],

        "family": [
            "mom",
            "mother",
            "dad",
            "father",
            "parents",
            "family",
            "brother",
            "sister"
        ],

        "sleep": [
            "sleep",
            "insomnia",
            "can't sleep",
            "awake"
        ],

        "anxiety": [
            "anxiety",
            "panic",
            "worried",
            "overthinking",
            "nervous"
        ],

        "exam": [
            "exam",
            "assignment",
            "Study",
            "Homework",
            "test",
            "quiz",
            "cgpa",
            "marks",
            "semester",
            "study"
        ],

        "coding": [
            "python",
            "java",
            "bug",
            "error",
            "exception",
            "debug"
        ]

    }

    for context, keywords in contexts.items():

        if any(word in text for word in keywords):

            return context

    return "general"

# ==========================================================
# CONTEXT INTRODUCTION
# ==========================================================

def context_intro(context, emotion):

    emotion = emotion.lower()

    intros = {

        "accident": {
            "sadness": "I'm really sorry that happened.",
            "fear": "I'm really sorry that happened.",
            "anger": "That sounds like a really difficult experience.",
            "default": "I'm really sorry that happened."
        },

        "relationship": {
            "sadness": "I'm really sorry you're going through this.",
            "anger": "I can understand why you're feeling upset.",
            "fear": "That sounds emotionally overwhelming.",
            "default": "Relationships can be incredibly difficult."
        },

        "family": {
            "sadness": "I'm sorry you're dealing with this.",
            "anger": "Family situations can be emotionally exhausting.",
            "fear": "That sounds really stressful.",
            "default": "I'm sorry you're experiencing this."
        },

        "sleep": {
            "sadness": "Lack of sleep can make everything feel heavier.",
            "fear": "Not being able to sleep can feel exhausting.",
            "default": "Sleep struggles can affect both your mind and body."
        },

        "anxiety": {
            "fear": "It sounds like you've been carrying a lot.",
            "sadness": "That sounds emotionally draining.",
            "default": "Anxiety can feel overwhelming sometimes."
        },

        "exam": {
            "fear": "Academic pressure can feel really overwhelming.",
            "sadness": "I'm sorry things have been so stressful.",
            "default": "It sounds like you've been under a lot of pressure."
        },

        "coding": {
            "default": "Let's figure this out together."
        },

        "general": {
            "default": "Thank you for sharing that with me."
        }

    }

    group = intros.get(context, intros["general"])

    return group.get(emotion, group["default"])

# ==========================================================
# MAIN RESPONSE BUILDER
# ==========================================================
def build_response(user_text, analysis, state):

    emotion = analysis["emotion"].lower()
    context = state["context"]
    stage = state["stage"]

    response = context_intro(context, emotion)
    response += "\n\n"

    # -------------------------------
    # ACCIDENT
    # -------------------------------

    if context == "accident":

        if stage == 1:

            response += (
                "Are you okay physically?\n\n"
                "If you're comfortable sharing, what happened?"
            )

        elif stage == 2:

            response += (
                "Thank you for telling me.\n\n"
                "Were you injured, or were you able to walk away safely?"
            )

        else:

            response += (
                "I'm glad you're still here talking with me.\n\n"
                "How are you feeling now?"
            )

    # -------------------------------
    # RELATIONSHIP
    # -------------------------------

    elif context == "relationship":

        if stage == 1:

            response += (
                "Would you like to tell me what happened?"
            )

        elif stage == 2:

            response += (
                "That sounds really painful.\n\n"
                "How have you been coping with everything?"
            )

        else:

            response += (
                "Thank you for continuing to share this with me.\n\n"
                "I'm listening."
            )

    # -------------------------------
    # FAMILY
    # -------------------------------

    elif context == "family":

        if stage == 1:

            response += (
                "How has this been affecting you?"
            )

        else:

            response += (
                "That sounds like a heavy situation to carry.\n\n"
                "I'm here to listen."
            )

    # -------------------------------
    # SLEEP
    # -------------------------------

    elif context == "sleep":

        if stage == 1:

            response += (
                "Has this been happening for a while, or is it something recent?"
            )

        else:

            response += (
                "Sleep problems can build up over time.\n\n"
                "Have you noticed anything that seems to make it worse?"
            )

    # -------------------------------
    # ANXIETY
    # -------------------------------

    elif context == "anxiety":

        if stage == 1:

            response += (
                "What's been worrying you the most lately?"
            )

        else:

            response += (
                "Thank you for explaining that.\n\n"
                "That sounds like a lot to carry."
            )

    # -------------------------------
    # EXAMS
    # -------------------------------

    elif context == "exam":

        if stage == 1:

            response += (
                "What do you think has been causing the most pressure?"
            )

        else:

            response += (
                "Thank you for explaining.\n\n"
                "Let's take it one step at a time."
            )

    # -------------------------------
    # CODING
    # -------------------------------

    elif context == "coding":

        if stage == 1:

            response += (
                "Could you share the error message or the code that's causing the issue?"
            )

        else:

            response += (
                "Great, thank you.\n\n"
                "Let's work through it together."
            )

    else:

        response += follow_up()

    return response

# ==========================================================
# ACTION BUTTONS
# ==========================================================

def available_actions(user_text):

    actions = [

        "💬 Just Listen",

        "🌿 Coping Tips"

    ]

    if is_study_related(user_text):

        actions.append("📚 Study Help")

    if is_coding_related(user_text):

        actions.append("💻 Coding Help")

    return actions


# ==========================================================
# COPING HELP
# ==========================================================

def get_coping_tips(emotion):

    emotion = emotion.lower()

    if emotion in COPING_STRATEGIES:

        return COPING_STRATEGIES[emotion]

    return COPING_STRATEGIES["general"]


# ==========================================================
# LEARNING RESOURCES
# ==========================================================

def get_learning_resources(user_text):

    text = normalize(user_text)

    if "python" in text:

        return LEARNING_RESOURCES["python"]

    if "java" in text:

        return LEARNING_RESOURCES["java"]

    if "machine learning" in text or "ai" in text:

        return LEARNING_RESOURCES["machine learning"]

    return []


# ==========================================================
# MAIN CHATBOT FUNCTION
# ==========================================================

def generate_response(user_text, state):

    if is_greeting(user_text):

        return {
            "reply": greeting_response(),
            "analysis": None,
            "actions": []
        }

    if is_goodbye(user_text):

        return {
            "reply": goodbye_response(),
            "analysis": None,
            "actions": []
        }

    if is_thanks(user_text):

        return {
            "reply": thanks_response(),
            "analysis": None,
            "actions": []
        }

    if is_crisis(user_text):

        return {

            "reply": CRISIS_MESSAGE,

            "analysis": analyze_message(user_text),

            "actions": []

        }

    analysis = analyze_message(user_text)

    update_conversation_state(state, user_text, analysis)

    reply = build_response(user_text, analysis, state)

    actions = available_actions(user_text)

    return {

        "reply": reply,

        "analysis": analysis,

        "actions": actions

    }

# ==========================================================
# OPTIONAL HELPERS (Used by app.py)
# ==========================================================

def get_action_response(action, last_message, analysis):
    """
    Returns a response when the user clicks one of the action buttons.
    """

    if action == "💬 Just Listen":

        return (
            "Of course. 💙\n\n"
            "You don't have to rush toward a solution.\n\n"
            "I'm here to listen.\n\n"
            "Tell me whatever feels comfortable to share."
        )

    elif action == "🌿 Coping Tips":

        tips = get_coping_tips(analysis["emotion"])

        response = (
            "Here are a few gentle ideas that might help:\n\n"
        )

        for tip in tips:
            response += f"• {tip}\n"

        return response

    elif action == "📚 Study Help":

        return (
            "Sure! 📚\n\n"
            "Tell me:\n"
            "• Which subject?\n"
            "• When is your exam or deadline?\n"
            "• How many hours can you study each day?\n\n"
            "I'll help you create a study plan."
        )

    elif action == "💻 Coding Help":

        resources = get_learning_resources(last_message)

        response = (
            "I'd be happy to help with your coding problem.\n\n"
        )

        if resources:

            response += "Here are some useful resources:\n\n"

            for name, link in resources:
                response += f"• {name}\n  {link}\n\n"

        response += (
            "You can also paste your code or error message here, "
            "and I'll help you debug it."
        )

        return response

    return (
        "I'm here for you. Tell me a little more about what's on your mind."
    )

# ==========================================================
# CONVERSATION MEMORY HELPERS
# ==========================================================

def create_conversation_state():
    """
    Initial session state.
    """

    return {
        "context": None,
        "emotion": None,
        "stage": 0,
        "last_user_message": "",
        "messages": []
    }


def update_conversation_state(state, user_text, analysis):

    new_context = detect_context(user_text)

    if state["context"] == new_context:
        state["stage"] += 1
    else:
        state["stage"] = 1

    state["context"] = new_context
    state["emotion"] = analysis["emotion"]
    state["last_user_message"] = user_text

    state["messages"].append(user_text)

    if len(state["messages"]) > 10:
        state["messages"] = state["messages"][-10:]


# ==========================================================
# EXPORTS
# ==========================================================

__all__ = [

    "generate_response",

    "get_action_response",

    "create_conversation_state",

    "update_conversation_state"
]

