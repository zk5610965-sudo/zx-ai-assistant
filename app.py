import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="ZX AI Assistant", page_icon="🤖")

st.title("🤖 ZX AI Assistant")
st.write("Padhai, Business, ya koi bhi sawal ho—yeh sab sambhal lega!")

# API Key configuration from Streamlit secrets
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = "YAHAN_APNI_API_KEY_DAAL_DENA"

client = genai.Client(api_key=api_key)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Yahan apna sawal likhein..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Soch raha hoon..."):
            try:
                # Using gemini-3.8-flash model
                response = client.models.generate_content(
                    model='gemini-3.8-flash',
                    contents=prompt,
                )
                ai_response = response.text
                st.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
            except Exception as e:
                st.error(f"Kuch error aa gaya: {e}")
