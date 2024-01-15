from openai import OpenAI
from dotenv import load_dotenv
# import openai
# openai.api_key = "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"

load_dotenv()
client = OpenAI()

def update_chat(messages, role, content):
    messages.append({"role": role, "content": content})
    return messages


def get_chatgpt_response(messages):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message.content


messages=[
    {"role": "system", "content": "You are Assistor, an experienced mental health therapist for teenagers, skilled in providing empathetic support and personalized solutions."},
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi there!, I'm Assistor, a mental health assistant. How are you feeling today?"},
    # {"role": "user", "content": "I've been feeling really stressed lately, and I don't know how to handle it."},
    # {"role": "assistant", "content": "I'm sorry to hear that you're feeling stressed. It's completely normal to feel this way sometimes. Can you share more about what's been going on?"},
    # {"role": "user", "content": "I have a lot of schoolwork, and it feels overwhelming. I don't know where to start."},
]

conversation = ""
for message in messages:
    if message["role"] == "user":
        conversation += "User: " + message["content"] + "\n"
    elif message["role"] == "assistant":
        conversation += "AI: " + message["content"] + "\n"
        
print(conversation)

while True:
    user_input = input("User: ")
    messages = update_chat(messages, "user", user_input)
    model_response = get_chatgpt_response(messages)
    messages = update_chat(messages, "assistant", model_response)
    print("AI:", model_response, end="\n\n")
