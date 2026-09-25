from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class ProteinUploadResponse(BaseModel):
    message: str
    id: int
    protein_name: str
    sequence_length: int


class ProteinAnalysisResult(BaseModel):
    id: int
    protein_name: str
    sequence: str
    sequence_length: Optional[int] = None
    molecular_weight: Optional[float] = None
    hydrophobicity: Optional[float] = None
    secondary_structure: Optional[str] = None
    disclaimer: Optional[str] = None
