# Sample Data Mapping

이 문서는 `data/sample/example_farms.csv`의 컬럼을 `docs/variable_design.md`의 변수에 매핑하는 가이드입니다.

- `farm_id` -> 고유 농가 식별자
- `latitude`, `longitude` -> 지리 좌표 (위치 기반 노출 지표 계산에 사용)
- `farm_area_ha` -> `farm_area_ha` (Exposure)
- `protected_area_m2` -> `protected_area_m2` (Exposure)
- `crop_type` -> `crop_type` (Vulnerability)
- `crop_area_share` -> `crop_area_share` (Exposure/가중치)
- `max_wind_ms`, `mean_wind_ms` -> 풍속 지표 (Hazard)
- `cum_precip_24h`, `cum_precip_72h`, `max_hourly_precip` -> 강수 지표 (Hazard)
- `central_pressure`, `typhoon_category` -> 태풍 강도 (Hazard)
- `distance_to_coast_km`, `is_lowland` -> 위치 노출 (Exposure)
- `elevation_m`, `slope_deg`, `soil_type` -> 지형/토양 (침수 위험 파생 변수)
- `past_damage_count`, `past_loss_estimate` -> 이력 기반 취약성 보정
- `insurance_covered` -> 관리 변수 (보상/대응 여력 반영)
- `facility_type`, `facility_structure_score`, `drainage_exists` -> 시설 취약성
- `obs_source`, `timestamp`, `imputed_flag` -> 메타/데이터 품질

데이터 형식/타입 권장:
- 수치 필드: float 또는 int
- 범주형: 소문자 문자열
- 불리언: True/False
- 날짜/시간: ISO-8601 문자열

다음 단계:
1. `src/data_loader.py`에 이 스키마를 검증하는 로직 추가
2. `src/preprocessing.py`에서 각 컬럼을 읽어 `docs/variable_design.md`의 변수 이름으로 정렬하고 타입·결측치 처리를 수행
