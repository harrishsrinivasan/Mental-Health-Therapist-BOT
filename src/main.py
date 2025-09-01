import os
import socket
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Settings
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Therapist system prompt (improved)
SYSTEM_PROMPT = (
    "You are a licensed mental health therapist based in India. "
    "Your role is to provide empathetic, professional, and supportive guidance for mental health concerns. "
    "Always respond in a warm, non-judgmental, and compassionate manner. "
    "Keep responses concise — usually between 3 to 6 sentences, but adapt based on the user’s needs. "
    "You may discuss sensitive topics such as smoking, drinking, casual sex, suicidal thoughts, and other mental health struggles. "
    "When suicide or self-harm is mentioned, provide crisis guidance along with relevant Indian resources such as 112 or AASRA (+91-9820466726). "
    "Offer coping strategies, healthier alternatives, and practical tools tailored to the user’s situation. "
    "If the user asks about topics unrelated to mental health, politely decline and gently redirect the conversation back to mental health."
    "Do not provide any programming code as part of some solution to mental health concerns."
)

# Function to check internet connectivity
def is_connected(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception:
        return False

ONLINE = is_connected()

# Streamlit page config
st.set_page_config(
    page_title="Therapist Bot",
    page_icon="👨‍⚕️",
    layout="centered",
)

st.title("👨‍⚕️ Mental Health Therapist")

# Initialize unified chat history
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [{"role": "system", "content": SYSTEM_PROMPT}]

# Load correct backend
if ONLINE:
    import google.generativeai as gen_ai
    gen_ai.configure(api_key=GOOGLE_API_KEY)
    model = gen_ai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=SYSTEM_PROMPT,
    )
else:
    from ollama import Client
    ollama_base = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    client = Client(host=ollama_base)
    try:
        _ = client.list()
    except Exception as e:
        st.error(
            "Can't connect to Ollama. Make sure Ollama is running and the model is pulled.\n\n"
            f"Try in a terminal:\n  ollama pull {OLLAMA_MODEL}\n  ollama run {OLLAMA_MODEL}\n\nDetails: {e}"
        )
        st.stop()


# Display chat history (skip system prompt)
for message in st.session_state["chat_history"]:
    if message["role"] == "system":
        continue
    with st.chat_message(message["role"], avatar="👨‍⚕️" if message["role"] == "assistant" else None):
        st.markdown(message["content"])

# Input
user_prompt = st.chat_input("Ask Therapist...")

if user_prompt:
    # Save user input
    st.chat_message("user").markdown(user_prompt)
    st.session_state["chat_history"].append({"role": "user", "content": user_prompt})

    if ONLINE:
        # Build context for Gemini
        context = "\n".join(
            [f"{msg['role']}: {msg['content']}" for msg in st.session_state["chat_history"] if msg["role"] != "system"]
        )
        gemini_response = model.generate_content(context)
        therapist_response = gemini_response.text
    else:
        # Ollama uses structured messages
        try:
            res = client.chat(model=OLLAMA_MODEL, messages=st.session_state["chat_history"])
            therapist_response = res["message"]["content"]
        except Exception as e:
            st.error(f"Ollama chat failed: {e}")
            st.stop()

    # Save assistant response
    st.session_state["chat_history"].append({"role": "assistant", "content": therapist_response})

    # Display assistant response
    with st.chat_message("assistant", avatar="👨‍⚕️"):
        st.markdown(therapist_response)

