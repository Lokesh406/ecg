from __future__ import annotations

from pathlib import Path

VALID_ECG_EXTENSIONS = {".csv"}
VALID_PROTEIN_EXTENSIONS = {".fasta", ".fa", ".txt"}
MAX_ECG_SIZE = 5 * 1024 * 1024
MAX_PROTEIN_SIZE = 2 * 1024 * 1024


def validate_csv_file(filename: str | None) -> bool:
    if not filename:
        return False
    return Path(filename).suffix.lower() in VALID_ECG_EXTENSIONS


def validate_protein_file(filename: str | None) -> bool:
    if not filename:
        return False
    return Path(filename).suffix.lower() in VALID_PROTEIN_EXTENSIONS


def sanitize_text(value: str) -> str:
    return value.replace("\r", "").replace("\n", " ").strip()
