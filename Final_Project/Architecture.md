# Architecture

This document describes the end-to-end architecture for the Final Project pipeline, including:

- **Batch path**: Kaggle → Colab → GCS → BigQuery  
- **Streaming path**: Public API → Cloud Function → Pub/Sub → Dataflow → BigQuery  
- **Analytics & ML**: BQML models trained on batch + streaming features  
- **Consumption**: Looker Studio dashboards on top of BigQuery  

> **Reproducibility**: Replace placeholders like `PROJECT_ID`, `REGION`, `BQ_DATASET`, etc. with your values.

---

## 1. High-Level Diagram

### 1.1 Overall Architecture

```
                        +------------------+
                        |   Kaggle Batch   |
                        |     Dataset      |
                        +---------+--------+
                                  |
                           (Colab / Notebook)
                                  |
                                  v
                        +----------------------+
                        |   GCS Raw Bucket     |
                        |  gs://BUCKET_RAW     |
                        +----------+-----------+
                                   |
                           (bq load / SQL)
                                   |
                                   v
                         +----------------------+
                         |   BigQuery (Batch)   |
                         |  Curated Tables      |
                         +----------+-----------+
                                    \
                                     \
                                      v
                                 +----------+
                                 |  BQML    |
                                 | Models   |
                                 +----------+
                                      |
                                      v
                             +-----------------+
                             |  Predictions &  |
                             |  Feature Tables |
                             +-----------------+
                                      |
                                      v
                              +----------------+
                              | Looker Studio  |
                              | Dashboards     |
                              +----------------+
```
### 1.2 Streaming Path
```
                         Public API (earthquake)
                                   |
                                   v
                       +------------------------+
                       | Cloud Function         |
                       | - Fetch API            |
                       | - Normalize JSON       |
                       | - Publish to Pub/Sub   |
                       +-----------+------------+
                                   |
                                   v
                          +------------------+
                          |  Pub/Sub Topic   |
                          | stream-events    |
                          +--------+---------+
                                   |
                                   v
                          +---------------------+
                          |  Dataflow Template  |
                          |  (Pub/Sub → BQ)     |
                          +----------+----------+
                                     |
                                     v
                       +---------------------------+
                       | BigQuery Streaming Fact   |
                       |  BQ_DATASET.stream_events |
                       +---------------------------+
```
### 1.3 Feature Engineering & BQML
```
    BigQuery Batch Tables               BigQuery Streaming Fact
 (entities, historical facts)          (near real-time metrics)
               |                                   |
               +---------------+-------------------+
                               |
                               |
                               v
                    +-----------------------+
                    |      BQML Models      |
                    +-----------+-----------+
                                |
         +----------------------+------------------+
         |                                         |
         v                                         v
  ML.EVALUATE (metrics)                    ML.EXPLAIN_PREDICT
                                                (feature attributions)
```
### 1.4 Dashboard View
```
                +----------------------------+
                |   BigQuery (Batch +        |
                |   Streaming + Predictions) |
                +----------------------------+
                               |
                               |
                               v
                 +---------------------------+
                 | Looker Studio Dashboard   |
                 | - 3 KPIs                  |
                 | - Time-series from stream |
                 +---------------------------+

```

## 2. Components & Responsibilities

### 2.1 GCS → BigQuery (Batch Path)

#### Colab / Notebook
- Downloads Kaggle dataset.
- Performs data quality checks such as null detection, range validation, and duplicate removal.
- Writes raw batch files to GCS under a structured folder path.

#### GCS Raw Bucket
- Serves as the landing zone for raw, unmodified batch data.
- Supports reproducibility and versioning for batch ingest workflows.

#### BigQuery Batch Tables
- Curated tables populated from GCS.
- Includes dimension and fact tables (e.g., entities, historical records).
- Uses partitioning and documented schema definitions.
- Forms the static feature foundation for ML and analytics.

---

### 2.2 Cloud Function → Pub/Sub → Dataflow → BigQuery (Streaming Path)

#### Cloud Function
- Fetches data from a public API
- Normalizes API responses into consistent JSON with entity identifiers, metric values, and timestamps.
- Publishes streaming events into a Pub/Sub topic.
- **Implements retry and logging for 429 or 5xx API failures.**

#### Pub/Sub Topic
- Buffers incoming streaming messages.
- Decouples Cloud Function from downstream processing.
- Supports reliable, scalable message-based ingestion.

#### Dataflow (Pub/Sub → BigQuery Template)
- Uses Google’s managed streaming template.
- Subscribes to the Pub/Sub topic.
- Processes and writes streaming rows to a BigQuery fact table.

#### BigQuery Streaming Fact Table
- Stores near real-time data produced by Dataflow.
- Typically partitioned by ingest or event timestamp.
- Serves as input for time-series dashboards and ML feature engineering.

---

### 2.3 Feature Engineering & BQML

#### BQML Model Training
- Trains tree and linear regression models using streaming and batch data
- Supports iterative model development entirely in SQL.

#### Model Evaluation and Explainability
- ML.EVALUATE provides numerical metrics such as precision, recall, RMSE, or accuracy.
- ML.EXPLAIN_PREDICT provides feature importance and attribution values.
- Classification models include a threshold selection discussion based on evaluation metrics.

---

### 2.4 Looker Studio Dashboards

#### Data Sources
- Connects directly to BigQuery tables including batch curated tables, streaming fact tables, and model output tables.

#### Dashboard Requirements
- Displays three KPIs.
- Includes at least one near real-time time-series visualization coming from the streaming table.

### Purpose
- Demonstrates full pipeline functionality during live demo.
- Validates end-to-end flow from Cloud Function → Pub/Sub → Dataflow → BigQuery → Dashboard.
