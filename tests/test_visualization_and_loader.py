import os
import tempfile
import pandas as pd
import pytest
import pydeck as pdk
import plotly.graph_objects as go

from src.data_loader import load_farms_csv, validate_schema
from src.visualization import (
    get_top_risk_farms,
    count_high_risk_farms,
    plot_risk_distribution,
    plot_risk_map,
)


def test_load_farms_csv_rejects_missing_essential_columns(tmp_path):
    csv_path = tmp_path / "bad.csv"
    df = pd.DataFrame({
        "farm_id": [1, 2],
        "latitude": [35.0, 36.0],
        "longitude": [127.0, 128.0],
        # missing required "farm_area_ha" and other essential columns
        "max_wind_ms": [10, 20],
        "cum_precip_72h": [100, 200],
        "facility_structure_score": [0.8, 0.9],
        "distance_to_coast_km": [5.0, 12.0],
        "is_lowland": [True, False],
    })
    df.to_csv(csv_path, index=False)

    with pytest.raises(ValueError, match="필수 컬럼이 누락되었습니다"):
        load_farms_csv(str(csv_path))


def test_validate_schema_reports_missing_and_extra():
    df = pd.DataFrame({
        "farm_id": [1],
        "latitude": [35.0],
        "longitude": [127.0],
        "farm_area_ha": [1.0],
        "max_wind_ms": [15.0],
        "cum_precip_72h": [120.0],
        "facility_structure_score": [0.5],
        "distance_to_coast_km": [3.0],
        "is_lowland": [False],
        "unknown_col": [42],
    })

    missing, extra = validate_schema(df)
    assert "farm_id" not in missing
    assert "unknown_col" in extra


def test_plot_risk_distribution_returns_figure():
    df = pd.DataFrame({
        "final_risk": [0.1, 0.5, 0.9],
    })
    fig = plot_risk_distribution(df)
    assert isinstance(fig, go.Figure)
    assert fig.data[0].x.tolist() == [0.1, 0.5, 0.9]


def test_plot_risk_map_returns_deck():
    df = pd.DataFrame({
        "farm_id": ["A", "B"],
        "latitude": [35.0, 35.5],
        "longitude": [127.0, 127.5],
        "final_risk": [0.2, 0.8],
    })
    deck = plot_risk_map(df)
    assert isinstance(deck, pdk.Deck)
    assert deck.layers[0].id is not None or deck.layers[0].type == "ScatterplotLayer"


def test_get_top_risk_farms_and_count_high_risk():
    df = pd.DataFrame({
        "farm_id": ["f1", "f2", "f3"],
        "final_risk": [0.2, 0.9, 0.6],
    })
    top = get_top_risk_farms(df, top_n=2)
    assert list(top["farm_id"]) == ["f2", "f3"]
    assert count_high_risk_farms(df, threshold=0.5) == 2
