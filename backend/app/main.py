from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import ALLOWED_ORIGINS, API_PREFIX
from app.database.database import Base, engine
from app.routes import dashboard, ecg, protein, reports

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Cloud-Based Healthcare and Biological Data Analysis Platform",
    description="Unified cloud application for ECG analysis and protein structure analysis",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ecg.router, prefix=f"{API_PREFIX}/ecg")
app.include_router(protein.router, prefix=f"{API_PREFIX}/protein")
app.include_router(dashboard.router, prefix=f"{API_PREFIX}")
app.include_router(reports.router, prefix=f"{API_PREFIX}")


@app.get(f"{API_PREFIX}/health")
def health_check():
    return {
        "status": "ok",
        "service": "Cloud Science Analytics Platform",
        "modules": ["ECG Analysis", "Protein Analysis"],
    }


@app.get("/")
def root():
    return {
        "message": "Cloud Science Analytics Platform API",
        "documentation": "/docs",
    }
