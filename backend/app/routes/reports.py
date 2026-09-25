from __future__ import annotations

from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import Report
from app.services.s3_service import S3Service

router = APIRouter()


def _remove_report_file(s3_path: str | None) -> None:
    if not s3_path:
        return

    try:
        if s3_path.startswith("file://"):
            parsed_path = urlparse(s3_path)
            local_path = Path(f"{parsed_path.netloc}{parsed_path.path}")
            if local_path.exists():
                local_path.unlink()
    except (FileNotFoundError, OSError, ValueError):
        pass


@router.get("/reports")
def list_reports(db: Session = Depends(get_db)) -> list[dict[str, Any]]:
    reports = db.query(Report).order_by(Report.created_at.desc()).all()
    return [
        {
            "id": item.id,
            "report_type": item.report_type,
            "related_id": item.related_id,
            "file_name": item.file_name,
            "s3_path": item.s3_path,
            "created_at": item.created_at.isoformat() if item.created_at else None,
        }
        for item in reports
    ]


@router.get("/reports/{report_id}/download")
def download_report(report_id: int, db: Session = Depends(get_db)) -> Response:
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report or not report.s3_path:
        raise HTTPException(status_code=404, detail="Report file not found.")

    try:
        if report.s3_path.startswith("file://"):
            parsed_path = urlparse(report.s3_path)
            local_path = Path(f"{parsed_path.netloc}{parsed_path.path}")
            content = local_path.read_bytes()
        elif report.s3_path.startswith("s3://"):
            content = S3Service().download_file(urlparse(report.s3_path).path.lstrip("/"))
        else:
            raise FileNotFoundError(report.s3_path)
    except (FileNotFoundError, OSError) as exc:
        raise HTTPException(status_code=404, detail="Report file is unavailable.") from exc

    return Response(
        content=content,
        media_type="text/plain",
        headers={"Content-Disposition": f'attachment; filename="{report.file_name}"'},
    )


@router.delete("/reports/{report_id}")
def delete_report(report_id: int, db: Session = Depends(get_db)) -> dict[str, Any]:
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found.")

    _remove_report_file(report.s3_path)
    db.delete(report)
    db.commit()
    return {"message": "Report deleted successfully", "id": report_id}
