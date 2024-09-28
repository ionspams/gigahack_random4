import streamlit as st
from transformers import pipeline
import time

# Initialize NLP pipelines for question answering and sentiment analysis
qa_pipeline = pipeline("question-answering")
sentiment_pipeline = pipeline("sentiment-analysis")

# Simple FAQ context for quick responses
faq_context = """
Your internet plan allows speeds of up to 100Mbps.
To restart your router, unplug it, wait 10 seconds, and plug it back in.
To upgrade your plan, visit our website or contact customer service.
"""

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

if 'user_input' not in st.session_state:
    st.session_state['user_input'] = ""

# Function to process user input and append response to chat
def process_input(user_input):
    # Analyze sentiment
    sentiment_label, sentiment_score = detect_sentiment(user_input)
    
    if sentiment_label == "NEGATIVE" and sentiment_score > 0.7:
        response = "It seems you're frustrated. Escalating to a human agent..."
    else:
        response = answer_query(user_input)
    
    # Append user input and assistant response to chat history
    st.session_state['chat_history'].append(f"You: {user_input}")
    st.session_state['chat_history'].append(f"Assistant: {response}")

# Function to display chat history
def display_chat():
    for message in st.session_state['chat_history']:
        st.write(message)

# Sentiment analysis function
def detect_sentiment(user_message):
    sentiment = sentiment_pipeline(user_message)
    return sentiment[0]['label'], sentiment[0]['score']

# Query-answering function
def answer_query(user_query):
    response = qa_pipeline({
        'question': user_query,
        'context': faq_context
    })
    return response['answer']

# Chat interface with voice-to-text
def chat_based_version():
    st.title("Telecom Virtual Assistant - Chat Interface")
    st.write("Welcome to the Telecom Assistant! Ask me anything.")
    
    # Display chat history
    display_chat()

    # Add input field for chat
    user_input = st.text_input("Type your message here:", key="user_input")

    # Add a microphone button for voice input
    st.markdown("""
    <script>
    const btn = document.createElement('button');
    btn.textContent = '🎤 Speak';
    btn.onclick = () => {
        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = 'en-US';
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;
        recognition.onresult = (event) => {
            const userVoiceInput = event.results[0][0].transcript;
            document.getElementById("user_input").value = userVoiceInput;
        };
        recognition.start();
    };
    document.body.appendChild(btn);
    </script>
    """, unsafe_allow_html=True)

    # Handle "Send" button click
    if st.button("Send"):
        if user_input:
            process_input(user_input)
            # Clear input after sending
            st.session_state['user_input'] = ""

# Main function to switch between interfaces
def main():
    # Sidebar for version selection
    st.sidebar.title("Version Selector")
    version = st.sidebar.radio(
        "Select the interface version to use:",
        ('Form-Based Prototype', 'Chat Interface with Voice-to-Text')
    )

    # Switch between the versions based on sidebar selection
    if version == 'Form-Based Prototype':
        form_based_version()
    elif version == 'Chat Interface with Voice-to-Text':
        chat_based_version()

# Current form-based version
def form_based_version():
    st.title("Telecom Virtual Assistant - Form Version")
    st.write("Hello! How can I assist you today?")
    
    user_input = st.text_input("Ask me anything about your telecom service:")

    if user_input:
        sentiment_label, sentiment_score = detect_sentiment(user_input)
        if sentiment_label == "NEGATIVE" and sentiment_score > 0.7:
            st.write("It seems you're frustrated. Escalating to a human agent...")
        else:
            response = answer_query(user_input)
            st.write(f"Response: {response}")

    st.write("Having internet issues? Let's troubleshoot.")
    step = st.number_input("Choose troubleshooting step (1-3):", min_value=1, max_value=3, step=1)
    if st.button("Run Troubleshooting"):
        solution = f"Troubleshooting Step {step} in progress..."
        st.write(solution)

    if st.button("Submit Feedback"):
        st.write("Thank you for your feedback!")

if __name__ == "__main__":
    main()