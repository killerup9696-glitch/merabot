import os
import streamlit as st
from huggingface_hub import InferenceClient

st.set_page_config(page_title="Mera Chatbot", page_icon="🤖")
st.title("🤖 Mera Chatbot")

MODEL_ID = "Qwen/Qwen2.5-7B-Instruct"
SYSTEM_PROMPT = "Aap ek madadgar assistant hain. Hindi ya English mein, jo user ne use kiya ho, usi mein jawab dein."

# Token: pehle environment variable, phir Streamlit secrets se lein
token = os.environ.get("HF_TOKEN")
if not token:
    try:
        token = st.secrets["HF_TOKEN"]
    except Exception:
        token = None

if not token:
    st.error("HF_TOKEN set nahi hai. App settings mein secret add karein.")
    st.stop()

client = InferenceClient(model=MODEL_ID, token=token)

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
                response = client.chat_completion(messages, max_tokens=512, temperature=0.7)
                reply = response.choices[0].message.content
            except Exception as e:
                reply = f"Error aaya: {e}"
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
