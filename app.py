import streamlit as st
from google import genai
from google.genai import types

# Page Config
st.set_page_config(page_title="Zahed All-in-One AI", page_icon="🤖", layout="centered")

st.title("🤖 Zahed's Personal AI Assistant")
st.write("Padhai, Recipe, Business ya kuch bhi puchiye — Yeh sab sambhal lega!")

# API Key configuration
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = "YAHAN_APNI_API_KEY_DAAL_DENA"

if not api_key or api_key == "YAHAN_APNI_API_KEY_DAAL_DENA":
    st.warning("⚠️ Kripya apni Gemini API key set karein code me ya Streamlit Secrets me.")
else:
    # Client initialize karna
    client = genai.Client(api_key=api_key)

    # Chat history maintain karne ke liye session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Chat session create karna Google Gemini ke sath with Google Search Tool
    system_instruction = (
        "Tum ek All-in-One Smart Personal Assistant ho. "
        "Tum user ki padhai (studies, commerce, 11th grade concepts), "
        "cooking recipes, aur business ya online work me poori tarah madad karte ho. "
        "Hamesha madadgar, friendly, aur aasan bhasha me jawab dena."
    )

    # Purani chat messages ko screen par dikhana
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User ka input lena
    if prompt := st.chat_input("Yahan apna sawal likhein..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # AI ka response generate karna
        with st.chat_message("assistant"):
            with st.spinner("Soch raha hoon..."):
                try:
                    chat = client.chats.create(
                        model="gemini-2.5-flash",
                        config=types.GenerateContentConfig(
                            system_instruction=system_instruction,
                            temperature=0.7,
                            tools=[{"google_search": {}}]
                        )
                    )
                    
                    response = chat.send_message(prompt)
                    ai_response = response.text
                    
                    st.markdown(ai_response)
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})
                except Exception as e:
                    error_msg = f"Kuch error aa gaya: {e}"
                    st.error(error_msg)
