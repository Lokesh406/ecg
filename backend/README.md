# Backend README

This backend provides the FastAPI services for the unified cloud science analytics platform.

## Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run locally

```bash
uvicorn app.main:app --reload
```

## API endpoints

- GET /api/health
- POST /api/ecg/upload
- POST /api/ecg/analyze
- GET /api/ecg/results/{id}
- GET /api/ecg/report/{id}
- POST /api/protein/upload
- POST /api/protein/analyze
- GET /api/protein/results/{id}
- GET /api/protein/report/{id}
- GET /api/dashboard/stats
- GET /api/history
- GET /api/reports

## Notes

- Local development uses SQLite.
- AWS S3 integration will be enabled in a later phase.
- ECG classification is educational and not a medical diagnostic tool.
- Protein results are educational and do not claim validated 3D structures.
