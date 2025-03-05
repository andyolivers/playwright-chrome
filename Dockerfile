FROM python:3.10

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update -q && \
    apt-get install -y -qq --no-install-recommends \
        xvfb \
        libxcomposite1 \
        libxdamage1 \
        libatk1.0-0 \
        libasound2 \
        libdbus-1-3 \
        libnspr4 \
        libgbm1 \
        libatk-bridge2.0-0 \
        libcups2 \
        libxkbcommon0 \
        libatspi2.0-0 \
        libnss3 \
    	curl \
    	&& apt-get clean

# Install Rust using rustup (Rust installer)
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# Add Rust to PATH
ENV PATH="/root/.cargo/bin:${PATH}"

COPY requirements.txt .

RUN pip install -r requirements.txt
RUN playwright install chromium

COPY script.py .

ENV DISPLAY=:99

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]