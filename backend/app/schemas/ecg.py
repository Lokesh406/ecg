from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class ECGUploadResponse(BaseModel):
    message: str
    id: int
    file_name: str
    s3_path: str


class ECGAnalysisResult(BaseModel):
    id: int
    file_name: str
    heart_rate: Optional[float] = None
    peak_count: Optional[int] = None
    classification: Optional[str] = None
    disclaimer: Optional[str] = None
