# Deployment Guide

This document explains how to run the `agri-typhoon-risk-priority` prototype and what to do if you want to prepare it for a simple deployment.

## Local setup

1. Create and activate a Python virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # WSL / macOS
   # .venv\Scripts\activate  # Windows PowerShell
   ```
2. Install project dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Streamlit app:
   ```bash
   python -m streamlit run app.py
   ```

## WSL / port 8502

If your WSL environment automatically opens a terminal on port 8502 or if port 8501 is unavailable, use:

```bash
python -m streamlit run app.py --server.port 8502
```

Then open one of these in your browser:

- `http://localhost:8501`
- `http://localhost:8502`

## What this repo contains

- `app.py`: Streamlit UI and workflow orchestration
- `src/`: data loading, preprocessing, risk model, and visualization helpers
- `data/sample/example_farms.csv`: sample farm-level data for testing
- `requirements.txt`: Python dependencies for the prototype
- `run_streamlit.sh`: helper script for Linux/WSL

## Deployment notes

This prototype is intended for local testing and classroom/demo use.

### If you want to deploy it further:

- Use a dedicated Python environment on the target server
- Ensure `requirements.txt` is installed
- Do not store private farm data in the repository
- Prefer containerization or VM deployment for operational stability

### Optional containerization

If you later want a Docker-based deployment, the repository can be containerized by adding a simple `Dockerfile` and running Streamlit inside the container.
