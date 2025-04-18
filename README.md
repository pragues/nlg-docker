# TextRank Keyword Extractor – Cloud Computing Project

This project is a keyword extraction platform based on **PySpark + Streamlit + Docker**, implementing the unsupervised keyword extraction algorithm proposed in the classic TextRank paper. It supports user-uploaded `.pdf`, `.docx` and `.txt` files or direct text input for keyword analysis. The backend utilizes distributed PySpark processing for high performance, while the frontend is built with Streamlit.

## Features Implemented

### Tech Architecture
- **Docker Compose Multi-Container Deployment**: Unified management and deployment of multiple services.
- **Spark Master + Worker**: Distributed task scheduling for improved processing efficiency.
- **Jupyter Notebook**: Facilitates debugging of PySpark algorithms and accelerates development iterations.
- **Streamlit Web App**: Clean and intuitive user interface for easy interaction.
- **TextRank-based Keyword Extraction**: Implementation of the classic TextRank algorithm.
- **Co-occurrence Graph Construction**: Builds a word graph using a sliding window for co-occurrence.
- **Keyword Scoring via PageRank**: Ranks keywords using the PageRank algorithm.
- **Multi-word Phrase Merging**: Recognizes and merges multi-word expressions as keywords.
- **Text Preprocessing**: Ensures algorithm accuracy through preprocessing steps.
- **File Upload Support (.txt, .docx and .pdf)**: Allows users to extract keywords from local files.
- **Direct Text Input Support**: Enables quick analysis via direct text input.
- **Frontend (Streamlit)**:
  - **Real-Time Keyword Display**: Immediate feedback of keyword extraction results.
  - **Manual Review of Output Keywords**: Users can inspect and analyze keywords easily.

## Project Structure

```
nlg-docker/
├── data/                  # Sample input texts (mounted to frontend & backend)
│   └── text_corpus.txt
├── docker-compose.yml     # Orchestrates all services
├── frontend/              # Streamlit frontend service
│   ├── app.py             # Main app entry
│   ├── utils.py           # Core TextRank logic
│   ├── Dockerfile
│   └── requirements.txt
├── jupyter/               # Jupyter + Spark container config
│   ├── Dockerfile
│   └── requirements.txt
├── notebooks/             # PySpark prototype scripts
│   └── textrank_demo.py
└── README.md
```

## Startup Instructions

Run the project with:
```
./run.sh [build|start|restart|down|clean]
```

Once started, services will be available at:

| Service | URL |
| ---- | ---- |
| 📊 Streamlit | http://localhost:8501 |
| 🧪 Jupyter | http://localhost:8888 |
| 🖥 Spark UI | http://localhost:8080 |

## How to Use
1. Visit http://localhost:8501  
2. Upload a `.pdf` or `.txt` file, or paste your text directly  
3. Click “🔍 Extract Keywords”  
4. View the extracted keyword results  

## TODO / Roadmap

| Feature | Status |
| ---- | ---- |
| Basic keyword extraction via Streamlit | ✅ Completed |
| Support for PDF / TXT / DOC files | ✅ Completed |
| Local debugging with Jupyter + PySpark | ✅ Completed |
| Multi-service deployment via Docker | ✅ Completed |
| 💾 Export keywords to CSV | ✅ Completed |
| 🌈 Add keyword word cloud | ✅ Completed |
| 🔗 Connect PySpark as backend service | 🔜 In planning (REST API to Spark) |
| ☁️ Add HDFS support for large-scale texts | 🔜 Optional goal |
| 🧠 Replace with KeyBERT / YAKE or advanced models | 🧪 Future extension |

## References
- Original TextRank paper: Mihalcea & Tarau, 2004 [PDF](https://web.eecs.umich.edu/~mihalcea/papers/mihalcea.emnlp04.pdfs)  
- Streamlit Documentation: https://docs.streamlit.io  
- Spark Chinese Docs: https://spark.apachecn.org  

**Example Output from the Original Paper:**

![Keywords:](frontend/demo.png)
