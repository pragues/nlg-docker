FROM jupyter/pyspark-notebook:spark-3.3.0

COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt
RUN python -m nltk.downloader stopwords averaged_perceptron_tagger
RUN python -m nltk.downloader averaged_perceptron_tagger
RUN python -m nltk.downloader universal_tagset

USER root

# Add to jupyter/Dockerfile
RUN apt-get update && apt-get install -y openjdk-11-jdk wget && \
    wget https://downloads.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz && \
    tar -xvzf hadoop-3.3.6.tar.gz -C /opt/ && \
    rm hadoop-3.3.6.tar.gz

ENV HADOOP_HOME=/opt/hadoop-3.3.6
ENV PATH=$PATH:$HADOOP_HOME/bin
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64