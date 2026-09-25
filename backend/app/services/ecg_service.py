from __future__ import annotations

import io
from typing import Any

import numpy as np
import pandas as pd
from scipy.signal import find_peaks


class ECGService:
    def __init__(self) -> None:
        pass

    def analyze_signal(self, file_bytes: bytes) -> dict[str, Any]:
        csv_text = file_bytes.decode("utf-8", errors="ignore")
        df = pd.read_csv(io.StringIO(csv_text))

        if "ecg" not in df.columns:
            raise ValueError("Missing required 'ecg' column in CSV file.")

        signal = df["ecg"].astype(float).to_numpy()
        if len(signal) < 10:
            raise ValueError("ECG signal is too short for analysis.")

        peaks, _ = find_peaks(signal, distance=max(1, len(signal) // 20))
        rr_intervals = np.diff(peaks)
        heart_rate = 60.0 / np.mean(rr_intervals) if len(rr_intervals) > 0 else 0.0

        result = {
            "mean_value": float(np.mean(signal)),
            "std_value": float(np.std(signal)),
            "min_value": float(np.min(signal)),
            "max_value": float(np.max(signal)),
            "signal_range": float(np.max(signal) - np.min(signal)),
            "peak_count": int(len(peaks)),
            "average_rr_interval": float(np.mean(rr_intervals)) if len(rr_intervals) > 0 else 0.0,
            "heart_rate": float(heart_rate),
            "classification": "Normal" if heart_rate >= 50 and heart_rate <= 120 else "Abnormal",
        }
        return result
