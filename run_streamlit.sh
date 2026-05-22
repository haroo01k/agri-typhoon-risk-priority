#!/usr/bin/env bash
# Helper script to run the Streamlit app on port 8502 (WSL-friendly)
set -euo pipefail
cd "$(dirname "$0")"
python -m streamlit run app.py --server.port 8502
