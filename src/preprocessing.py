import pandas as pd
import numpy as np
from typing import Dict


def _clip_ranges(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "max_wind_ms" in df.columns:
        df["max_wind_ms"] = df["max_wind_ms"].clip(lower=0, upper=80)
    if "cum_precip_24h" in df.columns:
        df["cum_precip_24h"] = df["cum_precip_24h"].clip(lower=0, upper=3000)
    if "cum_precip_72h" in df.columns:
        df["cum_precip_72h"] = df["cum_precip_72h"].clip(lower=0, upper=5000)
    if "central_pressure" in df.columns:
        df["central_pressure"] = df["central_pressure"].clip(lower=800, upper=1100)
    if "facility_structure_score" in df.columns:
        df["facility_structure_score"] = df["facility_structure_score"].clip(lower=0.0, upper=1.0)
    if "crop_area_share" in df.columns:
        df["crop_area_share"] = df["crop_area_share"].clip(lower=0.0, upper=1.0)
    return df


def _impute_missing(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # Numeric imputation: median by column
    num_cols = df.select_dtypes(include=["number"]).columns
    for c in num_cols:
        if df[c].isna().any():
            df[c] = df[c].fillna(df[c].median())

    # Boolean imputation: fill False
    bool_cols = df.select_dtypes(include=["boolean"]).columns
    for c in bool_cols:
        df[c] = df[c].fillna(False)

    # Timestamp: leave as-is (could be imputed externally)
    return df


def compute_hazard_wind_score(df: pd.DataFrame) -> pd.Series:
    # Simple linear scaling: 0–80 m/s -> 0–1
    s = df.get("max_wind_ms")
    if s is None:
        return pd.Series(dtype=float)
    return (s / 80.0).clip(0, 1)


def compute_hazard_precip_score(df: pd.DataFrame) -> pd.Series:
    # Combined precip (72h) scaling: 0–300 mm -> 0–1 (loose scaling)
    s = df.get("cum_precip_72h")
    if s is None:
        return pd.Series(dtype=float)
    return (s / 300.0).clip(0, 1)


def compute_hazard_combined(wind_score: pd.Series, precip_score: pd.Series) -> pd.Series:
    # Combine as union-like: 1 - (1-w)*(1-p)
    return (1 - (1 - wind_score) * (1 - precip_score)).clip(0, 1)


def compute_inundation_risk(df: pd.DataFrame) -> pd.Series:
    # Heuristic: based on precip, elevation, soil
    precip = df.get("cum_precip_72h")
    elev = df.get("elevation_m")
    soil = df.get("soil_type") if "soil_type" in df.columns else None

    base = (precip / 300.0).clip(0, 1)

    elev_factor = 1.0
    if elev is not None:
        elev_factor = (1 - (elev / 500.0)).clip(0, 1)

    soil_factor_map: Dict[str, float] = {"sand": 0.6, "loam": 0.8, "clay": 1.0}
    soil_factor = pd.Series(1.0, index=df.index)
    if soil is not None:
        soil_factor = soil.map(soil_factor_map).fillna(0.8)

    return (base * elev_factor * soil_factor).clip(0, 1)


def compute_crop_vulnerability(df: pd.DataFrame) -> pd.Series:
    # Map crop_types to sensitivity
    mapping = {
        "rice": 0.6,
        "maize": 0.5,
        "tomato": 0.8,
        "leafy": 0.9,
        "orchard": 0.4,
    }
    crop = df.get("crop_type")
    sens = pd.Series(0.5, index=df.index)
    if crop is not None:
        sens = crop.map(mapping).fillna(0.5)

    # growth stage multiplier
    stage = df.get("growth_stage")
    stage_map = {"seedling": 1.0, "vegetative": 0.8, "flowering": 1.0, "harvest": 1.2}
    stage_s = pd.Series(1.0, index=df.index)
    if stage is not None:
        stage_s = stage.map(stage_map).fillna(1.0)

    return (sens * stage_s).clip(0, 2)


def compute_derived_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = _clip_ranges(df)
    df = _impute_missing(df)

    wind_score = compute_hazard_wind_score(df)
    precip_score = compute_hazard_precip_score(df)
    combined = compute_hazard_combined(wind_score, precip_score)
    inundation = compute_inundation_risk(df)
    crop_vul = compute_crop_vulnerability(df)

    df["hazard_wind_score"] = wind_score
    df["hazard_precip_score"] = precip_score
    df["hazard_combined"] = combined
    df["inundation_risk"] = inundation
    df["crop_vulnerability"] = crop_vul

    return df


if __name__ == "__main__":
    import os
    from src.data_loader import load_farms_csv

    base = os.path.join(os.path.dirname(__file__), "..")
    sample = os.path.abspath(os.path.join(base, "data", "sample", "example_farms.csv"))
    try:
        df = load_farms_csv(sample)
        df2 = compute_derived_features(df)
        print("Derived columns:", [c for c in df2.columns if c.startswith("hazard_") or c.endswith("vulnerability") or c.endswith("risk")])
        print(df2[["farm_id", "hazard_combined", "inundation_risk", "crop_vulnerability"]].head().to_dict(orient="records"))
    except Exception as e:
        print("Preprocessing test failed:", e)
