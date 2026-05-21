"""
Visualization module for typhoon agricultural damage risk analysis.

Provides reusable plotting and analysis functions to generate
charts, maps, and diagnostic views without Streamlit dependencies.
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from typing import Optional, Tuple
import pydeck as pdk


# ============================================================================
# CORE PLOTTING FUNCTIONS (extracted from app.py)
# ============================================================================

def get_top_risk_farms(
    df: pd.DataFrame,
    top_n: int = 50,
    include_cols: Optional[list] = None
) -> pd.DataFrame:
    """
    Extract top N farms by final_risk score in descending order.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe with 'final_risk' column
    top_n : int
        Number of top farms to return (default: 50)
    include_cols : list, optional
        Specific columns to include. If None, returns all columns.
    
    Returns
    -------
    pd.DataFrame
        Top N farms sorted by final_risk (descending)
    """
    df_sorted = df.sort_values("final_risk", ascending=False)
    result = df_sorted.head(top_n)
    
    if include_cols is not None:
        missing = [c for c in include_cols if c not in result.columns]
        if missing:
            raise ValueError(f"Columns not found: {missing}")
        result = result[include_cols]
    
    return result


def count_high_risk_farms(
    df: pd.DataFrame,
    threshold: float = 0.7
) -> int:
    """
    Count farms exceeding a risk threshold.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe with 'final_risk' column
    threshold : float
        Risk threshold (default: 0.7)
    
    Returns
    -------
    int
        Number of farms with final_risk > threshold
    """
    return int((df["final_risk"] > threshold).sum())


def plot_risk_distribution(
    df: pd.DataFrame,
    nbins: int = 40,
    title: str = "Final Risk Distribution"
) -> go.Figure:
    """
    Generate histogram of final risk scores.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe with 'final_risk' column
    nbins : int
        Number of histogram bins (default: 40)
    title : str
        Chart title
    
    Returns
    -------
    plotly.graph_objects.Figure
        Histogram figure
    """
    fig = px.histogram(
        df,
        x="final_risk",
        nbins=nbins,
        title=title,
        labels={"final_risk": "Risk Score (0-1)"},
        color_discrete_sequence=["#636EFA"]
    )
    fig.update_layout(
        xaxis_title="Risk Score",
        yaxis_title="Number of Farms",
        hovermode="x unified"
    )
    return fig


def prepare_map_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare dataframe for map visualization by normalizing coordinates.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe with 'latitude', 'longitude', and 'final_risk' columns
    
    Returns
    -------
    pd.DataFrame
        Cleaned map data with 'lat', 'lon', and risk-based color encoding
    """
    map_df = df.dropna(subset=["latitude", "longitude"]).copy()
    map_df["lat"] = map_df["latitude"].astype(float)
    map_df["lon"] = map_df["longitude"].astype(float)
    return map_df


def plot_risk_map(
    df: pd.DataFrame,
    zoom: int = 6,
    pitch: int = 0,
    point_radius: int = 200
) -> pdk.Deck:
    """
    Generate pydeck map visualization with farms colored by risk level.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe with 'latitude', 'longitude', and 'final_risk' columns
    zoom : int
        Map zoom level (default: 6)
    pitch : int
        Map pitch/tilt angle in degrees (default: 0)
    point_radius : int
        Radius of farm points on map (default: 200)
    
    Returns
    -------
    pydeck.Deck
        Interactive map object ready for Streamlit rendering
    """
    map_df = prepare_map_data(df)
    
    if len(map_df) == 0:
        raise ValueError("No valid coordinates found in dataframe")
    
    # Color by risk: red (high) → yellow → green (low)
    # Using [R, G, B, Alpha] format
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=map_df,
        get_position="[lon, lat]",
        # Normalize risk to RGB: high risk = red (255, 0, 50), low risk = green (0, 255, 50)
        get_fill_color="[final_risk * 255, (1-final_risk)*255, 50, 200]",
        get_radius=point_radius,
        pickable=True,
    )
    
    view_state = pdk.ViewState(
        latitude=map_df["lat"].mean(),
        longitude=map_df["lon"].mean(),
        zoom=zoom,
        pitch=pitch
    )
    
    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "{farm_id}\nRisk: {final_risk:.3f}"}
    )
    
    return deck


