import os
import pandas as pd

from src.data_loader import load_farms_csv
from src.preprocessing import compute_derived_features
from src.risk_model import compute_final_risk


def test_pipeline_runs_and_outputs_final_risk():
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    sample = os.path.join(base, "data", "sample", "example_farms.csv")
    df = load_farms_csv(sample)
    df2 = compute_derived_features(df)
    df2["final_risk"] = compute_final_risk(df2)

    assert "final_risk" in df2.columns
    assert df2["final_risk"].notna().all()
    assert ((df2["final_risk"] >= 0) & (df2["final_risk"] <= 1)).all()
