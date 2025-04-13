FROM jupyter/pyspark-notebook:spark-3.3.0

COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt
RUN python -m nltk.downloader stopwords averaged_perceptron_tagger
RUN python -m nltk.downloader averaged_perceptron_tagger
RUN python -m nltk.downloader universal_tagset