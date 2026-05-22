# Roadmap for agri-typhoon-risk-priority

## Current Project Status

- Current state: **executable prototype demo**.
- The core workflow is implemented: CSV upload, schema validation, feature derivation, risk scoring, ranking, chart visualization, and download.
- This is a functional prototype designed for demonstration rather than a production system.
- Completion estimate from current state:
  - **1–2 days** to polish for a professor-level demo.
  - **2 weeks minimum**, preferably **4 weeks**, to evolve into a field-response system.

## Final Goal

Build a full **post-typhoon agricultural damage prioritization and response support system** that can:

- ingest multi-source typhoon and farm data,
- assess farm vulnerability and exposure accurately,
- prioritize field inspection targets,
- support on-site response workflows,
- provide operational reports for decision makers.

## Short-Term Plan (Day3–Day5)

### Day3

- Polish user-facing UX and documentation.
- Finalize prototype disclaimer and operating notes.
- Ensure schema validation and error messages are clear.
- Confirm demo flow works end-to-end with sample CSV.

### Day4

- Strengthen testing coverage for edge cases and larger datasets.
- Clean up documentation: `README.md`, `DEV_NOTES.md`, `docs/deployment.md`.
- Add sample usage scenarios for a demo.

### Day5

- Validate the prototype as a demo package.
- Confirm run instructions for Windows/WSL.
- Fix any remaining usability issues in `app.py` and documentation.
- Prepare a short demo script or checklist for presentation.

## Expansion Roadmap (Day6+ / 4 Weeks)

### Week 1

- Add multi-source data ingestion support.
- Improve model scoring logic with better hazard/exposure/vulnerability formulas.
- Add more robust input validation and data quality checks.

### Week 2

- Add a basic reporting layer or export summary report.
- Add user workflow support for inspection task assignment.
- Improve map-based filtering and prioritization visuals.

### Week 3

- Integrate more operational data (damage reports, weather feeds, insurance metadata).
- Add role-based access or simple user session handling.
- Start a deployment-ready configuration for a VM or container.

### Week 4

- Harden the system for field use: resilience, logging, environment configuration.
- Add deployment documentation, optional Docker support, and real-world test scenarios.
- Validate the project with a pilot dataset or simulated field inspection case.

## Features Not Doing Now

- Full damage labeling or insurance claim workflows.
- Real-time streaming weather data ingestion.
- Multi-user authentication and access control.
- Full GIS / satellite imagery processing.
- Production-grade logging, monitoring, or alerting.

## Long-Term Additions

- Validated damage risk model using historical typhoon data.
- Workflow management for field inspections, task assignment, and status tracking.
- Automated report generation for regional disaster response.
- Cloud deployment or containerized field operations stack.
- Integration with external disaster management platforms.
