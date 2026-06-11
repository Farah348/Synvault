# SYNVAULT JSON Database Version

This repository contains the updated SYNVAULT fraud intelligence project using a local JSON file as the database.

## Run

Double-click `START_SYNVAULT.bat`, or run:

```powershell
cd BACKEND
python main.py
```

Then open:

```text
http://127.0.0.1:8000
```

## Database Proof

The working data is stored in:

```text
BACKEND/data/database.json
```

That JSON file stores users, statements, and transactions from the local app run.
