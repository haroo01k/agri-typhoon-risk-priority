# Typhoon Agricultural Damage Priority Engine

## 1. Project Overview

This project aims to develop a typhoon agricultural damage risk scoring model that supports post-typhoon field inspection prioritization.

This project is not intended to be a simple weather dashboard. The dashboard is only a visualization interface. The core objective is to support decision-making for post-typhoon agricultural damage inspection and field response.

The system combines regional typhoon hazard factors such as wind and rainfall with farm-level vulnerability factors such as crop type, facility type, lowland condition, drainage weakness, and past damage history.

The long-term direction is to develop a research-oriented prototype for agricultural disaster management, crop-climate risk assessment, and field inspection prioritization.

## 2. Korean Title

태풍 농업피해 위험도 산정 및 우선확인 지원 시스템

## 3. Research Positioning

This project is positioned as a research-oriented prototype for agricultural disaster response and crop-climate risk assessment.

It is aligned with the following research directions:

- Rural Climate Systems Engineering
- Agricultural Disaster Management Engineering
- Agricultural Systems Modeling and Sustainability Assessments
- Climate Change and Agrometeorological Disasters
- Agricultural Complex Systems Engineering
- Crop system analysis and modeling
- Crop-climate risk assessment
- Post-disaster field response support

The project should be understood as a decision-support system for prioritizing agricultural damage inspection after typhoon events, rather than as a general-purpose weather or visualization dashboard.

## 4. Problem Statement

태풍 발생 이후 농가 피해 확인은 전화, 현장 방문, 신고 접수 등 수작업 중심으로 이루어지는 경우가 많다.

이 방식은 피해 지역이 넓거나 농가 수가 많을 때 대응 지연과 업무 비효율을 초래할 수 있다.

따라서 태풍의 강풍·강수 특성과 농가의 작물·시설·지역 취약성을 결합하여 피해 가능성이 높은 농가를 우선적으로 확인할 수 있는 위험도 산정 모델이 필요하다.

본 프로젝트는 이러한 문제를 해결하기 위해 태풍 이후 농업 피해 가능성이 높은 농가, 작물, 지역을 우선적으로 확인할 수 있도록 지원하는 의사결정 지원형 프로토타입을 구축하는 것을 목표로 한다.

## 5. Core Model Structure

Regional Typhoon Hazard  
→ Farm Vulnerability  
→ Exposure Factors  
→ Typhoon Damage Risk Score  
→ Field Inspection Priority

## 6. Main Components

- Regional wind risk scoring
- Regional rainfall risk scoring
- Farm crop vulnerability scoring
- Facility vulnerability scoring
- Exposure scoring
- Priority list generation
- Streamlit-based prototype interface for inspection priority visualization

## 7. Data Policy

This repository only includes sample or synthetic data.

Do not upload:

- Personal farm information
- Real farm location data without permission
- API keys
- Private research data
- Unpublished materials

Private data should be stored locally in:

```text
data/private/
```

API keys should be stored in:

```text
.env
```

## 8. Current Status

- Day 1: Project structure created
- Day 2: Visualization refactor, schema validation, safer temp file handling, logging, and tests added
- Local Streamlit app runs with sample data and supports CSV upload

Current project stage:

- Prototype/demo readiness: approximately 55–65%
- Full field-response system readiness: approximately 30–35%

The current version should be treated as an executable prototype demo, not as a validated operational system.

## 9. Current Limitations

The current version is an executable prototype demo, not a validated field operation system.

Current limitations include:

- The model currently uses sample or synthetic data.
- The risk scoring logic is still rule-based and requires further validation.
- Real typhoon, crop, and field damage datasets are not yet integrated.
- Crop growth stage, cultivar sensitivity, and detailed phenological risk are not yet reflected.
- The system does not yet include real-time weather API integration.
- The current interface supports prioritization analysis, but not full field operation management.

All outputs should be interpreted as prototype-level prioritization support and must be verified through expert review and field inspection.

## 10. How to Run

1. Create and activate a Python virtual environment or conda environment.

For WSL / macOS virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

For Windows PowerShell virtual environment:

```powershell
.venv\Scripts\activate
```

If using the current conda environment:

```bash
conda activate agri-B
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the Streamlit app:

```bash
python -m streamlit run app.py
```

4. Upload a farm-level CSV or use the built-in sample data at:

```text
data/sample/example_farms.csv
```

## 11. Deployment

This repository is designed as a source-built Streamlit prototype.

- Install dependencies using `requirements.txt`.
- Run the app locally with `python -m streamlit run app.py`.
- For WSL or environments where automatic browser launch fails, manually open the local URL shown in the terminal:
  - `http://localhost:8501`
  - `http://localhost:8502`
- Keep private farm data and API keys outside the repository.

## 12. Future Development

Future development will focus on expanding the prototype from a dashboard-based demo into a more complete agricultural disaster response support system.

Planned directions include:

- Refinement of typhoon hazard indicators
- Crop-specific vulnerability scoring
- Growth-stage-sensitive damage risk assessment
- Integration of rainfall, wind, drainage, and lowland exposure factors
- Validation using historical agricultural damage cases
- Improvement of field inspection priority logic
- Report generation for post-typhoon response planning
- Possible linkage with weather APIs, agricultural disaster records, or field survey data

The long-term goal is to support data-driven agricultural disaster management by helping decision-makers identify which farms, crops, or regions should be checked first after typhoon events.

## 13. Notes

- This tool is intended for prototype analysis and prioritization support.
- Always verify results through on-site inspection before taking operational action.
- Keep private farm data and API keys outside the repository.
- The dashboard is not the core research contribution. It is the interface for demonstrating the risk scoring and prioritization workflow.

## 14. Tests

Run the automated test suite with:

```bash
pytest -q
```
