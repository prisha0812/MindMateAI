"""
Study Planner
MindMate AI
"""

def study_plan(subject):

    plans = {

        "java":[

            "Day 1 - OOP",

            "Day 2 - Collections",

            "Day 3 - Exception Handling",

            "Day 4 - Multithreading",

            "Day 5 - Practice Questions"

        ],

        "python":[

            "Day 1 - Basics",

            "Day 2 - Functions",

            "Day 3 - OOP",

            "Day 4 - NumPy",

            "Day 5 - Machine Learning"

        ],

        "aiml":[

            "Day 1 - ML Basics",

            "Day 2 - Classification",

            "Day 3 - NLP",

            "Day 4 - CNN",

            "Day 5 - Transformers"

        ]

    }

    return plans.get(subject.lower(),["Create your own study schedule."])