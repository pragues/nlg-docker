FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# NLTK data
RUN python -m nltk.downloader stopwords averaged_perceptron_tagger