# ============================================================================
# EXTENDED ANALYSIS FUNCTIONS
# ============================================================================

def plot_component_distribution(
    df: pd.DataFrame,
    component_cols: list = ["hazard_wind_score", "hazard_precip_score"],
    nbins: int = 30
) -> go.Figure:
    """
    Generate overlaid histograms for multiple risk components.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe
    component_cols : list
        Column names to plot (default: wind and precip scores)
    nbins : int
        Number of histogram bins (default: 30)
    
    Returns
    -------
    plotly.graph_objects.Figure
        Overlaid histogram figure
    """
    fig = go.Figure()
    
    colors = ["#636EFA", "#EF553B", "#00CC96", "#AB63FA"]
    for i, col in enumerate(component_cols):
        if col in df.columns:
            fig.add_trace(go.Histogram(
                x=df[col],
                name=col,
                nbinsx=nbins,
                opacity=0.7,
                marker_color=colors[i % len(colors)]
            ))
    
    fig.update_layout(
        barmode="overlay",
        title="Distribution of Risk Components",
        xaxis_title="Score (0-1)",
        yaxis_title="Frequency",
        hovermode="x unified"
    )
    return fig


def plot_score_components_boxplot(
    df: pd.DataFrame,
    score_cols: list = ["hazard_combined", "crop_vulnerability", "farm_area_ha"]
) -> go.Figure:
    """
    Generate box plot comparing multiple score distributions.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe
    score_cols : list
        Columns to compare
    
    Returns
    -------
    plotly.graph_objects.Figure
        Box plot figure
    """
    data = []
    for col in score_cols:
        if col in df.columns:
            data.append(go.Box(y=df[col], name=col))
    
    fig = go.Figure(data=data)
    fig.update_layout(
        title="Comparison of Risk Component Distributions",
        yaxis_title="Score",
        hovermode="y unified"
    )
    return fig


def plot_top_farms_ranking(
    df: pd.DataFrame,
    top_n: int = 20,
    include_farm_id: bool = True
) -> go.Figure:
    """
    Generate bar chart ranking top N farms by risk.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe with 'final_risk' and optionally 'farm_id'
    top_n : int
        Number of top farms to display (default: 20)
    include_farm_id : bool
        Whether to use farm_id as x-axis label (default: True)
    
    Returns
    -------
    plotly.graph_objects.Figure
        Bar chart figure
    """
    top_df = get_top_risk_farms(df, top_n=top_n)
    
    if include_farm_id and "farm_id" in top_df.columns:
        x_col = "farm_id"
        labels = {"final_risk": "Risk Score", "farm_id": "Farm ID"}
    else:
        top_df = top_df.reset_index(drop=True)
        top_df["rank"] = range(1, len(top_df) + 1)
        x_col = "rank"
        labels = {"final_risk": "Risk Score", "rank": "Rank"}
    
    fig = px.bar(
        top_df,
        x=x_col,
        y="final_risk",
        title=f"Top {top_n} Farms by Risk Score",
        labels=labels,
        color="final_risk",
        color_continuous_scale="RdYlGn_r"
    )
    fig.update_layout(
        xaxis_title=labels.get(x_col, x_col),
        yaxis_title="Risk Score (0-1)",
        hovermode="x unified"
    )
    return fig


def calculate_correlation_matrix(
    df: pd.DataFrame,
    target_col: str = "final_risk",
    exclude_cols: Optional[list] = None
) -> pd.DataFrame:
    """
    Calculate correlation between all numeric columns and target.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe
    target_col : str
        Target column to correlate against (default: 'final_risk')
    exclude_cols : list, optional
        Columns to exclude from analysis
    
    Returns
    -------
    pd.DataFrame
        Correlation matrix sorted by absolute correlation with target
    """
    if target_col not in df.columns:
        raise ValueError(f"Target column '{target_col}' not found")
    
    # Select numeric columns
    numeric_df = df.select_dtypes(include=[np.number]).copy()
    
    # Exclude specified columns
    if exclude_cols:
        numeric_df = numeric_df.drop(columns=[c for c in exclude_cols if c in numeric_df.columns])
    
    # Calculate correlation with target
    corr = numeric_df.corr(numeric_only=True)[target_col].sort_values(ascending=False)
    
    return corr


