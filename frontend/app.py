import os

import pandas as pd
import requests
import streamlit as st


st.set_page_config(page_title="SuperKart Sales Predictor", page_icon="🛒", layout="centered")
API_URL = os.getenv("API_URL", "http://backend:7860").rstrip("/")

st.title("SuperKart Sales Revenue Predictor")
st.caption("Estimate revenue for one product-store record or upload a batch CSV.")

tab_single, tab_batch = st.tabs(["Single prediction", "Batch prediction"])

with tab_single:
    with st.form("single_prediction"):
        product_weight = st.number_input("Product weight", min_value=0.0, value=12.66)
        sugar = st.selectbox("Sugar content", ["Low Sugar", "Regular", "No Sugar"])
        area = st.number_input(
            "Allocated area ratio", min_value=0.0, max_value=1.0, value=0.027, format="%.3f"
        )
        mrp = st.number_input("Product MRP", min_value=0.0, value=117.08)
        size = st.selectbox("Store size", ["Small", "Medium", "High"])
        city = st.selectbox("City tier", ["Tier 1", "Tier 2", "Tier 3"])
        store_type = st.selectbox(
            "Store type",
            [
                "Supermarket Type1",
                "Supermarket Type2",
                "Supermarket Type3",
                "Departmental Store",
                "Food Mart",
            ],
        )
        prefix = st.selectbox("Product family", ["FD", "DR", "NC"])
        age = st.number_input("Store age in years", min_value=0, value=16)
        category = st.selectbox("Product type category", ["Perishables", "Non Perishables"])
        submitted = st.form_submit_button("Predict sales")

    if submitted:
        payload = {
            "Product_Weight": product_weight,
            "Product_Sugar_Content": sugar,
            "Product_Allocated_Area": area,
            "Product_MRP": mrp,
            "Store_Size": size,
            "Store_Location_City_Type": city,
            "Store_Type": store_type,
            "Product_Id_char": prefix,
            "Store_Age_Years": age,
            "Product_Type_Category": category,
        }
        try:
            response = requests.post(f"{API_URL}/v1/predict", json=payload, timeout=30)
            response.raise_for_status()
            st.metric("Predicted sales revenue", f"{response.json()['predicted_sales']:,.2f}")
        except requests.RequestException as exc:
            st.error(f"Prediction service is unavailable: {exc}")

with tab_batch:
    upload = st.file_uploader("Upload a CSV with the ten model features", type="csv")
    if upload is not None:
        frame = pd.read_csv(upload)
        st.dataframe(frame.head(), use_container_width=True)
        if st.button("Run batch prediction"):
            try:
                files = {
                    "file": (
                        upload.name,
                        frame.to_csv(index=False).encode("utf-8"),
                        "text/csv",
                    )
                }
                response = requests.post(f"{API_URL}/v1/predictbatch", files=files, timeout=60)
                response.raise_for_status()
                frame["Predicted_Sales"] = response.json()["predictions"]
                st.dataframe(frame, use_container_width=True)
                st.download_button(
                    "Download predictions",
                    frame.to_csv(index=False),
                    file_name="superkart_predictions.csv",
                    mime="text/csv",
                )
            except requests.RequestException as exc:
                st.error(f"Prediction service is unavailable: {exc}")
