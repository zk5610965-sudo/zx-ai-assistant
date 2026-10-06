import streamlit as st
from google import genai
import time

st.set_page_config(
    page_title="ZX Studio AI",
    page_icon="⚡",
    layout="centered"
)

st.title("⚡ ZX Professional AI Assistant")
st.write("Aapka apna smart assistant — Padhai, Business aur Coding ke liye!")

# API Key check
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = "YAHAN_APNI_API_KEY_DAAL_DENA"

client = genai.Client(api_key=api_key)

# Chat history initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Yahan apna sawal likhein..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response with retry logic for errors
    with st.chat_message("assistant"):
        with st.spinner("ZX AI soch raha hai..."):
            success = False
            attempts = 3
            for i in range(attempts):
                try:
                    response = client.models.generate_content(
                        model='gemini-3.8-flash',
                        contents=f"You are ZX AI Assistant, created for Zahed. Help him accurately and fast. User: {prompt}"
                    )
                    ai_response = response.text
                    st.markdown(ai_response)
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})
                    success = True
                    break
                except Exception as e:
                    if i < attempts - 1:
                        time.sleep(2) # 2 second wait karke dobara koshish karega
                    else:
                        st.error(f"Server busy hai, thodi der baad try karein. (Error: {e})")
