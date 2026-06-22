# Network Intrusion Detection App

This is a small Streamlit app I built to experiment with machine learning for network intrusion detection. It uses the NSL-KDD/KDD Cup 99 style dataset and predicts whether a network connection is normal or belongs to a specific attack type.

The main goal of the project is not to build a production security tool. I wanted to show the full workflow: preparing a dataset, training a few models, saving the best one, and connecting it to a simple interface.

## What It Does

- takes basic network traffic details from a Streamlit form
- encodes categorical fields like protocol, service, and connection flag
- predicts normal traffic or a specific attack label
- shows the broader attack family when an attack is detected
- includes a training script that compares a few models

## Models Tried

The training script compares:

- Decision Tree
- Random Forest
- Extra Trees

The best model is saved into the `model/` folder along with the label encoders used by the app.

## Project Files

```text
app.py                         Streamlit app
data/nsl_kdd.csv               Dataset used for training
model/model.pkl                Saved trained model
model/protocol_encoder.pkl     Encoder for protocol_type
model/service_encoder.pkl      Encoder for service
model/flag_encoder.pkl         Encoder for flag
scripts/train_multiclass_model.py
MULTICLASS_COLAB_CELLS.md      Copy-paste Colab training cells
requirements.txt               Python dependencies
```

## How To Run

Install the dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
streamlit run app.py
```

If Streamlit says the default port is already being used, run:

```bash
streamlit run app.py --server.port 8502
```

## Retraining

To retrain locally:

```bash
python scripts/train_multiclass_model.py
```


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

## Limitations

This is a learning project. Some NSL-KDD attack classes have very few examples, so the model is much stronger on common attacks than rare ones. That class imbalance is one of the main limitations of this dataset.
