import streamlit as st
from Llm import ask_ai

st.title("AI-Powered Text Summarizer")

text = st.text_area("Enter text to summarize", height=250)

if st.button("Summarize"):
    if not text.strip():
        st.warning("Please enter some text before summarizing.")
    else:
        prompt = f"""
        You are an expert text summarizer. Summarize the following text in 2-3 sentences:
        {text}
        """
        summary = ask_ai(prompt)
        st.subheader("Summary")
        st.write(summary)