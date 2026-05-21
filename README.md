# Typhoon Agricultural Damage Priority Engine

## 1. Project Overview

This project aims to develop a typhoon agricultural damage risk scoring model that supports post-typhoon field inspection prioritization.

The system combines regional typhoon hazard factors such as wind and rainfall with farm-level vulnerability factors such as crop type, facility type, lowland condition, drainage weakness, and past damage history.

## 2. Korean Title

태풍 농업피해 위험도 산정 및 우선확인 지원 시스템

## 3. Problem Statement

태풍 발생 이후 농가 피해 확인은 전화, 현장 방문, 신고 접수 등 수작업 중심으로 이루어지는 경우가 많다.

이 방식은 피해 지역이 넓거나 농가 수가 많을 때 대응 지연과 업무 비효율을 초래할 수 있다.

따라서 태풍의 강풍·강수 특성과 농가의 작물·시설·지역 취약성을 결합하여 피해 가능성이 높은 농가를 우선적으로 확인할 수 있는 위험도 산정 모델이 필요하다.

## 4. Core Model Structure

Regional Typhoon Hazard  
→ Farm Vulnerability  
→ Exposure Factors  
→ Typhoon Damage Risk Score  
→ Field Inspection Priority

## 5. Main Components

- Regional wind risk scoring
- Regional rainfall risk scoring
- Farm crop vulnerability scoring
- Facility vulnerability scoring
- Exposure scoring
- Priority list generation
- Streamlit dashboard visualization

## 6. Data Policy

This repository only includes sample or synthetic data.

Do not upload:
- Personal farm information
- Real farm location data without permission
- API keys
- Private research data
- Unpublished materials

Private data should be stored locally in:

data/private/

API keys should be stored in:

.env

## 7. Current Status


- Day 1: Project structure created
- Day 2: Visualization refactor, schema validation, safer temp file handling, logging, and tests added
- Local Streamlit app runs with sample data and supports CSV upload

## 8. How to Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```
3. Upload a farm-level CSV or use the built-in sample data at `data/sample/example_farms.csv`.

## 9. Tests

Run the automated test suite with:
```bash
pytest -q
```
