import streamlit as st
import pandas as pd


st.set_page_config(
    page_title="Typhoon Agricultural Damage Priority Engine",
    page_icon="🌪️",
    layout="wide",
)


st.title("🌪️ Typhoon Agricultural Damage Priority Engine")
st.subheader("태풍 농업피해 위험도 산정 및 우선확인 지원 시스템")

st.markdown(
    """
    이 프로젝트는 태풍 발생 시 지역별 강풍·강수 위험도와 농가별 작물·시설·지역 취약성을 결합하여  
    피해 가능성이 높은 농가를 우선적으로 확인하기 위한 위험도 산정 모델을 구축하는 것을 목표로 합니다.
    """
)

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("분석 대상 농가", "준비 중")

with col2:
    st.metric("고위험 농가", "준비 중")

with col3:
    st.metric("즉시 확인 대상", "준비 중")

st.divider()

st.header("프로젝트 핵심 구조")

st.markdown(
    """
    1. **지역별 강풍·강수 위험도 계산**  
    2. **농가 작물·시설·지역 취약성 반영**  
    3. **태풍 피해 위험도 점수 산정**  
    4. **우선확인 농가 리스트 생성**  
    5. **대시보드 기반 의사결정 지원**
    """
)

st.info("Day 1: 프로젝트 기본 구조 생성 완료. Day 2부터 변수 설계표를 작성합니다.")
