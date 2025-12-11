# Earthquake Risk Analytics – Governance Note

## 1. Purpose & Scope

This governance note describes how our team will responsibly operate the earthquake-risk analytics system we built on Google Cloud. The system combines:

- **Historical batch data** from the USGS Kaggle earthquake database.
- **Near–real-time streaming data** from the USGS Earthquake Catalog API.
- **BigQuery ML models** that estimate short-term seismic risk at a regional grid level (e.g., 0.5°×0.5° cells, 30-day windows). :contentReference[oaicite:0]{index=0}  

The goal of the project is **risk prioritization**, not deterministic prediction of individual earthquakes. Our outputs are probabilistic risk scores and descriptive analytics intended to support planning, not to replace seismologists, emergency managers, or official alerts.

This document focuses on four areas:

1. Assumptions baked into the data and modeling.
2. Data ethics and responsible use.
3. Privacy, security, and access controls.
4. A failure playbook for pipeline and model issues.

---

## 2. Core Assumptions

Our pipeline and models rely on several simplifying assumptions that must be made explicit:

1. **Data quality & completeness**
   - We assume the Kaggle and USGS sources are *internally consistent* and that missing or mis-located events are rare relative to the full dataset.
   - We assume event metadata (location, depth, magnitude) are accurate enough for regional risk modeling, even though individual event parameters may be revised later.

2. **Stationarity of patterns**
   - The logistic-regression risk model assumes that relationships between long-run seismicity, recent activity, and near-term risk remain broadly stable over time. If tectonic behavior changes or cataloging practices shift, risk scores may become mis-calibrated.

3. **Spatial & temporal aggregation**
   - We aggregate to **grid cells and 30-day windows**. We assume this level of aggregation is appropriate for emergency-management and planning use cases and that users understand that risk is *regional* and *time-window based*, not a pinpoint forecast.

4. **Risk framing**
   - The label `high_risk` (e.g., “at least one M ≥ 5.5 event in the next 30 days”) is a **design choice**, not an official risk rating. Thresholds for classifying “high-risk” vs “not high-risk” are subjective and must be documented when the system is used to influence decisions.

5. **Infrastructure assumptions**
   - The GCP project is configured with adequate quotas for BigQuery, Pub/Sub, Dataflow, and Cloud Functions. We assume proper billing alerts and monitoring are in place to avoid surprise overages and silent failures.

---

## 3. Data Ethics & Responsible Use

Even though our data sources are public and non-personal, misuse of the outputs can still cause harm if they are over-interpreted or miscommunicated.

### 3.1 Intended Use

- **Intended users:** students, analysts, and planners using the dashboard to explore patterns and run “what-if” questions about seismic risk.
- **Intended decisions:** prioritizing regions for further expert study, resilience planning, or insurance scenario analysis.
- **Not intended for:** issuing evacuation orders, overriding official hazard maps, or providing real-time life-safety warnings.

All dashboards, README files, and presentations should clearly state that this is a **research / educational prototype**, not an operational early-warning system.

### 3.2 Biases and Limitations

- **Catalog coverage bias:** Some regions and time periods are better instrumented and reported than others. This can bias long-run event rates and cause the model to treat well-measured regions as “riskier” simply because more events were recorded there.
- **Rare events:** Large earthquakes (M ≥ 6–7) are rare, so the model learns mainly from more common moderate events. Risk scores for truly extreme events carry high uncertainty.
- **Model form:** Logistic regression and simple features may under-represent complex tectonic processes. We must avoid presenting model outputs as if they capture all scientific knowledge about earthquakes.

Where possible, the dashboard should surface **confidence / uncertainty cues** (e.g., event counts, sample sizes) and not just raw probabilities.

### 3.3 Communication & Guardrails

To reduce misinterpretation:

- Every chart and KPI should include *plain-language captions* explaining what is and is not being shown (e.g., “Probability of at least one M ≥ 5.5 event in the next 30 days, based on historical patterns and recent activity”).
- We will avoid deterministic phrasing (“an earthquake will occur”) and instead use **probabilistic language** (“higher relative risk compared to baseline”).
- When sharing results with non-technical audiences, at least one team member should highlight limitations and recommend consultation with domain experts before acting on the insights.

---

## 4. Privacy, Security & Access Control

Although our input data is non-personal and public, we still need to secure **infrastructure, credentials, and derived assets.**

### 4.1 Data Classification

- **Public / low-risk:** Raw USGS and Kaggle earthquake records; aggregated tables; model outputs; dashboard visualizations.
- **Sensitive:** GCP project configuration, service-account keys, Cloud Function environment variables, billing info, and any logs that might contain stack traces or error messages.

### 4.2 Access Control & IAM

