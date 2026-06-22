# Multiclass Training Cells

These are the Colab cells I would use to retrain the app so it predicts the actual attack label instead of only saying "attack".

## Cell 1 - Imports

```python
!pip -q install pandas joblib scikit-learn==1.8.0

import pandas as pd
import joblib
from google.colab import files

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
```

## Cell 2 - Upload and prepare the dataset

```python
uploaded = files.upload()
csv_name = next(iter(uploaded))

columns = [
    "duration","protocol_type","service","flag","src_bytes","dst_bytes","land",
    "wrong_fragment","urgent","hot","num_failed_logins","logged_in",
    "num_compromised","root_shell","su_attempted","num_root","num_file_creations",
    "num_shells","num_access_files","num_outbound_cmds","is_host_login",
    "is_guest_login","count","srv_count","serror_rate","srv_serror_rate",
    "rerror_rate","srv_rerror_rate","same_srv_rate","diff_srv_rate",
    "srv_diff_host_rate","dst_host_count","dst_host_srv_count",
    "dst_host_same_srv_rate","dst_host_diff_srv_rate",
    "dst_host_same_src_port_rate","dst_host_srv_diff_host_rate",
    "dst_host_serror_rate","dst_host_srv_serror_rate","dst_host_rerror_rate",
    "dst_host_srv_rerror_rate","label","difficulty"
]

features = [
    "duration",
    "protocol_type",
    "service",
    "num_failed_logins",
    "src_bytes",
    "dst_bytes",
    "flag",
]

df = pd.read_csv(csv_name, header=None, names=columns)
df = df[features + ["label"]].copy()

protocol_encoder = LabelEncoder()
service_encoder = LabelEncoder()
flag_encoder = LabelEncoder()

df["protocol_type"] = protocol_encoder.fit_transform(df["protocol_type"])
df["service"] = service_encoder.fit_transform(df["service"])
df["flag"] = flag_encoder.fit_transform(df["flag"])

X = df[features]
y = df["label"]   # Keep the original labels so the app can show names like neptune or satan.

print(y.value_counts())
```

## Cell 3 - Train and compare models

```python
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)

models = {
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "Random Forest": RandomForestClassifier(n_estimators=150, random_state=42, n_jobs=-1),
    "Extra Trees": ExtraTreesClassifier(n_estimators=150, random_state=42, n_jobs=-1),
}

best_name = None
best_model = None
best_accuracy = 0

for name, model in models.items():
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)

    print(f"\n{name}")
    print("Accuracy:", acc)
    print(classification_report(y_test, preds, zero_division=0))

    if acc > best_accuracy:
        best_name = name
        best_model = model
        best_accuracy = acc

print("\nBest model:", best_name)
print("Best accuracy:", best_accuracy)
```

## Cell 4 - Download the files for Streamlit

```python
joblib.dump(best_model, "model.pkl")
joblib.dump(protocol_encoder, "protocol_encoder.pkl")
joblib.dump(service_encoder, "service_encoder.pkl")
joblib.dump(flag_encoder, "flag_encoder.pkl")

files.download("model.pkl")
files.download("protocol_encoder.pkl")
files.download("service_encoder.pkl")
files.download("flag_encoder.pkl")
```

Put the downloaded files in the project's `model` folder, replacing the old ones, then run:

```bash
streamlit run app.py
```
