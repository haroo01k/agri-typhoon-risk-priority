import logging

import pandas as pd
from typing import List, Tuple

logger = logging.getLogger(__name__)

REQUIRED_COLUMNS: List[str] = [
    "farm_id",
    "latitude",
    "longitude",
    "farm_area_ha",
    "protected_area_m2",
    "crop_type",
    "crop_area_share",
    "max_wind_ms",
    "mean_wind_ms",
    "cum_precip_24h",
    "cum_precip_72h",
    "max_hourly_precip",
    "central_pressure",
    "typhoon_category",
    "distance_to_coast_km",
    "is_lowland",
    "elevation_m",
    "slope_deg",
    "soil_type",
    "past_damage_count",
    "past_loss_estimate",
    "insurance_covered",
    "facility_type",
    "facility_structure_score",
    "drainage_exists",
    "obs_source",
    "timestamp",
    "imputed_flag",
]

ESSENTIAL_COLUMNS: List[str] = [
    "farm_id",
    "latitude",
    "longitude",
    "farm_area_ha",
    "max_wind_ms",
    "cum_precip_72h",
    "facility_structure_score",
    "distance_to_coast_km",
    "is_lowland",
]


def validate_schema(df: pd.DataFrame) -> Tuple[List[str], List[str]]:
    """Validate dataframe columns against REQUIRED_COLUMNS.

    Returns (missing_columns, extra_columns).
    """
    cols = list(df.columns)
    missing = [c for c in REQUIRED_COLUMNS if c not in cols]
    extra = [c for c in cols if c not in REQUIRED_COLUMNS]
    return missing, extra


def _coerce_types(df: pd.DataFrame) -> pd.DataFrame:
    """Attempt to coerce common columns to sensible dtypes.

    Does not fail on errors — logs by raising ValueError for immediate attention.
    """
    df = df.copy()

    float_cols = [
        "latitude",
        "longitude",
        "farm_area_ha",
        "protected_area_m2",
        "crop_area_share",
        "max_wind_ms",
        "mean_wind_ms",
        "cum_precip_24h",
        "cum_precip_72h",
        "max_hourly_precip",
        "central_pressure",
        "distance_to_coast_km",
        "elevation_m",
        "slope_deg",
        "facility_structure_score",
    ]
    int_cols = ["past_damage_count"]
    bool_cols = ["is_lowland", "insurance_covered", "drainage_exists", "imputed_flag"]

    for c in float_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    for c in int_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce").astype("Int64")

    for c in bool_cols:
        if c in df.columns:
            # Accept True/False, 1/0, 'true'/'false'
            df[c] = df[c].map({"True": True, "False": False, "true": True, "false": False}).fillna(df[c])
            df[c] = df[c].astype("boolean")

    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    return df


def load_farms_csv(path: str) -> pd.DataFrame:
    """Load farm-level sample CSV and perform basic schema validation and type coercion.

    - Reads CSV with pandas
    - Validates required columns; raises ValueError if many required columns missing
    - Coerces common numeric/boolean/datetime types
    - Returns cleaned DataFrame
    """
    df = pd.read_csv(path)
    missing, extra = validate_schema(df)
    missing_essential = [c for c in ESSENTIAL_COLUMNS if c not in df.columns]
    if missing_essential:
        raise ValueError(
            f"필수 컬럼이 누락되었습니다: {missing_essential}. 업로드한 CSV에 해당 컬럼을 포함해주세요."
        )
    if missing:
        # Warn on less important missing columns, but proceed if essential fields exist
        if len(missing) > 0:
            logger.warning("Recommended columns missing from %s: %s", path, missing)
    df = _coerce_types(df)

    # Ensure imputed_flag exists
    if "imputed_flag" not in df.columns:
        df["imputed_flag"] = False

    return df


if __name__ == "__main__":
    import os
    sample_path = os.path.join(os.path.dirname(__file__), "..", "data", "sample", "example_farms.csv")
    sample_path = os.path.abspath(sample_path)
    try:
        df = load_farms_csv(sample_path)
        print("Loaded sample farms: ", df.shape)
        print(df.head(1).to_dict(orient="records"))
    except Exception as e:
        print("Error loading sample data:", e)