- Use **principle of least privilege**:  
  - Data engineers and pipeline maintainers get “Editor” or more granular roles (BigQuery Data Editor, Dataflow Developer, etc.).  
  - Analysts and dashboard viewers get “BigQuery Data Viewer” and Looker Studio viewer roles only.
- Avoid sharing access via personal Gmail accounts; prefer team / course accounts managed by the instructor or org.

### 4.3 Secrets Management

- API keys (if any), service-account JSON, and connection strings must **never** be hard-coded in source code or notebooks.
- Use **Secret Manager** for any non-public configuration and reference those secrets from Cloud Functions / Dataflow, per best practices.
- Revoke or rotate keys immediately if they are accidentally committed to GitHub.

### 4.4 Encryption & Transport

- Rely on Google Cloud’s default **encryption at rest** for BigQuery tables and GCS objects.
- All access to GCP console, BigQuery, and the USGS API should occur over **HTTPS/TLS**.

---

## 5. Model Governance

### 5.1 Training, Evaluation & Monitoring

- Training queries and model creation SQL are stored in version-controlled repositories so we can recreate models.
- We use `ML.EVALUATE` and precision-recall curves to select and document a risk threshold that balances missed high-risk regions vs false alarms.
- If the model is retrained (e.g., with more recent data or new features), we will:
  - Log the training date, data span, and performance metrics.
  - Compare performance with previous versions and document changes.

### 5.2 Explainability

- For selected regions and dates, we use `ML.EXPLAIN_PREDICT` to identify which features (e.g., recent event counts vs long-run max magnitude) drive risk scores.
- These explanations are summarized in the dashboard and documentation so that stakeholders understand *why* certain regions are flagged as high risk.

### 5.3 Lifecycle & Decommissioning

- Models and dashboards should not be treated as permanent. If data sources, team ownership, or course context change, we will either:
  - Retrain and re-validate the models, or
  - Explicitly mark them as **archived** and not for current decision-making.

---

## 6. Operational Risks & Failure Playbook

Our architecture has several potential failure points, especially in the streaming path (Cloud Function → Pub/Sub → Dataflow → BigQuery) and in downstream analytics. :contentReference[oaicite:1]{index=1}  

### 6.1 External API Issues

**Failure modes**

- USGS API returns HTTP 429 (rate-limited) or 5xx errors.
- Network connectivity issues or schema changes in the API response.

**Mitigations / Playbook**

- Cloud Function uses exponential backoff and retries on transient errors.
- On repeated failures, we log the error, emit a structured error event to a separate Pub/Sub topic, and surface a “data freshness” warning in the dashboard.
- If the API schema changes, we temporarily pause the streaming pipeline and fall back to historical-only analytics until the parsing logic is updated.

### 6.2 Pub/Sub Backlog & Dataflow Latency

**Failure modes**

- Incoming event rate briefly exceeds Dataflow processing capacity, causing a growing Pub/Sub backlog.
- Dataflow job fails or stalls.

**Mitigations / Playbook**

- Monitor Pub/Sub **undelivered messages** and Dataflow **system latency** via Cloud Monitoring.
- Configure alerts (email/Slack) when backlog exceeds a threshold or when job latency violates the target SLO (e.g., P95 < 10 minutes).
- If backlog grows:
  - Temporarily scale Dataflow workers up (if quotas allow).
  - Simplify transformations or increase batch size to BigQuery to reduce per-message overhead.
- If the Dataflow job crashes:
  - Restart from the same Pub/Sub subscription (at-least-once semantics), acknowledging that some events may be reprocessed but not duplicated in BigQuery due to idempotent writes.

### 6.3 BigQuery / Dashboard Issues

**Failure modes**

- BigQuery quota limits or cost caps are hit.
- A schema change breaks dashboard queries.
- Dashboard becomes stale because streaming table is not updating.

**Mitigations / Playbook**

- Enable **cost controls** (e.g., custom cost cap alerts) and prefer partitioned / clustered tables to reduce query cost.
- Keep schema evolution under version control and update Looker Studio queries when tables change.
- Add a visible “Last updated” timestamp card on the dashboard; if timestamp is old, users know to treat metrics as historical only.

---

## 7. Limitations & Future Work

This system is an educational prototype, not a production-grade hazard platform. Key limitations include:

- Reliance on public catalogs with known uncertainties.
- Use of relatively simple models and features.
- Limited monitoring and alerting compared with real emergency-management systems.

Future improvements could include:

- Incorporating domain-specific seismic features (fault lines, tectonic settings).
- Exploring more advanced models (e.g., gradient-boosted trees) while preserving explainability.
- Hardening monitoring, alerting, and CI/CD for Cloud Functions and Dataflow pipelines.

By making our assumptions, risks, and safeguards explicit, this governance note helps ensure that the earthquake-risk analytics system is used **responsibly, transparently, and proportionately** to its capabilities.
