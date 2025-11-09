# ✅ Train enhanced model
%%bigquery --project $PROJECT_ID
CREATE OR REPLACE MODEL `titanic.Model_B`
OPTIONS(model_type='logistic_reg', input_label_cols=['Survived']) AS
SELECT
  Pclass,
  Sex,
  Age,
  Fare,
  Embarked,
  family_size,
  fare_bucket,
  sex_pclass,
  Survived
FROM `titanic.Model_B_features`;