def plot_correlation_heatmap(
    df: pd.DataFrame,
    target_cols: Optional[list] = None,
    min_correlation: float = 0.1
) -> go.Figure:
    """
    Generate heatmap of correlations between variables and risk components.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe
    target_cols : list, optional
        Columns to include in heatmap. If None, uses all numeric columns
        with sufficient correlation.
    min_correlation : float
        Minimum absolute correlation to include (default: 0.1)
    
    Returns
    -------
    plotly.graph_objects.Figure
        Heatmap figure
    """
    numeric_df = df.select_dtypes(include=[np.number])
    
    if target_cols:
        numeric_df = numeric_df[[c for c in target_cols if c in numeric_df.columns]]
    
    corr_matrix = numeric_df.corr(numeric_only=True)
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale="RdBu",
        zmid=0,
        zmin=-1,
        zmax=1
    ))
    
    fig.update_layout(
        title="Variable Correlation Matrix",
        xaxis_title="Variables",
        yaxis_title="Variables",
        width=700,
        height=600
    )
    return fig


def plot_contribution_breakdown(
    df: pd.DataFrame,
    weight_dict: dict = None
) -> go.Figure:
    """
    Generate stacked bar chart showing contribution of each component to final risk.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe with component scores and final_risk
    weight_dict : dict, optional
        Weights used in final_risk calculation. If None, uses defaults.
    
    Returns
    -------
    plotly.graph_objects.Figure
        Stacked bar chart figure
    """
    if weight_dict is None:
        weight_dict = {"hazard": 0.5, "vulnerability": 0.3, "exposure": 0.2}
    
    # Calculate contributions for top 20 farms
    top_df = get_top_risk_farms(df, top_n=20)
    
    contributions = pd.DataFrame(index=top_df.index)
    
    if "hazard_combined" in top_df.columns:
        contributions["Hazard"] = top_df["hazard_combined"] * weight_dict.get("hazard", 0.5)
    
    if "crop_vulnerability" in top_df.columns or "vulnerability_score" in top_df.columns:
        vuln_col = "crop_vulnerability" if "crop_vulnerability" in top_df.columns else "vulnerability_score"
        contributions["Vulnerability"] = top_df[vuln_col] * weight_dict.get("vulnerability", 0.3)
    
    if "farm_area_ha" in top_df.columns:
        # Approximate exposure from area (simplified)
        contributions["Exposure"] = (top_df["farm_area_ha"] / top_df["farm_area_ha"].max()) * weight_dict.get("exposure", 0.2)
    
    # Add farm labels if available
    if "farm_id" in top_df.columns:
        contributions["farm_id"] = top_df["farm_id"].values
    
    fig = go.Figure()
    for col in ["Hazard", "Vulnerability", "Exposure"]:
        if col in contributions.columns:
            fig.add_trace(go.Bar(
                x=range(len(contributions)),
                y=contributions[col],
                name=col
            ))
    
    fig.update_layout(
        barmode="stack",
        title="Risk Score Contribution Breakdown (Top 20 Farms)",
        xaxis_title="Farm Rank",
        yaxis_title="Contribution to Risk Score",
        hovermode="x unified"
    )
    return fig


def generate_farm_summary_stats(df: pd.DataFrame) -> dict:
    """
    Generate summary statistics for risk analysis report.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe with 'final_risk' column
    
    Returns
    -------
    dict
        Summary statistics dictionary
    """
    stats = {
        "total_farms": len(df),
        "mean_risk": df["final_risk"].mean(),
        "median_risk": df["final_risk"].median(),
        "std_risk": df["final_risk"].std(),
        "min_risk": df["final_risk"].min(),
        "max_risk": df["final_risk"].max(),
        "high_risk_count_70": count_high_risk_farms(df, 0.7),
        "high_risk_count_80": count_high_risk_farms(df, 0.8),
        "high_risk_count_90": count_high_risk_farms(df, 0.9),
    }
    
    # Add percentiles
    for p in [25, 50, 75, 90, 95]:
        stats[f"percentile_{p}"] = df["final_risk"].quantile(p / 100.0)
    
    return stats
