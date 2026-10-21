"""Feature engineering for the churn project."""
import pandas as pd


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["tenure_group"] = pd.cut(df["tenure"], bins=[-1, 12, 36, 1000],
                                labels=["0-12", "13-36", "37+"])
    df["avg_charge_per_month"] = df["TotalCharges"] / (df["tenure"] + 1)
    return df
