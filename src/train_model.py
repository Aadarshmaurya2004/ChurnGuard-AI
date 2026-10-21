
from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from data_cleaning import clean_data
from feature_engineering import add_features

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "WA_Fn-UseC_-Telco-Customer-Churn.csv"
REPORT_DIR = ROOT / "reports"


def main():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)
    df = clean_data(df)

    # Convert target to binary values
    df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})
    df = df.dropna(subset=["Churn"])

    df = add_features(df)

    # Exclude identifiers and target from model inputs
    X = df.drop(columns=["Churn", "customerID"], errors="ignore")
    y = df["Churn"].astype(int)

    numeric = [
        col for col in [
            "tenure", "MonthlyCharges", "TotalCharges",
            "avg_charge_per_month"
        ] if col in X.columns
    ]

    categorical = [
        col for col in X.columns if col not in numeric
    ]

    preprocess = ColumnTransformer([
        ("num", StandardScaler(), numeric),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
    ])

    model = Pipeline([
        ("preprocess", preprocess),
        ("classifier", RandomForestClassifier(
            n_estimators=200,
            class_weight="balanced",
            random_state=42,
            n_jobs=-1
        )),
    ])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]

    print("\nClassification Report:")
    print(classification_report(y_test, predictions, zero_division=0))
    print("ROC-AUC:", round(roc_auc_score(y_test, probabilities), 3))

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report = classification_report(
        y_test, predictions, output_dict=True, zero_division=0
    )
    pd.DataFrame(report).transpose().to_csv(
        REPORT_DIR / "classification_report.csv"
    )

    print(f"\nReport saved to: {REPORT_DIR / 'classification_report.csv'}")


if __name__ == "__main__":
    main()
