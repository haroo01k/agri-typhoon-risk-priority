import pandas as pd


def compute_hazard_score(df: pd.DataFrame) -> pd.Series:
    # Assumes `hazard_wind_score` and `hazard_precip_score` exist
    wind = df.get("hazard_wind_score", pd.Series(0.0, index=df.index))
    precip = df.get("hazard_precip_score", pd.Series(0.0, index=df.index))
    combined = df.get("hazard_combined", 1 - (1 - wind) * (1 - precip))
    return combined.clip(0, 1)


def compute_vulnerability_score(df: pd.DataFrame) -> pd.Series:
    # Combine crop vulnerability, facility structure, and past damage
    crop_v = df.get("crop_vulnerability", pd.Series(0.5, index=df.index))
    facility = df.get("facility_structure_score", pd.Series(0.5, index=df.index))
    past = df.get("past_damage_count", pd.Series(0, index=df.index)).fillna(0)

    # Normalize past damage: simple sigmoid
    past_score = (1 / (1 + (1 / (1 + past))))

    # Weighted sum
    return (0.6 * crop_v + 0.3 * (1 - facility) + 0.1 * past_score).clip(0, 1)


def compute_exposure_score(df: pd.DataFrame) -> pd.Series:
    # Exposure by farm area, protected area ratio, coastal proximity, lowland
    area = df.get("farm_area_ha", pd.Series(0.0, index=df.index))
    protected = df.get("protected_area_m2", pd.Series(0.0, index=df.index))
    distance = df.get("distance_to_coast_km", pd.Series(999.0, index=df.index))
    is_lowland = df.get("is_lowland", pd.Series(False, index=df.index))

    protected_ratio = (protected / (area * 10000)).fillna(0)  # m2 per ha -> ratio
    area_score = (area / (area.max() if area.max() > 0 else 1)).clip(0, 1)
    coast_score = (1 - (distance / 50.0)).clip(0, 1)  # within 0-50km
    lowland_score = is_lowland.astype(float)

    return (0.5 * area_score + 0.2 * protected_ratio + 0.2 * coast_score + 0.1 * lowland_score).clip(0, 1)


def compute_final_risk(df: pd.DataFrame, weights: dict = None) -> pd.Series:
    if weights is None:
        weights = {"hazard": 0.5, "vulnerability": 0.3, "exposure": 0.2}

    hazard = compute_hazard_score(df)
    vuln = compute_vulnerability_score(df)
    expos = compute_exposure_score(df)

    final = (weights["hazard"] * hazard) + (weights["vulnerability"] * vuln) + (weights["exposure"] * expos)
    return final.clip(0, 1)


if __name__ == "__main__":
    import os
    from src.data_loader import load_farms_csv
    from src.preprocessing import compute_derived_features

    base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    sample = os.path.join(base, "data", "sample", "example_farms.csv")
    try:
        df = load_farms_csv(sample)
        df = compute_derived_features(df)
        df["final_risk"] = compute_final_risk(df)
        print("Final risk sample:", df[["farm_id", "final_risk"]].to_dict(orient="records"))
    except Exception as e:
        print("Risk model test failed:", e)
