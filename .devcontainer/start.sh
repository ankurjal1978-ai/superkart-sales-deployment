#!/usr/bin/env bash
set -euo pipefail

if ! pgrep -f "python backend/app.py" >/dev/null; then
  nohup python backend/app.py > /tmp/superkart-backend.log 2>&1 &
fi

if ! pgrep -f "streamlit run frontend/app.py" >/dev/null; then
  nohup env API_URL=http://localhost:7860 streamlit run frontend/app.py \
    --server.address 0.0.0.0 \
    --server.port 8501 \
    --server.headless true \
    > /tmp/superkart-frontend.log 2>&1 &
fi
