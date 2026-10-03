from io import StringIO
import os
from pathlib import Path

import joblib
import pandas as pd
from flask import Flask, jsonify, request


app = Flask(__name__)
MODEL_PATH = Path(os.getenv("MODEL_PATH", Path(__file__).with_name("superkart_model.joblib")))
model = joblib.load(MODEL_PATH)

FEATURES = [
    "Product_Weight",
    "Product_Sugar_Content",
    "Product_Allocated_Area",
    "Product_MRP",
    "Store_Size",
    "Store_Location_City_Type",
    "Store_Type",
    "Product_Id_char",
    "Store_Age_Years",
    "Product_Type_Category",
]


def validate_columns(frame):
    missing = [column for column in FEATURES if column not in frame.columns]
    if missing:
        raise ValueError("Missing required fields: " + ", ".join(missing))
    return frame[FEATURES]


@app.get("/health")
def health():
    return jsonify({"status": "ok", "model": MODEL_PATH.name})


@app.post("/v1/predict")
def predict_one():
    try:
        payload = request.get_json(force=True)
        frame = validate_columns(pd.DataFrame([payload]))
        prediction = float(model.predict(frame)[0])
        return jsonify({"predicted_sales": round(prediction, 2)})
    except (ValueError, TypeError) as exc:
        return jsonify({"error": str(exc)}), 400


@app.post("/v1/predictbatch")
def predict_batch():
    try:
        if "file" not in request.files:
            raise ValueError("Upload a CSV file using the 'file' field.")
        text = request.files["file"].read().decode("utf-8")
        frame = validate_columns(pd.read_csv(StringIO(text)))
        predictions = model.predict(frame)
        return jsonify({"predictions": [round(float(value), 2) for value in predictions]})
    except (ValueError, UnicodeDecodeError, pd.errors.ParserError) as exc:
        return jsonify({"error": str(exc)}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
