from __future__ import annotations

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import ProteinAnalysis, Report
from app.services.report_service import ReportService
from app.services.protein_service import ProteinService
from app.services.s3_service import S3Service

router = APIRouter()
VALID_AMINO_ACIDS = set("ACDEFGHIKLMNPQRSTVWY")


def parse_protein_sequence(content: bytes) -> str:
    text = content.decode("utf-8", errors="ignore")
    sequence_lines = [line.strip() for line in text.splitlines() if not line.strip().startswith(">")]
    return "".join(sequence_lines).replace(" ", "").upper()


@router.post("/upload")
async def upload_protein(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename or not file.filename.lower().endswith((".fasta", ".fa", ".txt")):
        raise HTTPException(status_code=400, detail="Only FASTA or text files are allowed for protein analysis.")

    if file.size and file.size > 2 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File exceeds 2MB size limit.")

    content = await file.read()
    sequence = parse_protein_sequence(content)

    if not sequence:
        raise HTTPException(status_code=400, detail="Uploaded protein sequence is empty.")

    invalid = sorted({char.upper() for char in sequence if char.upper() not in VALID_AMINO_ACIDS})
    if invalid:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Invalid amino acid characters found: {invalid[:10]}. "
                "Use one-letter amino-acid codes only; FASTA headers must start with >."
            ),
        )

    analysis = ProteinService().analyze_sequence(sequence)
    storage_url = S3Service().upload_file(file.filename, content, "protein/uploads")
    record = ProteinAnalysis(
        protein_name=file.filename,
        sequence=analysis["sequence"],
        s3_path=storage_url,
        sequence_length=analysis["sequence_length"],
        molecular_weight=analysis["molecular_weight"],
        hydrophobicity=analysis["hydrophobicity"],
        secondary_structure=analysis["secondary_structure"],
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return {
        "message": "Protein file uploaded successfully",
        "id": record.id,
        "protein_name": record.protein_name,
        "sequence_length": record.sequence_length,
        "molecular_weight": record.molecular_weight,
        "hydrophobicity": record.hydrophobicity,
        "secondary_structure": record.secondary_structure,
    }


@router.post("/analyze")
async def analyze_protein(db: Session = Depends(get_db)):
    record = db.query(ProteinAnalysis).order_by(ProteinAnalysis.id.desc()).first()
    if not record:
        raise HTTPException(status_code=404, detail="No protein analysis found.")

    report_text = ReportService().generate_protein_report_text({
        "protein_name": record.protein_name,
        "sequence_length": record.sequence_length,
        "molecular_weight": record.molecular_weight,
        "hydrophobicity": record.hydrophobicity,
        "secondary_structure": record.secondary_structure,
    })
    report_name = f"{record.protein_name.replace('.txt', '').replace('.fa', '').replace('.fasta', '')}_protein_report.txt"
    report_link = S3Service().upload_file(report_name, report_text.encode("utf-8"), "protein/reports")

    report = Report(
        report_type="Protein",
        related_id=record.id,
        file_name=report_name,
        s3_path=report_link,
    )
    db.add(report)
    db.commit()

    return {
        "id": record.id,
        "protein_name": record.protein_name,
        "sequence_length": record.sequence_length,
        "molecular_weight": record.molecular_weight,
        "hydrophobicity": record.hydrophobicity,
        "secondary_structure": record.secondary_structure,
        "status": "Completed",
        "report_id": report.id,
        "report_path": report.s3_path,
        "disclaimer": "Educational protein analysis only. This is not experimental 3D structure prediction.",
    }


@router.get("/results/{analysis_id}")
def get_protein_result(analysis_id: int, db: Session = Depends(get_db)):
    record = db.query(ProteinAnalysis).filter(ProteinAnalysis.id == analysis_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Protein result not found.")

    return {
        "id": record.id,
        "protein_name": record.protein_name,
        "sequence": record.sequence,
        "sequence_length": record.sequence_length,
        "molecular_weight": record.molecular_weight,
        "hydrophobicity": record.hydrophobicity,
        "secondary_structure": record.secondary_structure,
    }


@router.get("/report/{analysis_id}")
def get_protein_report(analysis_id: int, db: Session = Depends(get_db)):
    record = db.query(ProteinAnalysis).filter(ProteinAnalysis.id == analysis_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Protein report not found.")

    return {
        "analysis_id": record.id,
        "protein_name": record.protein_name,
        "sequence": record.sequence,
        "sequence_length": record.sequence_length,
        "molecular_weight": record.molecular_weight,
        "hydrophobicity": record.hydrophobicity,
        "secondary_structure": record.secondary_structure,
        "disclaimer": "Educational protein analysis only. This is not experimental 3D structure prediction.",
    }
