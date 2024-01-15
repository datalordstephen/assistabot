import streamlit as st
from openai import OpenAI
import openai

openai.api_key = st.secrets["OPENAI_API_KEY"]

client = OpenAI()

# App title
st.set_page_config(page_title="🦙💬 Llama 2 Chatbot")

with st.sidebar:
    st.title('💬 AssistaBot - The Mental Health Companion')
    st.write('This chatbot is created for the purpose of providing mental health support to users. It is not meant to replace professional medical advice. If you are in need of urgent help, please reach out to .')

personality = "You are Assistor, an experienced mental health therapist for teenagers, skilled in providing empathetic support and personalized solutions. \
    You will be speaking to teenagers and youths, so please keep your language and tone appropriate.\
    Help the user to feel comfortable and safe. You can ask questions to get more information, but do not ask too many questions at once.\
    You can share resources with the user, such as links to articles or videos.\
    Do not respond with overly long messages. Keep your responses short and concise."

default_messages = [
    {"role": "system", "content": personality},
    {"role": "assistant", "content": "Hi there!, I'm AssistaBot, a mental health assistant. How are you feeling today?"},
]

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [default_messages]

# Display or clear chat messages
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [default_messages]
    
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

def update_chat(messages, role, content):
    messages.append({"role": role, "content": content})
    return messages

def get_chatgpt_response(messages):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message.content

# User-provided prompt
if prompt := st.chat_input(disabled=False, placeholder="Talk to AssistaBot", key="prompt"):
    update_chat(st.session_state.messages, "user", prompt)
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_chatgpt_response(st.session_state.messages)
            placeholder = st.empty()
            placeholder.markdown(response)
    update_chat(st.session_state.messages, "assistant", response)