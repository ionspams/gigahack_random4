import streamlit as st
from transformers import pipeline
import time

# Initialize NLP pipeline for question answering and sentiment analysis
qa_pipeline = pipeline("question-answering")
sentiment_pipeline = pipeline("sentiment-analysis")

# Simple FAQ context for quick responses
faq_context = """
Your internet plan allows speeds of up to 100Mbps.
To restart your router, unplug it, wait 10 seconds, and plug it back in.
To upgrade your plan, visit our website or contact customer service.
"""

def answer_query(user_query):
    response = qa_pipeline({
        'question': user_query,
        'context': faq_context
    })
    return response['answer']

def detect_sentiment(user_message):
    sentiment = sentiment_pipeline(user_message)
    return sentiment[0]['label'], sentiment[0]['score']

def troubleshooting_step(step):
    steps = {
        1: "Step 1: Please restart your router by unplugging it for 10 seconds.",
        2: "Step 2: Check if the internet light on the router is on.",
        3: "Step 3: If the issue persists, contact customer support."
    }
    return steps.get(step, "No more troubleshooting steps available.")

def main():
    st.title("Telecom Virtual Assistant")

    st.write("Hello! How can I assist you today?")
    
    # Query section
    user_query = st.text_input("Ask me anything about your telecom service:")

    if user_query:
        with st.spinner('Processing...'):
            sentiment_label, sentiment_score = detect_sentiment(user_query)
            if sentiment_label == "NEGATIVE" and sentiment_score > 0.7:
                st.write("It seems you're frustrated. Escalating to a human agent...")
            else:
                response = answer_query(user_query)
                time.sleep(2)
                st.write(f"Response: {response}")

    # Troubleshooting module
    st.write("Having internet issues? Let's troubleshoot.")
    step = st.number_input("Choose troubleshooting step (1-3):", min_value=1, max_value=3, step=1)
    if st.button("Run Troubleshooting"):
        solution = troubleshooting_step(step)
        st.write(solution)

    # Feedback form
    if st.button("Submit Feedback"):
        st.write("Thank you for your feedback!")

if __name__ == "__main__":
    main()
