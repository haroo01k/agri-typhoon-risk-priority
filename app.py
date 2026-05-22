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

from src.data_loader import load_farms_csv, validate_schema

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)
from src.preprocessing import compute_derived_features
from src.risk_model import compute_final_risk


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

st.divider()

with st.sidebar:
    st.header("데이터 입력")
    uploaded = st.file_uploader("CSV 파일 업로드 (farm-level)", type=["csv"])
    st.markdown("또는 샘플 데이터를 사용하려면 빈 상태로 둡니다.")

    with st.expander("샘플 데이터 및 필수 컬럼"):
        st.markdown(
            "- 샘플 데이터: `data/sample/example_farms.csv`\n"
            "- 업로드 시 `farm_id`, `latitude`, `longitude`, `farm_area_ha`, `max_wind_ms`, `cum_precip_72h`, `facility_structure_score`, `distance_to_coast_km`, `is_lowland` 컬럼이 필요합니다."
        )
        st.caption(
            "모델은 검증 가능한 의사결정 지원을 목표로 하며, 실제 피해 확정을 대신하지 않습니다."
        )

    st.header("가중치 (초기값)")
    w_h = st.number_input("Hazard weight", min_value=0.0, max_value=1.0, value=0.5, step=0.05)
    w_v = st.number_input("Vulnerability weight", min_value=0.0, max_value=1.0, value=0.3, step=0.05)
    w_e = st.number_input("Exposure weight", min_value=0.0, max_value=1.0, value=0.2, step=0.05)

    if st.button("Run analysis"):
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
