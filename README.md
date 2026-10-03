# SuperKart Sales Revenue Prediction

This repository contains the deployment files for the SuperKart sales-revenue project:

- a Flask prediction API with single and batch endpoints;
- a Streamlit interface for single-record and CSV predictions;
- a Docker Compose configuration for GitHub Codespaces;
- the executed Colab notebook used for EDA, model comparison, tuning and evaluation.

## Run in GitHub Codespaces

1. Select **Code**, open the **Codespaces** tab and create a codespace on `main`.
2. Wait for the container setup and Docker image build to finish.
3. If the services are not already running, use `docker compose up -d` in the Codespace terminal.
4. In the **Ports** tab, set ports `7860` and `8501` to **Public**.
5. Open port `8501` for the Streamlit application. Port `7860` is the backend root URL used by the notebook.

## API endpoints

- `GET /health`
- `POST /v1/predict`
- `POST /v1/predictbatch`

The deployment model is trained during the backend Docker build using the same ten-feature pipeline and selected Random Forest settings documented in the notebook.
