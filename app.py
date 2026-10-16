import os
import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Mera Chatbot", page_icon="🤖")
st.title("🤖 Mera Chatbot")

# OpenRouter model. Dusra model chahiye to yahan badal sakte hain.
MODEL_ID = "meta-llama/llama-3.3-70b-instruct:free"
SYSTEM_PROMPT = "Aap ek madadgar assistant hain. Hindi ya English mein, jo user ne use kiya ho, usi mein jawab dein."

# Key: pehle environment variable, phir Streamlit secrets se lein
api_key = os.environ.get("OPENROUTER_API_KEY")
if not api_key:
    try:
        api_key = st.secrets["OPENROUTER_API_KEY"]
    except Exception:
        api_key = None

if not api_key:
    st.error("OPENROUTER_API_KEY set nahi hai. App settings mein secret add karein.")
    st.stop()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

# Chat history session mein save karein
if "messages" not in st.session_state:
    st.session_state.messages = []

# Purane messages dikhayein
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Naya message lein
if prompt := st.chat_input("Apna sawal likhein..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages

    with st.chat_message("assistant"):
        with st.spinner("Soch raha hoon..."):
            try:
                response = client.chat.completions.create(
                    model=MODEL_ID,
                    messages=messages,
                    max_tokens=512,
                    temperature=0.7,
                )
                reply = response.choices[0].message.content
            except Exception as e:
                reply = f"Error aaya: {e}"
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
