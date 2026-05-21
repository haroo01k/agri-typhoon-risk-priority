# Ensemble & DSSAT Integration — Extension Notes

이 문서는 향후 기후 앙상블(예: NetCDF/GRIB 또는 API 기반)과 DSSAT 모델 출력을 통합할 때 고려할 필드, 모듈 스켈레톤, 입력/출력 포맷을 정리합니다.

## 1. 확장 필드(데이터 스키마)
- `scenario_id`: 앙상블 시나리오 식별자 (e.g., RCP/SSP or run id)
- `member_id`: 앙상블 멤버 식별자
- `ensemble_mean_max_wind_ms`, `ensemble_std_max_wind_ms`
- `ensemble_mean_cum_precip_24h`, `ensemble_std_cum_precip_24h`
- `uncertainty_flags`: 불확실성 수준(예: low/med/high)
- DSSAT outputs: `phenology_stage`, `lai`, `root_depth`, `water_stress_index`, `yield_estimate`

## 2. 모듈 스켈레톤 제안
- `src/integrations/climate_ensemble.py`
  - `load_ensemble_netcdf(path)` → xarray.Dataset 처리
  - `extract_site_series(ds, lat, lon, radius=5km)` → pandas.DataFrame per site
  - `compute_ensemble_stats(df_list)` → mean/std per variable

- `src/integrations/dssat_connector.py`
  - `run_dssat_for_site(config)` → 실행 래퍼 (주의: DSSAT는 외부 바이너리)
  - `parse_dssat_output(output_dir)` → pandas.DataFrame of key outputs

## 3. 불확실성 전파
- 앙상블 표준편차를 최종 위험도에서 신뢰구간으로 전파
- 예: 최종 리스크의 95% CI = FinalRisk ± 1.96 * propagated_std

## 4. 저장 포맷 및 메타
- 시공간 대용량 데이터는 parquet/feather + 메타 JSON 추천
- 앙상블 원본은 가능하면 NetCDF로 보관; 추출물은 site-level CSV/parquet로 저장

## 5. 연산 비용 및 배치 전략
- 앙상블·DSSAT 연동은 배치(슬라이스별) 처리 권장
- 병렬 실행: 멤버 단위로 분산 처리 (Dask 또는 배치 스크립트)

## 6. 문서화
- `docs/variable_design.md`에 앙상블·DSSAT 필드 추가
- 통합 테스트: 소규모 앙상블 + 가짜 DSSAT 출력으로 파이프라인 검증


*** End of file
