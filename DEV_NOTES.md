# Developer Notes for agri-typhoon-risk-priority

## Current Execution Method

- The app is a Streamlit prototype located in `app.py`.
- Run the app from the project root using:
  ```bash
  python -m streamlit run app.py
  ```
- Dependencies are listed in `requirements.txt`.
- For local tests, use:
  ```bash
  PYTHONPATH=. pytest -q
  ```

## Streamlit Execution Notes

- The project currently supports a single farm-level CSV upload workflow.
- `src/data_loader.py` validates required fields and coerces common types.
- `src/preprocessing.py` derives hazard and vulnerability features.
- `src/risk_model.py` computes final risk scores combining hazard, vulnerability, and exposure.
- `src/visualization.py` contains reusable plotting and map helpers.

## WSL and Browser Auto-Launch

- In WSL, Streamlit may print a message like:
  ```text
  gio: http://localhost:8501: Operation not supported
  ```
- That message means Streamlit tried to open the browser automatically and failed.
- The app can still run normally; open the local URL manually instead.
- Recommended manual URLs:
  - `http://localhost:8501`
  - `http://localhost:8502`

## Current Project Design Direction

- This is not a final damage assessment model; it is a **prioritization support prototype**.
- The focus is on a simple, explainable scoring workflow:
  1. validate input schema,
  2. derive hazard / vulnerability / exposure features,
  3. compute a combined risk score,
  4. rank farms and show priorities.
- The project should remain modular: data loading, preprocessing, modeling, and visualization are separated into `src/`.
- Useful prototypes should be stable, explainable, and easy to run for a demo.

## What to Read First in a New Chat

When continuing this project, start with:

1. `README.md` for project purpose and how to run it.
2. `ROADMAP.md` for current status, short-term and 4-week plan.
3. `DEV_NOTES.md` for execution details and WSL-specific notes.
4. `src/` modules for the current implementation structure.
5. `tests/` for the existing validation coverage.

## Important Remaining Priorities

- Keep the prototype focused on the prioritization support workflow.
- Avoid adding full damage confirmation or insurance settlement logic too early.
- Make sure the app remains runnable in WSL and easy to demonstrate.
- Document every critical assumption and the current limitation clearly.
