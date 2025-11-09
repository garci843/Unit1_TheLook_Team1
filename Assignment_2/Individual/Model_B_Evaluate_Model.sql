# ✅ Evaluate enhanced model
%%bigquery --project $PROJECT_ID
SELECT *
FROM ML.EVALUATE(MODEL `titanic.Model_B`);
