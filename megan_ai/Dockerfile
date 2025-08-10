# Create and use a venv for Python packages
RUN python3 -m venv /venv \
 && . /venv/bin/activate \
 && pip install --no-cache-dir --upgrade pip wheel setuptools \
 && pip install --no-cache-dir fastapi uvicorn httpx numpy soundfile TTS

ENV PATH="/venv/bin:$PATH"
