import streamlit as st
import requests
import os
# Hugging Face API
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
headers = {
    "Authorization": f"Bearer {os.getenv('HUGGINGFACEHUB_API_TOKEN')}"
}

# Prompt Template
def build_prompt(user_text):
    return f"""Analyze the following journal entry:
{user_text}
Determine the emotional tone, identify recurring themes, and provide personalized motivational advice.
"""

# Query HF model
def query_huggingface_model(prompt):
    payload = {"inputs": prompt}
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()[0]["generated_text"]
    else:
        return f"Error: {response.status_code} - {response.text}"

# Streamlit UI
st.title("🧠 Mental Wellness Diary Analyzer")

st.markdown("Write about your day emotionally. Let the AI help you reflect.")

user_input = st.text_area("Your Journal Entry", height=200, placeholder="Type your journal entry here...")

if st.button("🧾 Analyze Entry"):
    if user_input.strip() == "":
        st.warning("Please enter something before clicking analyze.")
    else:
        with st.spinner("Analyzing your entry..."):
            prompt = build_prompt(user_input)
            result = query_huggingface_model(prompt)
        st.success("Here's what the AI found:")
        st.write(result)
