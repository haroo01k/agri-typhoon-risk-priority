
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
 * Local Streamlit app runs with sample data and supports CSV upload

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

# Typhoon Agricultural Damage Priority Engine

## 1. Project Overview

This repository contains a prototype decision-support system for prioritizing post-typhoon agricultural field inspections.

It uses regional typhoon hazard indicators and farm-level vulnerability/exposure features to highlight farms that should be checked first after a storm.

## 2. What This Is

- A prototype for post-typhoon agricultural damage prioritization.
- A decision-support tool, not a confirmed damage assessment model.
- Designed for early-stage field survey planning and prioritization.

## 3. What This Is Not

- Not a substitute for on-site damage verification.
- Not an official insurance loss estimator.
- Not a final classification of actual crop loss.

## 4. How It Works

1. Load farm-level `CSV` data or use the included sample file.
2. Apply simple hazard, vulnerability, and exposure scoring.
3. Combine component scores into a normalized risk ranking.
4. Display top-priority farms, risk distribution, and map views.
5. Export the ranked results for field inspection planning.

## 5. Input Data

The system expects a farm-level CSV with at least the following essential columns:

- `farm_id`
- `latitude`
- `longitude`
- `farm_area_ha`
- `max_wind_ms`
- `cum_precip_72h`
- `facility_structure_score`
- `distance_to_coast_km`
- `is_lowland`

Additional columns improve the model and reporting, but the core workflow can run with the essential fields.

Sample data is available at:

- `data/sample/example_farms.csv`

## 6. Project Scope

This project emphasizes transparency and reproducibility.
The goal is to create a verifiable prototype that supports early-stage decisions after typhoon events.

## 7. Current Status

- Day 1: Project structure created
- Day 2: Visualization refactor, schema validation, safer temp file handling, logging, and tests added
- Day 3: UI guidance, prototype disclaimer, and documentation aligned to decision-support use case

## 8. How to Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the Streamlit app (WSL-friendly). The development environment may automatically open a terminal on port 8502; if so use the 8502 URL below.
   - Default (8501):
     ```bash
     python -m streamlit run app.py
     ```
   - Explicit 8502 (if your environment or terminal uses port 8502):
     ```bash
     python -m streamlit run app.py --server.port 8502
     ```
   - Quick helper script (Linux/WSL):
     ```bash
     ./run_streamlit.sh
     ```
3. If the browser does not open automatically, paste one of these into your browser:
   - `http://localhost:8501` (or `http://127.0.0.1:8501`)
   - `http://localhost:8502` (or `http://127.0.0.1:8502`) if you used port 8502

## 9. Notes

- This tool is intended for prototype analysis and prioritization support.
- Always verify results through on-site inspection before taking operational action.
- Keep private farm data and API keys outside the repository.

## 10. Tests

Run the automated test suite with:
```bash
pytest -q
```

