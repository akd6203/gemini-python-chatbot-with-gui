import streamlit as st
import google.generativeai as genai
from mykey import API_KEY

# Configure Gemini API Key
genai.configure(api_key=API_KEY)  # Replace with your key

# Initialize Gemini model
model = genai.GenerativeModel('gemini-2.5-pro-exp-03-25')

# Streamlit App UI
st.set_page_config(page_title="Gemini AI Chatbot", layout="centered")
st.title(" Gemini AI Chatbot with Memory (Python + Streamlit)")

# Initialize session state for conversation
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# User input
user_input = st.text_input("You:", key="user_input")

# Send button logic
if st.button("Send") and user_input.strip() != "":
    st.session_state.conversation.append({"role": "user", "parts": [user_input]})

    # Limit conversation history for performance (last 6 messages)
    context = st.session_state.conversation[-6:]

    try:
        with st.spinner("Gemini is thinking..."):
            response = model.generate_content(context)
            reply = response.text
    except Exception as e:
        reply = f"⚠️ Error: {str(e)}"

    st.session_state.conversation.append({"role": "model", "parts": [reply]})

# Display chat history
st.markdown("###  Chat History")
for message in st.session_state.conversation:
    if message["role"] == "user":
        st.markdown(f"**You:** {message['parts'][0]}")
    elif message["role"] == "model":
        st.markdown(f"**Gemini:** {message['parts'][0]}")
