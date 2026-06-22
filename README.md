# Network Intrusion Detection App

A simple Streamlit project that uses machine learning to classify network traffic from the NSL-KDD/KDD Cup 99 style dataset. The app takes a few traffic features, encodes the categorical values, and predicts whether the traffic is normal or a specific attack type.

This is meant to be a student portfolio project showing:

- basic data preprocessing
- training and comparing different ML models
- saving trained models with `joblib`
- connecting a trained model to a Streamlit interface

## Features

- Streamlit web interface for manual testing
- Multiclass attack prediction, not just normal vs attack
- Attack family display for common NSL-KDD attack labels
- Training script that compares Decision Tree, Random Forest, and Extra Trees
- Colab-ready notebook cells in `MULTICLASS_COLAB_CELLS.md`

## Project Structure

```text
.
├── app.py
├── data/
│   └── nsl_kdd.csv
├── model/
│   ├── model.pkl
│   ├── protocol_encoder.pkl
│   ├── service_encoder.pkl
│   └── flag_encoder.pkl
├── notebooks/
│   └── 01_training.ipynb
├── scripts/
│   └── train_multiclass_model.py
├── MULTICLASS_COLAB_CELLS.md
└── requirements.txt
```

## How To Run

Create a virtual environment if you want to keep dependencies separate, then install the requirements:

```bash
pip install -r requirements.txt
```

Start the Streamlit app:

```bash
streamlit run app.py
```

If the default Streamlit port is busy, run:

```bash
streamlit run app.py --server.port 8502
```

## Retraining The Model

To retrain locally:

```bash
python scripts/train_multiclass_model.py
```

The script trains and compares:

- Decision Tree
- Random Forest
- Extra Trees

It saves the best model and encoders into the `model/` folder.

For Google Colab, copy the cells from `MULTICLASS_COLAB_CELLS.md`.

## Sample Inputs

### Normal Traffic

```text
Duration: 0
Protocol Type: tcp
Service: ftp_data
Connection Flag: SF
Failed Login Attempts: 0
Source Bytes: 491
Destination Bytes: 0
```

Expected output:

```text
Normal Traffic Detected
```

### Neptune Attack

```text
Duration: 0
Protocol Type: tcp
Service: private
Connection Flag: S0
Failed Login Attempts: 0
Source Bytes: 0
Destination Bytes: 0
```

Expected output:

```text
Attack Detected: neptune
Attack family: Denial of Service
```

### Guess Password Attack

```text
Duration: 0
Protocol Type: tcp
Service: telnet
Connection Flag: RSTO
Failed Login Attempts: 1
Source Bytes: 125
Destination Bytes: 179
```

Expected output:

```text
Attack Detected: guess_passwd
Attack family: Remote to Local
```

## Notes

This project is for learning and demonstration. Some attack classes in NSL-KDD have very few examples, so the model performs better on common classes than on rare attacks.
