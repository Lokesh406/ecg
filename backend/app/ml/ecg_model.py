from __future__ import annotations

from typing import Any

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


class ECGModel:
    def __init__(self) -> None:
        self.model = RandomForestClassifier(n_estimators=50, random_state=42)

    def train(self, features: list[list[float]], labels: list[str]) -> None:
        X_train, X_test, y_train, y_test = train_test_split(
            features,
            labels,
            test_size=0.2,
            random_state=42,
        )
        self.model.fit(X_train, y_train)
        self._test_accuracy = self.model.score(X_test, y_test)

    def predict(self, features: list[float]) -> str:
        result = self.model.predict([features])[0]
        return str(result)

    def predict_rule_based(self, features: list[float]) -> str:
        mean_value = features[0]
        std_value = features[1]
        if abs(mean_value) <= 0.35 and std_value <= 0.25:
            return "Normal"
        return "Abnormal"

    def get_accuracy(self) -> float:
        return getattr(self, "_test_accuracy", 0.0)
