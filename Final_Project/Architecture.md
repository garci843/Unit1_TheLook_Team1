# Architecture

This document describes the end-to-end architecture for the Final Project pipeline, including:

- **Batch path**: Kaggle → Colab → GCS → BigQuery  
- **Streaming path**: Public API → Cloud Function → Pub/Sub → Dataflow → BigQuery  
- **Analytics & ML**: BQML models trained on batch + streaming features  
- **Consumption**: Looker Studio dashboards on top of BigQuery  
- **Reproducibility**: How to spin the pipeline up and down with `gcloud` and notebooks

> Replace placeholders like `PROJECT_ID`, `REGION`, `BQ_DATASET`, etc. with your values.

---

## 1. High-Level Diagram

### 1.1 Overall Architecture

```text
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
