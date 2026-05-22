import os
import pandas as pd

from src.data_loader import load_farms_csv
from src.preprocessing import compute_derived_features
from src.risk_model import compute_final_risk


def make_test_df(num_rows=100):
    return pd.DataFrame({
        "farm_id": [f"farm_{i}" for i in range(num_rows)],
        "latitude": [35.0 + i * 0.01 for i in range(num_rows)],
        "longitude": [127.0 + i * 0.01 for i in range(num_rows)],
        "farm_area_ha": [1.0 + (i % 5) * 0.5 for i in range(num_rows)],
        "protected_area_m2": [100.0 + (i % 3) * 50.0 for i in range(num_rows)],
        "crop_type": ["rice" if i % 2 == 0 else "maize" for i in range(num_rows)],
        "crop_area_share": [0.7 for _ in range(num_rows)],
        "max_wind_ms": [10.0 + (i % 10) for i in range(num_rows)],
        "mean_wind_ms": [8.0 + (i % 5) for i in range(num_rows)],
        "cum_precip_24h": [50.0 + (i % 20) * 2 for i in range(num_rows)],
        "cum_precip_72h": [100.0 + (i % 15) * 3 for i in range(num_rows)],
        "max_hourly_precip": [20.0 + (i % 4) * 5 for i in range(num_rows)],
        "central_pressure": [990.0 - (i % 10) for i in range(num_rows)],
        "typhoon_category": ["Tropical Storm" for _ in range(num_rows)],
        "distance_to_coast_km": [5.0 + (i % 12) for i in range(num_rows)],
        "is_lowland": [True if i % 3 == 0 else False for i in range(num_rows)],
        "elevation_m": [10.0 + (i % 8) * 2 for i in range(num_rows)],
        "slope_deg": [1.0 + (i % 6) for i in range(num_rows)],
        "soil_type": ["loam" if i % 2 == 0 else "clay" for i in range(num_rows)],
        "past_damage_count": [i % 4 for i in range(num_rows)],
        "past_loss_estimate": [1000.0 + (i % 5) * 200.0 for i in range(num_rows)],
        "insurance_covered": [True if i % 3 == 0 else False for i in range(num_rows)],
        "facility_type": ["greenhouse" if i % 2 == 0 else "open_field" for i in range(num_rows)],
        "facility_structure_score": [0.7 + (i % 4) * 0.05 for i in range(num_rows)],
        "drainage_exists": [True if i % 2 == 0 else False for i in range(num_rows)],
        "obs_source": ["sensor" for _ in range(num_rows)],
        "timestamp": ["2026-05-22 00:00:00" for _ in range(num_rows)],
        "imputed_flag": [False for _ in range(num_rows)],
    })


def test_pipeline_runs_and_outputs_final_risk():
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    sample = os.path.join(base, "data", "sample", "example_farms.csv")
    df = load_farms_csv(sample)
    df2 = compute_derived_features(df)
    df2["final_risk"] = compute_final_risk(df2)

    assert "final_risk" in df2.columns
    assert df2["final_risk"].notna().all()
    assert ((df2["final_risk"] >= 0) & (df2["final_risk"] <= 1)).all()


def test_pipeline_handles_large_dataset(tmp_path):
    csv_path = tmp_path / "large_sample.csv"
    df = make_test_df(num_rows=1000)
    df.to_csv(csv_path, index=False)

    loaded = load_farms_csv(str(csv_path))
    processed = compute_derived_features(loaded)
    processed["final_risk"] = compute_final_risk(processed)

    assert len(processed) == 1000
    assert processed["final_risk"].notna().all()
    assert ((processed["final_risk"] >= 0) & (processed["final_risk"] <= 1)).all()


def test_load_farms_csv_coerces_string_types(tmp_path):
    csv_path = tmp_path / "coerce.csv"
    df = pd.DataFrame({
        "farm_id": ["f1", "f2"],
        "latitude": ["35.0", "36.0"],
        "longitude": ["127.0", "128.0"],
        "farm_area_ha": ["1.5", "2.0"],
        "protected_area_m2": ["200", "300"],
        "crop_type": ["rice", "maize"],
        "crop_area_share": ["0.8", "0.6"],
        "max_wind_ms": ["15", "20"],
        "mean_wind_ms": ["10", "12"],
        "cum_precip_24h": ["50", "60"],
        "cum_precip_72h": ["120", "130"],
        "max_hourly_precip": ["30", "40"],
        "central_pressure": ["980", "990"],
        "typhoon_category": ["TS", "TD"],
        "distance_to_coast_km": ["5", "10"],
        "is_lowland": ["True", "False"],
        "elevation_m": ["12", "15"],
        "slope_deg": ["2", "3"],
        "soil_type": ["loam", "clay"],
        "past_damage_count": ["1", "0"],
        "past_loss_estimate": ["1000", "1200"],
        "insurance_covered": ["False", "True"],
        "facility_type": ["greenhouse", "open_field"],
        "facility_structure_score": ["0.7", "0.8"],
        "drainage_exists": ["True", "False"],
        "obs_source": ["sensor", "survey"],
        "timestamp": ["2026-05-22", "2026-05-23"],
        "imputed_flag": ["False", "True"],
    })
    df.to_csv(csv_path, index=False)

    loaded = load_farms_csv(str(csv_path))

    assert loaded["latitude"].dtype == float
    assert loaded["longitude"].dtype == float
    assert loaded["farm_area_ha"].dtype == float
    assert loaded["is_lowland"].dtype.name == "boolean"
    assert loaded["insurance_covered"].dtype.name == "boolean"
    assert loaded["drainage_exists"].dtype.name == "boolean"
    assert loaded["imputed_flag"].dtype.name == "boolean"


def test_compute_final_risk_returns_bounded_scores():
    df = make_test_df(num_rows=20)
    processed = compute_derived_features(df)
    processed["final_risk"] = compute_final_risk(processed)

    assert processed["final_risk"].between(0, 1).all()
