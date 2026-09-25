from __future__ import annotations

import re
from typing import Any

AA_WEIGHTS = {
    "A": 89.09, "C": 121.16, "D": 133.10, "E": 147.13,
    "F": 165.19, "G": 75.07, "H": 155.16, "I": 131.17,
    "K": 146.19, "L": 131.17, "M": 149.21, "N": 132.12,
    "P": 115.13, "Q": 146.15, "R": 174.20, "S": 105.09,
    "T": 119.12, "V": 117.15, "W": 186.21, "Y": 181.19,
}

HYDROPHOBIC = {"A": 1.8, "V": 4.2, "L": 3.8, "I": 4.5, "M": 1.9, "F": 2.8, "W": -0.9, "Y": -1.3}


def clean_sequence(sequence: str) -> str:
    return re.sub(r"[^ACDEFGHIKLMNPQRSTVWY]", "", sequence.upper())


class ProteinService:
    def __init__(self) -> None:
        pass

    def analyze_sequence(self, sequence: str) -> dict[str, Any]:
        seq = clean_sequence(sequence)
        if len(seq) == 0:
            raise ValueError("Protein sequence is empty or contains invalid characters.")

        composition = {aa: seq.count(aa) for aa in sorted(set(seq))}
        molecular_weight = sum(AA_WEIGHTS.get(aa, 0.0) for aa in seq)
        hydrophobicity = sum(HYDROPHOBIC.get(aa, 0.0) for aa in seq) / len(seq) if seq else 0.0
        secondary_structure = self.predict_secondary_structure(seq)

        return {
            "sequence_length": len(seq),
            "amino_acid_composition": composition,
            "molecular_weight": round(molecular_weight, 2),
            "hydrophobicity": round(hydrophobicity, 4),
            "secondary_structure": secondary_structure,
            "sequence": seq,
        }

    def predict_secondary_structure(self, sequence: str) -> str:
        structure = []
        for aa in sequence:
            if aa in {"A", "L", "M", "E", "K", "R"}:
                structure.append("H")
            elif aa in {"V", "I", "Y", "F", "W"}:
                structure.append("E")
            else:
                structure.append("C")
        return "".join(structure)
