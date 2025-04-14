import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from io import BytesIO
from utils import extract_keywords_from_text, extract_text_from_pdf

st.set_page_config(page_title="TextRank Keyword Extractor", layout="wide")
st.title("🧠 TextRank Keyword Extractor")

st.markdown("Upload a `.pdf`, `.txt`, or `.docx` file, or paste text below.")

uploaded_file = st.file_uploader("Upload File", type=["txt", "pdf", "docx"])
input_text = ""

if uploaded_file:
    if uploaded_file.name.endswith(".pdf"):
        input_text = extract_text_from_pdf(uploaded_file)
    elif uploaded_file.name.endswith(".txt"):
        input_text = uploaded_file.read().decode("utf-8")
    elif uploaded_file.name.endswith(".docx"):
        input_text = extract_text_from_docx(uploaded_file)

text_input = st.text_area("Or paste text here", value=input_text, height=300)



if st.button("🔍 Extract Keywords"):
    if not text_input.strip():
        st.warning("Please input some text or upload a file.")
    else:
        keywords = extract_keywords_from_text(text_input)
        
        st.subheader("🔑 Top Keywords")
        for kw in keywords:
            st.markdown(f"- {kw}")

        # 显示词云
        st.subheader("☁️ Keyword Word Cloud")
        word_freq = {k: (len(keywords) - i) for i, k in enumerate(keywords)}  # 简单模拟词频
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(word_freq)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)

        # 导出 CSV
        st.subheader("📥 Export as CSV")
        df = pd.DataFrame(keywords, columns=["Keyword"])
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download Keyword CSV",
            data=csv,
            file_name="keywords.csv",
            mime="text/csv"
        )