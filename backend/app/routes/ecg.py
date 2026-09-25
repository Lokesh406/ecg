from __future__ import annotations

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import ECGAnalysis, Report
from app.services.ecg_service import ECGService
from app.services.report_service import ReportService
from app.services.s3_service import S3Service

router = APIRouter()


@router.post("/upload")
async def upload_ecg(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed for ECG analysis.")

    if file.size and file.size > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File exceeds 5MB size limit.")

    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail="Uploaded ECG file is empty.")

    try:
        analysis = ECGService().analyze_signal(file_bytes)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    storage_url = S3Service().upload_file(file.filename, file_bytes, "ecg/uploads")

    record = ECGAnalysis(
        file_name=file.filename,
        s3_path=storage_url,
        heart_rate=analysis["heart_rate"],
        peak_count=analysis["peak_count"],
        mean_value=analysis["mean_value"],
        std_value=analysis["std_value"],
        classification=analysis["classification"],
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return {
        "message": "ECG file uploaded and saved",
        "id": record.id,
        "file_name": record.file_name,
        "s3_path": record.s3_path,
        "heart_rate": record.heart_rate,
        "peak_count": record.peak_count,
        "classification": record.classification,
    }


@router.post("/analyze")
async def analyze_ecg(db: Session = Depends(get_db)):
    record = db.query(ECGAnalysis).order_by(ECGAnalysis.id.desc()).first()
    if not record:
        raise HTTPException(status_code=404, detail="No ECG analysis found.")

    report_text = ReportService().generate_ecg_report_text({
        "file_name": record.file_name,
        "heart_rate": record.heart_rate,
        "peak_count": record.peak_count,
        "mean_value": record.mean_value,
        "std_value": record.std_value,
        "classification": record.classification,
    })
    report_name = f"{record.file_name.replace('.csv', '')}_ecg_report.txt"
    report_link = S3Service().upload_file(report_name, report_text.encode("utf-8"), "ecg/reports")

    report = Report(
        report_type="ECG",
        related_id=record.id,
        file_name=report_name,
        s3_path=report_link,
    )
    db.add(report)
    db.commit()

    return {
        "id": record.id,
        "file_name": record.file_name,
        "heart_rate": record.heart_rate,
        "peak_count": record.peak_count,
        "classification": record.classification,
        "status": "Completed",
        "report_id": report.id,
        "report_path": report.s3_path,
        "disclaimer": "Educational ECG analysis only. This is not medical diagnosis.",
    }


@router.get("/results/{analysis_id}")
def get_ecg_result(analysis_id: int, db: Session = Depends(get_db)):
    record = db.query(ECGAnalysis).filter(ECGAnalysis.id == analysis_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="ECG result not found.")

    return {
        "id": record.id,
        "file_name": record.file_name,
        "s3_path": record.s3_path,
        "heart_rate": record.heart_rate,
        "peak_count": record.peak_count,
        "mean_value": record.mean_value,
        "std_value": record.std_value,
        "classification": record.classification,
    }


@router.get("/report/{analysis_id}")
def get_ecg_report(analysis_id: int, db: Session = Depends(get_db)):
    record = db.query(ECGAnalysis).filter(ECGAnalysis.id == analysis_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="ECG report not found.")

    return {
        "analysis_id": record.id,
        "file_name": record.file_name,
        "heart_rate": record.heart_rate,
        "peak_count": record.peak_count,
        "mean_value": record.mean_value,
        "std_value": record.std_value,
        "classification": record.classification,
        "disclaimer": "Educational ECG analysis only. This is not medical diagnosis.",
    }
