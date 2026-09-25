# Cloud Science Analytics Platform

This project is a unified cloud application for scientific data analysis. It combines:

- ECG signal analysis
- Protein sequence analysis
- Shared dashboard, reports, history, and cloud storage

The application follows a single frontend, single backend, single database, and one shared AWS S3 bucket architecture.

## Project structure

```text
cloud-science-platform/
├── backend/
│   ├── app/
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
├── frontend/
│   ├── src/
│   ├── package.json
│   ├── vite.config.js
│   └── .env.example
├── data/
│   ├── ecg/
│   └── protein/
├── reports/
├── README.md
├── .gitignore
└── docker-compose.yml   # optional
```

## Phase 2 status

This phase creates the project skeleton and backend foundation.

## Next steps

- Install backend dependencies
- Create SQLite database models
- Implement API routes
- Add ECG and protein logic
- Build React frontend
- Connect to backend
- Add AWS S3 integration

## Local backend run

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Local frontend run

```bash
cd frontend
npm install
npm run dev
```
