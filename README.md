# SYNVAULT JSON Database Version

This repository contains the updated SYNVAULT fraud intelligence project using a local JSON file as the database.

## Database

Data is saved here:

```text
BACKEND/data/database.json
```

The JSON file stores:

- `users`
- `statements`
- `transactions`
- `audit_logs`

Existing users are kept. The first existing user is treated as the admin account, and new signups are normal users.

The browser only stores the active `user_id` and `statement_id` so the pages know which user and uploaded statement are currently active.

## Fraud Detection and ML Model

SYNVAULT now uses two fraud detection layers:

1. **Rule-based risk scoring**
   - Checks transaction amount, transaction type, location, login attempts, account balance, duration, and channel.
   - Adds risk points for suspicious conditions.
   - Stores clear fraud reasons for explainability.

2. **Unsupervised machine learning anomaly detection**
   - Uses a z-score anomaly detection model trained from each uploaded CSV file.
   - Learns the normal pattern of the uploaded statement using features such as amount, login attempts, balance, duration, transaction type, location, and channel.
   - Produces `ml_anomaly_score`, `ml_prediction`, `ml_confidence`, and `ml_reasons` for each transaction.

This ML approach is used because the available CSV files do not include a confirmed fraud label column. Without labels, a supervised model such as logistic regression or random forest cannot be trained correctly. Unsupervised anomaly detection is suitable for the prototype stage because it can still learn unusual transaction behavior from the available financial data.

## What changed from PostgreSQL

- PostgreSQL is not used.
- SQLAlchemy models are not required.
- Signup, login, upload, fraud detection, analytics, transactions, and chatbot routes are handled by a Python local HTTP server.
- The Python backend reads and writes the JSON database file.

## Run

Easiest option:

```text
Double-click START_SYNVAULT.bat
```

That starts the JSON backend and opens the app.

From the backend folder:

```powershell
cd BACKEND
python main.py
```

Then open:

```text
http://127.0.0.1:8000
```

Important: because the app saves data into a JSON file through the backend, run the backend instead of opening the HTML file directly.

## User History

After login, users can open `history.html` from the upload page or dashboard. It shows their previous statement uploads from `database.json`. Opening any old statement stores that statement ID in browser `localStorage` and loads the dashboard analytics for that saved upload.

## Admin Panel

The login page has separate `User Login` and `Admin Login` buttons. Both use the same JSON-backed account system, but the admin button only opens `admin.html` when the account role is `admin`.

Admins can open `admin.html`. The admin panel shows:

- total users
- total uploaded statements
- total transactions
- total fraud records
- all users and upload counts
- all uploaded statements
- high-risk transactions across the full JSON database
- suspicious user ranking by fraud volume and exposure
- admin audit log for role and review-status changes

Admins can also:

- search and filter uploaded statements by user email, file name, risk level, or review status
- update user roles between `admin` and `user`
- mark uploaded statements as `Pending Review`, `Reviewed`, `Escalated`, or `Cleared`
- export user and statement tables as CSV files
- download a full `database.json` backup from the browser

## Current Local Test Result

The updated ML version was tested locally. One uploaded statement showed:

```text
Statement 1: 2512 transactions, 600 fraud records, 60 ML anomalies
```
