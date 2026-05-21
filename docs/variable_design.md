# Variable Design — Day 2

이 문서는 태풍 농업피해 위험도 산정 모델의 변수 목록, 정의, 단위, 점수화 및 전처리 규칙을 정리합니다. 각 변수를 `src/`의 전처리 및 모델 코드로 일치시키는 것이 목표입니다.

## 1. 설계 원칙
- 모든 하위지수는 가능하면 0–1 또는 0–100 범위로 정규화
- 결측치는 명시적 대체 규칙(인근 평균/지역 중앙값/플래그)을 적용
- 파생변수는 재현 가능하고 설명 가능해야 함

## 2. 변수 카테고리 요약
- Hazard (지역적 위험): 풍속, 강수, 태풍 등급, 중심기압 등
- Exposure (노출): 농가 면적, 시설 유형, 해안/저지대 근접성
- Vulnerability (취약성): 작물별 민감도, 생육단계, 시설 내구성
- Historical / Management: 과거 피해 이력, 배수 개선 여부
- Meta: 관측 소스, 결측/추정 플래그

## 3. 상세 변수 목록 (권장 필드 형식)

### Hazard (지역 위험)
- `max_wind_ms`: 최대순간풍속 (m/s). 등급화: 0–15, 15–25, 25–35, >35
- `mean_wind_ms`: 평균풍속 (m/s)
- `cum_precip_24h`: 24시간 누적강수량 (mm)
- `cum_precip_72h`: 72시간 누적강수량 (mm)
- `max_hourly_precip`: 시간당 최대강수량 (mm/hr)
- `central_pressure`: 중심최저기압 (hPa)
- `typhoon_category`: 태풍 등급 (categorical)
- 파생: `hazard_wind_score` (0–1), `hazard_precip_score` (0–1), `hazard_combined` (0–1)

스케일링: 각 풍속/강수 지표에 대해 도메인 기준 또는 퍼센타일 기반 컷오프를 사용해 0–1로 정규화.

### Exposure (노출)
- `farm_area_ha`: 농가 재배면적 (ha)
- `protected_area_m2`: 온실/시설 면적 (m²)
- `distance_to_coast_km`: 해안선으로부터 거리 (km)
- `is_lowland`: 저지대 여부 (boolean)
- `crop_area_share`: 주요 작물별 면적 비율 (dict or multiple cols)

스코어링: 면적/시설 비중이 클수록 노출 점수 상승. 거리/저지대는 침수·풍해 노출을 증가시킴.

### Vulnerability — Crop
- `crop_type`: 작물 코드/종류
- `crop_sensitivity`: 작물별 취약성 지수 (0–1)
- `growth_stage`: 생육단계 (seedling, vegetative, flowering, harvest)
- `stage_sensitivity`: 생육단계 가중치 (0–1)

파생: `crop_vulnerability = crop_sensitivity * stage_sensitivity`.

### Vulnerability — Facility
- `facility_type`: 시설 유형 (open_field, plastic_house, glass_house)
- `facility_structure_score`: 구조 내구성 지수 (0–1)
- `drainage_exists`: 배수시설 유무 (boolean)

시설 점수는 구조 내구성 저하면 풍해·침수 취약성 증가.

### Terrain & Soil
- `elevation_m`: 고도 (m)
- `slope_deg`: 경사 (deg)
- `soil_type`: 토양 유형 (sand, loam, clay)

침수 위험 파생: `f(cum_precip, elevation, soil_type)` → `inundation_risk` (0–1).

### Historical / Management
- `past_damage_count`: 최근 N년 피해 발생 횟수
- `past_loss_estimate`: 과거 손실(금액) 또는 피해 등급
- `insurance_covered`: 보험 가입 여부 (boolean)

이력은 취약성 보정에 사용 (예: 과거 피해가 많으면 취약성 가중치 증가).

### Meta / Data Quality
- `obs_source`: 관측/모델/추정
- `timestamp`: 관측 시각
- `imputed_flag`: 결측 대체 여부


## 4. 점수화·가중치 초안
- 각 구성요소: `Hazard_score`, `Vulnerability_score`, `Exposure_score` (각각 0–1)
- 초기 가중치(초안): FinalRisk = 0.5*Hazard + 0.3*Vulnerability + 0.2*Exposure
- 가중치는 검증데이터와 전문가 피드백으로 조정

## 5. 결측치·이상치 처리 규칙
- 필수 변수(`max_wind_ms`, `cum_precip_24h`, `farm_area_ha`) 결측 시 지역 중앙값 또는 인근 관측소 평균으로 대체하고 `imputed_flag` 설정
- 이상치는 도메인별 상한/하한으로 클리핑(예: 풍속 <0 → 0, 풍속>80 → 80)

## 6. 구현 포인터
- 문서화된 변수명으로 `src/data_loader.py`에서 컬럼 정렬 및 타입 검사 구현
- `src/preprocessing.py`에 결측치 대체, 범주형 인코딩, 파생변수 계산 함수 추가
- `src/risk_model.py`에는 하위지수를 계산하는 함수(`compute_hazard_score`, `compute_vulnerability_score`, `compute_exposure_score`, `compute_final_risk`) 추가
- `src/visualization.py`는 `FinalRisk` 기반 정렬·필터·지도 시각화 함수 제공

## 7. 검증·튜닝 권장 절차
1. 샘플 데이터로 단위 테스트 및 시나리오 테스트 작성
2. 도메인 전문가와 컷오프/가중치 검토
3. 민감도 분석(가중치 변화에 따른 우선순위 변화 관찰)

---
작성자: 개발 초안
