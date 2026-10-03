# SuperKart Sales Revenue Prediction

This repository contains the deployment files for the SuperKart sales-revenue project:

- a Flask prediction API with single and batch endpoints;
- a Streamlit interface for single-record and CSV predictions;
- a reproducible GitHub Codespaces setup;
- the executed Colab notebook used for EDA, model comparison, tuning and evaluation.

## Run in GitHub Codespaces

1. Select **Code**, open the **Codespaces** tab and create a codespace on `main`.
2. Wait for the Python packages to install and the deployment model to train.
3. The services start automatically. If the Codespace was paused, use `bash .devcontainer/start.sh` in its terminal.
4. In the **Ports** tab, set ports `7860` and `8501` to **Public**.
5. Open port `8501` for the Streamlit application. Port `7860` is the backend root URL used by the notebook.

## Live demonstration

- Streamlit interface: https://cuddly-succotash-5v4rpqwppw7x27qqg-8501.app.github.dev/
- API health check: https://cuddly-succotash-5v4rpqwppw7x27qqg-7860.app.github.dev/health

The free Codespace pauses after inactivity. Reopen it from this repository if the links are temporarily unavailable.

## API endpoints

- `GET /health`
- `POST /v1/predict`
- `POST /v1/predictbatch`

The deployment model is trained from `backend/SuperKart.csv` using the same ten-feature pipeline and selected Random Forest settings documented in the notebook.
