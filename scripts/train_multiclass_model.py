import joblib
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier


COLUMNS = [
    "duration",
    "protocol_type",
    "service",
    "flag",
    "src_bytes",
    "dst_bytes",
    "land",
    "wrong_fragment",
    "urgent",
    "hot",
    "num_failed_logins",
    "logged_in",
    "num_compromised",
    "root_shell",
    "su_attempted",
    "num_root",
    "num_file_creations",
    "num_shells",
    "num_access_files",
    "num_outbound_cmds",
    "is_host_login",
    "is_guest_login",
    "count",
    "srv_count",
    "serror_rate",
    "srv_serror_rate",
    "rerror_rate",
    "srv_rerror_rate",
    "same_srv_rate",
    "diff_srv_rate",
    "srv_diff_host_rate",
    "dst_host_count",
    "dst_host_srv_count",
    "dst_host_same_srv_rate",
    "dst_host_diff_srv_rate",
    "dst_host_same_src_port_rate",
    "dst_host_srv_diff_host_rate",
    "dst_host_serror_rate",
    "dst_host_srv_serror_rate",
    "dst_host_rerror_rate",
    "dst_host_srv_rerror_rate",
    "label",
    "difficulty",
]

FEATURES = [
    "duration",
    "protocol_type",
    "service",
    "num_failed_logins",
    "src_bytes",
    "dst_bytes",
    "flag",
]


def main():
    df = pd.read_csv("data/nsl_kdd.csv", header=None, names=COLUMNS)
    df = df[FEATURES + ["label"]].copy()

    protocol_encoder = LabelEncoder()
    service_encoder = LabelEncoder()
    flag_encoder = LabelEncoder()

    df["protocol_type"] = protocol_encoder.fit_transform(df["protocol_type"])
    df["service"] = service_encoder.fit_transform(df["service"])
    df["flag"] = flag_encoder.fit_transform(df["flag"])

    X = df[FEATURES]
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    models = {
        "Decision Tree": DecisionTreeClassifier(random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=150, random_state=42, n_jobs=1),
        "Extra Trees": ExtraTreesClassifier(n_estimators=150, random_state=42, n_jobs=1),
    }

    best_name = ""
    best_model = None
    best_accuracy = 0

    for name, model in models.items():
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)

        print(f"\n{name}")
        print(f"Accuracy: {accuracy:.4f}")
        print(classification_report(y_test, predictions, zero_division=0))

        if accuracy > best_accuracy:
            best_name = name
            best_model = model
            best_accuracy = accuracy

    # Save the model and encoders together so the Streamlit app uses matching labels.
    joblib.dump(best_model, "model/model.pkl")
    joblib.dump(protocol_encoder, "model/protocol_encoder.pkl")
    joblib.dump(service_encoder, "model/service_encoder.pkl")
    joblib.dump(flag_encoder, "model/flag_encoder.pkl")

    print(f"\nSaved best model: {best_name} ({best_accuracy:.4f})")


if __name__ == "__main__":
    main()
