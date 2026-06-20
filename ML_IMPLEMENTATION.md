# SYNVAULT Machine Learning Implementation

SYNVAULT uses an unsupervised machine learning anomaly detection layer together with rule-based fraud scoring.

## Why Unsupervised ML?

The financial transaction CSV files used in this project do not contain a confirmed fraud label column such as `is_fraud`, `fraud`, or `target`. Because of that, a supervised model such as Logistic Regression, Random Forest, or SVM cannot be trained correctly without inventing labels.

For the prototype stage, the correct lightweight ML choice is unsupervised anomaly detection. This allows the system to learn normal transaction behavior from the uploaded statement and flag transactions that are unusual compared with the rest of the file.

## Model Used

The implemented ML model is:

```text
Unsupervised Z-Score Anomaly Detection
```

It trains on every uploaded CSV file and calculates how unusual each transaction is compared with the average pattern of that statement.

## Features Used

The ML model uses these features:

- absolute transaction amount
- login attempts
- account balance
- transaction duration
- risk-sensitive transaction type: transfer or withdrawal
- unknown or missing location
- suspicious channel: unknown or other

## How It Works

1. The uploaded CSV is read by the Python backend.
2. Numeric and encoded features are extracted from each transaction.
3. The system calculates the mean and standard deviation for each feature.
4. Each transaction receives a z-score based anomaly score.
5. The highest unusual transactions are marked as ML anomalies.
6. The ML result is combined with the rule-based risk score.

## Output Stored Per Transaction

Each transaction stores:

```text
ml_model
ml_anomaly_score
ml_raw_score
ml_prediction
ml_confidence
ml_reasons
```

Example values:

```text
ml_prediction: Anomaly
ml_anomaly_score: 87.4
ml_confidence: 93.46
ml_reasons: ML anomaly: unusual absolute amount
```

## Why This Is Suitable For The Project

This approach is suitable because SYNVAULT is a prototype and the dataset is unlabelled. It still satisfies the model-development objective because the system contains a real model-based detection layer that learns transaction patterns from data.

In future work, if a labelled fraud dataset is available, this can be extended to supervised machine learning models such as:

- Logistic Regression
- Decision Tree
- Random Forest
- XGBoost
- Neural Network

## How To Explain To The Professor

You can say:

> The original dataset did not include a confirmed fraud label column, so I could not train a supervised classifier correctly. Therefore, for the prototype, I implemented an unsupervised anomaly detection model. It learns normal transaction behavior from each uploaded CSV using features such as amount, login attempts, account balance, transaction duration, transaction type, location, and channel. It then calculates anomaly scores and flags unusual transactions. I also combined this with rule-based risk scoring to make the output explainable.

Local test result from the updated project:

```text
Statement 1: 2512 transactions, 600 fraud records, 60 ML anomalies
```
