
# Use Ubuntu 22.04 as base image
FROM ubuntu:22.04

# Set noninteractive installation mode
ENV DEBIAN_FRONTEND=noninteractive

# Update and install basic tools
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    gnupg \
    python3-pip \
    python3-dev \
    default-jdk \
    openjdk-17-jdk \
    openjdk-17-jre \
    git \
    unzip && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY ./requirements.txt /tmp/

# upgrade pip
RUN pip install --upgrade pip

# Install Python dependencies
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# install chinese support.
RUN apt-get update && apt-get install -y \
    fonts-noto-cjk \
    locales \
    && locale-gen en_US.UTF-8

# Set environment variables
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# After installing Python, verify the version
RUN python3 --version

RUN groupadd -r courses && useradd --create-home --no-log-init -r -g courses courses


# Set work directory
WORKDIR /app

# Copy your application code
COPY . /app


# Make scripts executable
RUN chmod +x /app/build-neo4j-instances.sh /app/neo4j-instance.sh /app/run_llama_cpp.sh

# Expose port for FastAPI
EXPOSE 8000

RUN chmod +x /app/entrypoint.sh

USER courses

RUN ["/bin/bash", "./build-neo4j-instances.sh", "./neo4j_prompts"]

# CMD ["/bin/bash", "./entrypoint.sh", "&&" , "tail", "-f", "/dev/null"]
CMD ["/bin/bash", "./entrypoint.sh"]
