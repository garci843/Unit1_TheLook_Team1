# Contribution:

## Tasks Completed
- **Configured full cloud workflow** by setting up Google Cloud authentication, enabling required APIs, and integrating Kaggle credentials for automated dataset access.
- **Imported and cleaned the earthquake dataset**, including handling missing values, parsing timestamps, normalizing schemas, and selecting relevant predictive features.
- **Uploaded cleaned data to BigQuery**, creating the `earthquake.earthquake_bqml` table with validated schemas for downstream ML tasks.
- **Engineered advanced ML features**:
  - Cyclical encodings to capture periodic behavior (`hour_sin`, `hour_cos`, `day_sin`, `day_cos`).
  - Polynomial and interaction terms enhancing linear model expressiveness (`depth_x_magnitude`, squared terms).
  - Added geospatial and temporal augmentations where applicable.
- **Created an enhanced BigQuery table** with all engineered features, ensuring compatibility for BQML training.
- **Trained a BigQuery ML Linear Regression model** using the enriched feature set; monitored job execution and validated training results.
- **Evaluated model performance** using BigQuery ML metrics (RMSE, MAE, R²), comparing enhanced model accuracy to baseline and interpreting error trends.
- **Established a reproducible end-to-end ML pipeline** covering ingestion → preprocessing → cloud storage → feature engineering → BQML training → evaluation.


## Lessons Learned
Through this project I learned how to complete an end-to-end pipeline for data that comes in batch or streaming formats and how to use that data to generate useful and important analyses. Furthermore, through the work my group member did, I got a better understanding of how to upload streaming data from an API you can find on the internet, and how to turn that raw data into useful insights. Another thing I learned was how to best use my previous labs and gemini to improve my efficiency and help me solve problems with ease. Learning how to use the resources I had helped me improve my resourcefulness and taught me not to try and "rediscover fire" when building pipelines and models. Finally, through this project I gained extensive experience working with different parts of GCS and how to trouble shoot within GCS if any cloud related issues pop up. I found this experience to be very valuable for my future endeavors.
