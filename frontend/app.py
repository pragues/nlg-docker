import streamlit as st
from utils import extract_keywords_from_text, extract_text_from_pdf

st.set_page_config(page_title="TextRank Keyword Extractor", layout="wide")
st.title("🧠 TextRank Keyword Extractor")

st.markdown("Upload a `.pdf` / `.txt` file or paste text below.")

uploaded_file = st.file_uploader("Upload File", type=["txt", "pdf"])
input_text = ""

if uploaded_file:
    if uploaded_file.name.endswith(".pdf"):
        input_text = extract_text_from_pdf(uploaded_file)
    elif uploaded_file.name.endswith(".txt"):
        input_text = uploaded_file.read().decode("utf-8")

text_input = st.text_area("Or paste text here", value=input_text, height=300)

if st.button("🔍 Extract Keywords"):
    if not text_input.strip():
        st.warning("Please input some text or upload a file.")
    else:
        keywords = extract_keywords_from_text(text_input)
        st.subheader("Top Keywords")
        for kw in keywords:
            st.markdown(f"- {kw}")