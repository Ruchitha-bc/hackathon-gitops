FROM jenkins/jenkins:2.555.3-jdk21

USER root

# Install docker CLI utilities and Git
RUN apt-get update && \
    apt-get install -y docker.io git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Fix permission tracking by forcing the runtime context to root
USER root
