import io
import logging

import streamlit as st
import pandas as pd
import os
import tempfile
from src.visualization import (
    plot_risk_distribution,
    plot_risk_map,
    get_top_risk_farms,
    count_high_risk_farms,
)

from src.data_loader import (
    load_farms_csv,
    validate_schema,
    REQUIRED_COLUMNS,
    ESSENTIAL_COLUMNS,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)
from src.preprocessing import compute_derived_features
from src.risk_model import compute_final_risk


def inspect_csv_schema(uploaded_file):
    try:
        buffer = io.BytesIO(uploaded_file.getvalue())
        df = pd.read_csv(buffer, nrows=0)
        return list(df.columns), None
    except Exception as exc:
        return None, f"CSV를 읽는 중 오류가 발생했습니다: {exc}"


def display_analysis_summary(df: pd.DataFrame, threshold: float):
    st.subheader("분석 요약")
    col1, col2, col3 = st.columns(3)
    col1.metric("농가 수", len(df))
    col2.metric("평균 최종 위험도", f"{df['final_risk'].mean():.2f}")
    col3.metric(f"위험도 > {threshold}", count_high_risk_farms(df, threshold))

    with st.expander("리스크 통계", expanded=False):
        stats = {
            "최소": f"{df['final_risk'].min():.3f}",
            "25%": f"{df['final_risk'].quantile(0.25):.3f}",
            "중앙값": f"{df['final_risk'].median():.3f}",
            "75%": f"{df['final_risk'].quantile(0.75):.3f}",
            "최대": f"{df['final_risk'].max():.3f}",
        }
        st.write(stats)


st.set_page_config(
    page_title="Typhoon Agricultural Damage Priority Engine",
    page_icon="🌪️",
    layout="wide",
)


st.title("🌪️ Typhoon Agricultural Damage Priority Engine")
st.subheader("태풍 농업피해 위험도 산정 및 우선확인 지원 시스템")

st.markdown(
    "이 프로젝트는 태풍 발생 시 지역별 강풍·강수 위험도와 농가별 취약성을 결합해 피해 가능성이 높은 농가를 우선적으로 확인합니다."
)

st.warning(
    "이 시스템은 태풍 이후 농업 피해를 최종 확정하는 모델이 아니라, "
    "우선탐색이 필요한 농가를 선별하는 의사결정 지원 프로토타입입니다."
)

st.info(
    "1) CSV 업로드 또는 샘플 데이터를 사용합니다. 2) 가중치를 확인한 뒤 분석을 실행합니다. "
    "3) 우선확인 농가 목록과 분포를 확인하여 현장조사 순위를 계획합니다."
)

st.divider()

upload_columns = []
upload_schema_error = None
missing_essential = []
missing_optional = []
extra_columns = []

