#!/usr/bin/env bash
set -euo pipefail

MODEL_ID="${MODEL_ID:-llama3.2:3b}"

if ! pgrep -x "ollama" >/dev/null; then
  echo "[Megan] Starting Ollama..."
  /usr/local/bin/ollama serve &
  sleep 3
fi

if [ "${PRELOAD_MODEL:-true}" = "true" ]; then
  echo "[Megan] Pulling model ${MODEL_ID}..."
  /usr/local/bin/ollama pull "${MODEL_ID}" || true
fi

APP="/config/megan_ai_single_file.py"
if [ ! -f "$APP" ]; then
  APP="/opt/megan/megan_ai_single_file.py"
fi

export PROVIDER=ollama
export MODEL_ID="${MODEL_ID}"
export OLLAMA_HOST="http://localhost:11434"

echo "[Megan] Launching server on 0.0.0.0:8000 using ${MODEL_ID}"
exec uvicorn megan_ai_single_file:app --host 0.0.0.0 --port 8000 --app-dir "$(dirname "$APP")"
