import streamlit as st
from google import genai

# Page Configuration for Professional Look
st.set_page_config(
    page_title="ZX Studio - AI Assistant",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom Styling for Professional UI
st.markdown("""
    <style>
    .stChatInput input {
        border-radius: 20px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Design
with st.sidebar:
    st.title("⚡ ZX Studio AI")
    st.markdown("---")
    st.markdown("**App Features:**")
    st.markdown("💬 Smart Chat & Coding")
    st.markdown("🎨 AI Image Prompts & Ideas")
    st.markdown("📈 Business & Studies Help")
    st.markdown("---")
    st.success("Status: Online & Active")
    st.caption("Powered by Google Gemini")

# Main Header
st.title("⚡ ZX Professional AI Assistant")
st.write("Aapka apna smart assistant jo padhai, business aur creative ideas me madad karega!")

# API Key configuration
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = "YAHAN_APNI_API_KEY_DAAL_DENA"

client = genai.Client(api_key=api_key)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Yahan apna sawal ya image ka idea likhein..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("ZX AI soch raha hai..."):
            try:
                response = client.models.generate_content(
                    model='gemini-3.8-flash',
                    contents=f"You are ZX AI Assistant, created for Zahed. Be very helpful, professional, and smart. User input: {prompt}"
                )
                ai_response = response.text
                st.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
            except Exception as e:
                st.error(f"Kuch error aa gaya: {e}")
