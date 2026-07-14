import streamlit as st

from chatbot import (
    generate_response,
    get_action_response,
    create_conversation_state,
    update_conversation_state
)

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="MindMate AI",
    page_icon="🧠",
    layout="wide"
)

# ==========================================================
# SESSION STATE
# ==========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "analysis" not in st.session_state:
    st.session_state.analysis = None

if "actions" not in st.session_state:
    st.session_state.actions = []

if "conversation_state" not in st.session_state:
    st.session_state.conversation_state = create_conversation_state()

# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.title("🧠 MindMate AI")

    st.caption("AI Mental Wellness Companion")

    st.divider()

    if st.session_state.analysis:

        analysis = st.session_state.analysis

        st.subheader("AI Insights")

        st.metric(
            "Wellness Score",
            f"{analysis['wellness_score']}/100"
        )

        st.write(
            f"😊 Emotion: **{analysis['emotion'].title()}**"
        )

        st.write(
            f"💬 Sentiment: **{analysis['sentiment'].title()}**"
        )

    else:

        st.info("Start chatting to see AI insights.")

    st.divider()

    st.caption(
        "MindMate provides emotional support. It is not a substitute for professional mental healthcare."
    )

# ==========================================================
# MAIN PAGE
# ==========================================================

st.title("🧠 MindMate AI")

st.subheader("Your Mental Wellness Companion")

st.markdown(
"""
Hi! 👋

You can talk to me about:

- Stress
- Anxiety
- Relationships
- College
- Exams
- Coding
- Anything on your mind

I'm here to understand first before suggesting solutions.
"""
)

st.divider()

# ==========================================================
# CHAT HISTORY
# ==========================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# ==========================================================
# USER INPUT
# ==========================================================

prompt = st.chat_input("Type your message...")

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    result = generate_response(
        prompt,
        st.session_state.conversation_state
    )

    st.session_state.analysis = result["analysis"]

    st.session_state.actions = result["actions"]


    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": result["reply"]
        }
    )

    with st.chat_message("assistant"):
        st.markdown(result["reply"])

# ==========================================================
# ACTION BUTTONS
# ==========================================================

if st.session_state.actions:

    st.divider()

    st.subheader("How would you like me to help?")

    cols = st.columns(len(st.session_state.actions))

    for i, action in enumerate(st.session_state.actions):

        with cols[i]:

            if st.button(action):

                response = get_action_response(
                    action,
                    st.session_state.conversation_state["last_user_message"],
                    st.session_state.analysis
                )

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": response
                    }
                )

                st.rerun() 