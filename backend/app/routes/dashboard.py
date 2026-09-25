from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import ECGAnalysis, ProteinAnalysis, Report

router = APIRouter()


@router.get("/dashboard/stats")
def dashboard_stats(db: Session = Depends(get_db)) -> dict[str, Any]:
    ecg_count = db.query(ECGAnalysis).count()
    protein_count = db.query(ProteinAnalysis).count()
    report_count = db.query(Report).count()
    recent_ecg = db.query(ECGAnalysis).order_by(ECGAnalysis.created_at.desc()).limit(5).all()
    recent_protein = db.query(ProteinAnalysis).order_by(ProteinAnalysis.created_at.desc()).limit(5).all()
    recent_analyses = [
        {"type": "ECG", "name": item.file_name, "status": "Completed", "created_at": item.created_at}
        for item in recent_ecg
    ] + [
        {"type": "Protein", "name": item.protein_name, "status": "Completed", "created_at": item.created_at}
        for item in recent_protein
    ]
    recent_analyses.sort(key=lambda item: item["created_at"] or 0, reverse=True)

    return {
        "ecg_analyses": ecg_count,
        "protein_analyses": protein_count,
        "files_stored": ecg_count + protein_count,
        "reports_generated": report_count,
        "recent_analyses": [
            {key: value.isoformat() if key == "created_at" and value else value for key, value in item.items()}
            for item in recent_analyses[:5]
        ],
    }


@router.get("/history")
def history(db: Session = Depends(get_db)) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []

    for item in db.query(ECGAnalysis).all():
        results.append(
            {
                "id": item.id,
                "type": "ECG",
                "name": item.file_name,
                "date": item.created_at.strftime("%d/%m/%y") if item.created_at else "",
                "status": "Completed",
            }
        )

    for item in db.query(ProteinAnalysis).all():
        results.append(
            {
                "id": item.id,
                "type": "Protein",
                "name": item.protein_name,
                "date": item.created_at.strftime("%d/%m/%y") if item.created_at else "",
                "status": "Completed",
            }
        )

    return results