with st.sidebar:
    st.header("데이터 입력")
    uploaded = st.file_uploader("CSV 파일 업로드 (farm-level)", type=["csv"])
    st.markdown("또는 샘플 데이터를 사용하려면 빈 상태로 둡니다.")

    if uploaded is not None:
        upload_columns, upload_schema_error = inspect_csv_schema(uploaded)
        if upload_schema_error:
            st.error(upload_schema_error)
        else:
            missing_essential = [c for c in ESSENTIAL_COLUMNS if c not in upload_columns]
            missing = [c for c in REQUIRED_COLUMNS if c not in upload_columns]
            missing_optional = [c for c in missing if c not in missing_essential]
            extra_columns = [c for c in upload_columns if c not in REQUIRED_COLUMNS]

            if missing_essential:
                st.error(
                    "필수 컬럼이 누락되었습니다. 다음 컬럼을 포함해 주세요: "
                    + ", ".join(missing_essential)
                )
            elif missing_optional:
                st.warning(
                    "권장 컬럼이 누락되었습니다. 결과 일부가 제한될 수 있습니다: "
                    + ", ".join(missing_optional)
                )
            else:
                st.success("필수 컬럼 검증 통과")

            if extra_columns:
                st.info(
                    "업로드된 CSV에 추가 컬럼이 포함되어 있습니다: "
                    + ", ".join(extra_columns)
                )

            with st.expander("업로드된 CSV 컬럼 요약", expanded=False):
                st.write("**업로드된 컬럼**")
                st.write(upload_columns)
                st.write("**필수 컬럼 상태**")
                for c in ESSENTIAL_COLUMNS:
                    status = "✅" if c in upload_columns else "❌"
                    st.write(f"{status} {c}")

        if uploaded is not None and getattr(uploaded, 'name', None) is not None:
            st.caption(f"업로드한 파일: {uploaded.name}")

    with st.expander("샘플 데이터 및 필수 컬럼"):
        st.markdown(
            "- 샘플 데이터: `data/sample/example_farms.csv`\n"
            "- 필수 컬럼:\n"
            "  - `farm_id`\n"
            "  - `latitude`\n"
            "  - `longitude`\n"
            "  - `farm_area_ha`\n"
            "  - `max_wind_ms`\n"
            "  - `cum_precip_72h`\n"
            "  - `facility_structure_score`\n"
            "  - `distance_to_coast_km`\n"
            "  - `is_lowland`\n"
        )
        st.caption(
            "모델은 검증 가능한 의사결정 지원을 목표로 하며, 실제 피해 확정을 대신하지 않습니다."
        )

    st.warning(
        "필수 컬럼이 누락된 CSV는 분석이 실패합니다. 누락 컬럼이 있을 경우 업로드된 파일을 확인하세요."
    )

    st.header("가중치 (초기값)")
    w_h = st.number_input("Hazard weight", min_value=0.0, max_value=1.0, value=0.5, step=0.05)
    w_v = st.number_input("Vulnerability weight", min_value=0.0, max_value=1.0, value=0.3, step=0.05)
    w_e = st.number_input("Exposure weight", min_value=0.0, max_value=1.0, value=0.2, step=0.05)

    if st.button("Run analysis"):
        if upload_schema_error:
            st.error(upload_schema_error)
        elif uploaded is not None and missing_essential:
            st.error(
                "필수 컬럼이 누락되어 분석을 실행할 수 없습니다. "
                "업로드한 CSV의 컬럼 구성을 확인해 주세요."
            )
        else:
            # Normalize weights
            s = max((w_h + w_v + w_e), 1e-6)
            weights = {"hazard": w_h / s, "vulnerability": w_v / s, "exposure": w_e / s}

            try:
                logger.info("Starting analysis run")
                if uploaded is not None:
                    tf = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
                    try:
                        tf.write(uploaded.getvalue())
                        tf.flush()
                        df = load_farms_csv(tf.name)
                    finally:
                        try:
                            tf.close()
                        except Exception:
                            logger.warning("Failed to close temporary file", exc_info=True)
                        try:
                            os.unlink(tf.name)
                        except Exception:
                            logger.warning("Failed to delete temporary file", exc_info=True)
                else:
                    sample_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "data", "sample", "example_farms.csv"))
                    df = load_farms_csv(sample_path)

                missing, extra = validate_schema(df)
                if missing:
                    st.warning(
                        "다음 권장 컬럼이 누락되었습니다. 일부 기능이 제한될 수 있습니다: "
                        + ", ".join(missing)
                    )
                if extra:
                    st.info(
                        "업로드 CSV에 인식되지 않는 추가 컬럼이 포함되어 있습니다: "
                        + ", ".join(extra)
                    )

                df = compute_derived_features(df)
                df["final_risk"] = compute_final_risk(df, weights=weights)

                st.success("분석 완료")
                st.metric("분석 대상 농가", len(df))

                # Threshold and top-N
                risk_threshold = st.slider("리스크 임계값", 0.0, 1.0, 0.7, 0.01)
                top_n = st.number_input("상위 N 농가 표시", min_value=5, max_value=500, value=50, step=5)

                high_cnt = count_high_risk_farms(df, threshold=risk_threshold)
                st.metric(f"고위험 농가(>{risk_threshold})", high_cnt)

                display_analysis_summary(df, risk_threshold)

                st.header("우선확인 농가 (상위 N)")
                top_df = get_top_risk_farms(df, top_n=top_n)
                st.dataframe(top_df)

                # Risk distribution
                st.header("리스크 분포")
                try:
                    fig = plot_risk_distribution(df)
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    logger.exception("Failed to render risk distribution")
                    st.warning("분포 시각화를 생성할 수 없습니다.")

                # Map view if coordinates available
                if {"latitude", "longitude"}.issubset(set(df.columns)):
                    st.header("지도 보기")
                    try:
                        deck = plot_risk_map(df)
                        st.pydeck_chart(deck)
                    except Exception as e:
                        logger.exception("Failed to render risk map")
                        st.warning("지도를 생성할 수 없습니다.")

                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button("결과 다운로드 (CSV)", csv, file_name="risk_results.csv", mime="text/csv")

            except ValueError as e:
                logger.warning("Validation error during analysis", exc_info=True)
                st.error(f"입력 데이터 오류: {e}")
            except Exception as e:
                logger.exception("Unexpected error during analysis")
                st.error("알 수 없는 오류가 발생했습니다. 서버 로그를 확인해 주세요.")

st.divider()

st.header("프로젝트 핵심 구조")

st.markdown(
    """
    1. 지역별 강풍·강수 위험도 계산
    2. 농가 작물·시설·지역 취약성 반영
    3. 태풍 피해 위험도 점수 산정
    4. 우선확인 농가 리스트 생성
    5. 대시보드 기반 의사결정 지원
    """
)

st.info("MVP: 파일 업로드 → 전처리 → 위험도 계산 → 결과 테이블/다운로드")
