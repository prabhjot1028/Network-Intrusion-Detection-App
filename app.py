from pathlib import Path
import streamlit as st
import joblib
import pandas as pd
import numpy as np

# These are the usual attack families used when discussing KDD/NSL-KDD labels.
# The model predicts the exact label; this just makes the output easier to read.
ATTACK_CATEGORIES = {
    "back": "Denial of Service",
    "land": "Denial of Service",
    "neptune": "Denial of Service",
    "pod": "Denial of Service",
    "smurf": "Denial of Service",
    "teardrop": "Denial of Service",
    "ipsweep": "Probe",
    "nmap": "Probe",
    "portsweep": "Probe",
    "satan": "Probe",
    "ftp_write": "Remote to Local",
    "guess_passwd": "Remote to Local",
    "imap": "Remote to Local",
    "multihop": "Remote to Local",
    "phf": "Remote to Local",
    "spy": "Remote to Local",
    "warezclient": "Remote to Local",
    "warezmaster": "Remote to Local",
    "buffer_overflow": "User to Root",
    "loadmodule": "User to Root",
    "perl": "User to Root",
    "rootkit": "User to Root",
}


def get_attack_category(prediction):
    return ATTACK_CATEGORIES.get(str(prediction).lower(), "Unknown attack family")


st.set_page_config(
    page_title="Network Intrusion Detection System",
    layout="centered",
    initial_sidebar_state="expanded"
)

@st.cache_resource
def load_artifacts():
    """Load the model files once instead of reloading them on every Streamlit rerun."""
    model = joblib.load("model/model.pkl")
    protocol_encoder = joblib.load("model/protocol_encoder.pkl")
    service_encoder = joblib.load("model/service_encoder.pkl")
    flag_encoder_path = Path("model/flag_encoder.pkl")
    flag_encoder = joblib.load(flag_encoder_path) if flag_encoder_path.exists() else None
    return model, protocol_encoder, service_encoder, flag_encoder

model, protocol_encoder, service_encoder, flag_encoder = load_artifacts()

st.title("Network Intrusion Detection System")
st.caption(
    "A small ML demo that classifies network traffic as normal or as a specific "
    "attack type using KDD intrusion detection data."
)

st.divider()

with st.sidebar:
    st.header("About this project")
    st.write(
        """
        - **Model:** Random Forest selected after comparing a few models  
        - **Dataset:** NSL-KDD / KDD Cup 99 style data  
        - **Task:** Multi-class classification  
        - **Interface:** Streamlit  
        - **Pipeline:**  
          User Input -> Encoding -> Model -> Prediction
        """
    )

st.subheader("Enter Network Traffic Details")

# Streamlit shows the text labels, but the saved model expects encoded numbers.
protocol_mapping = {i: cls for i, cls in enumerate(protocol_encoder.classes_)}
service_mapping = {i: cls for i, cls in enumerate(service_encoder.classes_)}
flag_mapping = {i: cls for i, cls in enumerate(flag_encoder.classes_)} if flag_encoder else None

col1, col2 = st.columns(2)

with col1:
    duration = st.number_input(
        "Connection Duration (seconds)",
        min_value=0,
        help="How long the connection lasted"
    )

    protocol_encoded = st.selectbox(
        "Protocol Type",
        options=list(protocol_mapping.keys()),  # numeric labels
        format_func=lambda x: protocol_mapping[x],  # show text
        help="Transport protocol used (TCP, UDP, ICMP)"
    )

    service_encoded = st.selectbox(
        "Service",
        options=list(service_mapping.keys()),  # numeric labels
        format_func=lambda x: service_mapping[x],  # show text
        help="Network service on the destination (HTTP, FTP, SSH, etc.)"
    )

    if flag_mapping:
        flag_encoded = st.selectbox(
            "Connection Flag",
            options=list(flag_mapping.keys()),
            format_func=lambda x: flag_mapping[x],
            help="Basic connection status from the NSL-KDD dataset"
        )

with col2:
    num_failed_logins = st.number_input(
        "Failed Login Attempts",
        min_value=0,
        help="Number of failed login attempts during the session"
    )

    src_bytes = st.number_input(
        "Source Bytes",
        min_value=0,
        help="Bytes sent from source to destination"
    )

    dst_bytes = st.number_input(
        "Destination Bytes",
        min_value=0,
        help="Bytes sent from destination to source"
    )

st.divider()

if st.button("Run Detection", use_container_width=True):
    # Keep this column order the same as the Colab training cell.
    input_data = {
        "duration": duration,
        "protocol_type": protocol_encoded,
        "service": service_encoded,
        "num_failed_logins": num_failed_logins,
        "src_bytes": src_bytes,
        "dst_bytes": dst_bytes
    }

    if flag_mapping:
        input_data["flag"] = flag_encoded

    input_df = pd.DataFrame([input_data])
    st.write("Input for model:")
    st.write(input_df)

    prediction = model.predict(input_df)[0]

    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(input_df)[0]
        confidence = np.max(proba) * 100
    else:
        confidence = None

    st.subheader("Detection Result")

    prediction_text = str(prediction)

    if prediction_text.lower() == "normal":
        st.success("**Normal Traffic Detected**")
    elif prediction_text.lower() == "attack":
        st.error("**Potential Attack Detected**")
        st.info("This model is binary. Retrain with the multiclass Colab cells to show the attack name.")
    else:
        st.error(f"**Attack Detected: {prediction_text}**")
        st.write(f"**Attack family:** `{get_attack_category(prediction_text)}`")

    if confidence is not None:
        st.write(f"**Model confidence:** `{confidence:.2f}%`")

    st.caption(
        "Prediction generated using the trained machine learning model. "
        "This system is intended for educational and demonstrative purposes."
    )
