# Roadmap for agri-typhoon-risk-priority

## 1. Current Project Status

The current project is an **executable prototype demo**.

The core workflow is already implemented:

- CSV upload
- Schema validation
- Feature derivation
- Risk scoring
- Inspection priority ranking
- Chart visualization
- Result download
- Basic testing structure

This project should not be interpreted as a simple weather dashboard. The dashboard is only the interface for demonstrating the risk scoring and prioritization workflow.

Current completion estimate:

- **Prototype/demo readiness:** approximately 55–65%
- **Professor-facing demo readiness:** 1–2 additional days of polishing
- **Full field-response system readiness:** at least 2 weeks, preferably 4 weeks or more

The current version is suitable as a research-oriented prototype, but it is not yet a validated operational system.

---

## 2. Final Goal

The final goal is to build a **post-typhoon agricultural damage prioritization and field response support system**.

The system should help users identify which farms, crops, or regions should be checked first after typhoon-related agricultural damage events.

Long-term system goals include:

- Ingest typhoon hazard, farm, crop, and regional vulnerability data
- Assess farm-level vulnerability and exposure
- Estimate relative agricultural damage risk
- Prioritize field inspection targets
- Support post-disaster response workflows
- Provide decision-support outputs for researchers, field managers, and agricultural disaster response teams

The project should remain centered on **agricultural disaster management**, **crop-climate risk assessment**, and **field inspection prioritization**.

---

## 3. Research Alignment

This project is aligned with the following research directions:

- Rural Climate Systems Engineering
- Agricultural Disaster Management Engineering
- Agricultural Systems Modeling and Sustainability Assessments
- Climate Change and Agrometeorological Disasters
- Agricultural Complex Systems Engineering
- Crop system analysis and modeling
- Crop-climate risk assessment
- Post-disaster agricultural field response

The project can be positioned as a prototype that connects:

```text
Typhoon Hazard
→ Crop and Farm Vulnerability
→ Exposure Factors
→ Risk Score
→ Field Inspection Priority
→ Post-Disaster Response Support
```

This direction is more important than the dashboard itself.

The dashboard is only a demonstration layer. The core research contribution should be the design of the risk-scoring logic, the variable structure, and the decision-support workflow.

---

## 4. Short-Term Plan: Day3–Day5

## Day3: Documentation and Direction Lock

Main goal: clarify the project identity.

Tasks:

- Update `README.md`
- Confirm `ROADMAP.md`
- Confirm or create `DEV_NOTES.md`
- Clarify that this is not a simple weather dashboard
- Define the project as a post-typhoon agricultural damage prioritization system
- Add current limitations and future development direction
- Confirm data policy for sample/synthetic data only
- Check that the app still runs after documentation updates

Expected output:

- Clear README
- Research-oriented roadmap
- Development notes for future continuation
- Stable demo direction

---

## Day4: Variable Design and Validation Refinement

Main goal: make the risk logic more explainable.

Tasks:

- Review required input columns
- Review optional input columns
- Clarify each variable used in risk scoring
- Separate variables into:
  - Typhoon hazard factors
  - Crop vulnerability factors
  - Farm/facility vulnerability factors
  - Exposure factors
  - Response priority factors
- Improve schema validation messages
- Check sample CSV consistency
- Add variable explanation table if needed

Expected output:

- More explainable scoring logic
- Cleaner input data requirements
- Better preparation for professor-facing discussion

---

## Day5: Professor-Facing Demo Preparation

Main goal: prepare a clean explanation flow.

Tasks:

- Confirm end-to-end demo flow using sample CSV
- Prepare a short demo scenario
- Explain what the current model does and does not do
- Prepare a list of current limitations
- Prepare future research questions
- Run tests
- Confirm local Streamlit execution
- Prepare commit before sharing or presenting

Expected output:

- Professor-facing demo checklist
- Stable local execution
- Clean explanation of the system as a research prototype

---

## 5. Expansion Roadmap: Day6+ / Four-Week Plan

## Week 1: Risk Variable Design and Model Logic

Focus: improve the scientific structure of the risk score.

Tasks:

- Define core typhoon hazard variables:
  - rainfall intensity
  - accumulated rainfall
  - wind speed
  - typhoon exposure level
- Define crop vulnerability variables:
  - crop type
  - growth stage
  - sensitivity to wind/rainfall/waterlogging
- Define farm and field vulnerability variables:
  - lowland condition
  - drainage weakness
  - facility type
  - past damage history
- Review whether current weights are reasonable
- Document the risk score formula
- Separate prototype assumptions from validated knowledge

Expected output:

- Variable design table
- Risk score explanation
- Better model transparency

---

## Week 2: Crop-Climate Risk Extension

Focus: connect the prototype to crop-climate risk assessment.

Tasks:

- Add crop-specific vulnerability categories
- Add growth-stage-sensitive risk logic
- Consider typhoon-related agricultural damage mechanisms:
  - lodging
  - flooding
  - waterlogging
  - facility damage
  - fruit drop or physical damage
- Improve interpretation of risk score outputs
- Add example scenarios for different crops or farm types

Expected output:

- More crop-aware risk scoring logic
- Better connection to crop system analysis and agricultural disaster management

---

## Week 3: Field Response and Inspection Priority Workflow

Focus: move from risk score to response support.

Tasks:

- Improve inspection priority categories
- Add response labels such as:
  - urgent inspection
  - monitor
  - low priority
  - data insufficient
- Add simple field response status structure
- Improve map/table filtering for priority review
- Add export format for field inspection planning
- Prepare a simulated post-typhoon response scenario

Expected output:

- Stronger field response logic
- More realistic post-disaster inspection workflow

---

## Week 4: Validation, Reporting, and Research Packaging

Focus: make the prototype discussable as a research project.

Tasks:

- Add validation scenario using sample or simulated damage cases
- Compare high-risk predictions with assumed damage outcomes
- Add simple performance or plausibility checks
- Prepare report generation or summary export
- Organize documentation for lab discussion
- Prepare future research questions
- Prepare possible thesis/project framing

Expected output:

- Research-style prototype package
- Clear explanation of current assumptions and limitations
- Better readiness for professor/lab discussion

---

## 6. Features Not Prioritized Now

The following features are intentionally not prioritized at the current stage:

- Real-time weather API integration
- Full insurance claim workflow
- Multi-user authentication
- Role-based access control
- Full GIS or satellite image processing
- Production-grade cloud deployment
- Mobile app development
- Complex machine learning model training
- Automated official disaster reporting

These features may be considered later, but the current priority is to stabilize the **risk logic**, **variable design**, **prototype workflow**, and **research direction**.

---

## 7. Long-Term Additions

Potential long-term extensions include:

- Historical typhoon and agricultural damage dataset integration
- Weather API linkage
- Crop growth-stage-sensitive risk scoring
- Farm-level vulnerability database
- Field inspection workflow management
- Damage report and photo upload
- Automated post-typhoon response report generation
- Model validation using real or historical damage records
- Linkage with agricultural disaster management platforms
- Decision-support tools for local governments, agricultural agencies, or insurance-related field assessment

---

## 8. Development Principle

Future development should follow this order:

```text
Research direction
→ Variable design
→ Risk scoring logic
→ Schema validation
→ Prototype interface
→ Demo scenario
→ Testing
→ Deployment
```

Avoid large feature additions before the model logic and research framing are clear.

The core question should always remain:

```text
After a typhoon, which farms, crops, or regions should be checked first, and why?
```
