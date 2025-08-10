ARG BUILD_FROM=ghcr.io/hassio-addons/base:16.3.3
FROM ${BUILD_FROM}

RUN apk add --no-cache python3 py3-pip git curl bash ca-certificates ffmpeg

RUN python3 -m pip install --no-cache-dir --upgrade pip wheel setuptools  && pip install --no-cache-dir fastapi uvicorn httpx numpy soundfile TTS

# Ollama
RUN curl -fsSL https://ollama.com/download/linux | sh || true
ENV OLLAMA_HOST=0.0.0.0:11434

WORKDIR /opt/megan
RUN echo '# Placeholder Megan server' > /opt/megan/megan_ai_single_file.py

COPY rootfs /

EXPOSE 8000 11434

CMD ["/run.sh"]
