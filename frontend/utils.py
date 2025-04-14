import re
from nltk import pos_tag
from nltk.corpus import stopwords
from itertools import combinations
import networkx as nx
from PyPDF2 import PdfReader
import nltk
from docx import Document


# 初次运行时需要下载 NLTK 数据
nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")
nltk.download("averaged_perceptron_tagger_eng")
nltk.download("stopwords")

STOP = set(stopwords.words("english"))
TOKEN_RE = re.compile(r"[A-Za-z]{2,}")

def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])

def extract_keywords_from_text(text, top_n=10, window=2):
    tokens = TOKEN_RE.findall(text.lower())
    tagged = pos_tag(tokens, lang='eng')
    words = [w for w, t in tagged if t.startswith("NN") or t.startswith("JJ")]
    words = [w for w in words if w not in STOP]

    edges = []
    for i in range(len(words) - window):
        window_words = words[i:i+window]
        for a, b in combinations(window_words, 2):
            edges.append((a, b))
            edges.append((b, a))

    graph = nx.DiGraph()
    graph.add_edges_from(edges)
    ranks = nx.pagerank(graph)

    top_keywords = sorted(ranks.items(), key=lambda x: -x[1])[:top_n]
    return [kw for kw, _ in top_keywords]

def extract_text_from_docx(uploaded_file):
    doc = Document(uploaded_file)
    return "\n".join([para.text for para in doc.paragraphs])