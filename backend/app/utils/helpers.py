from __future__ import annotations

from typing import Any


def build_response(message: str, status: str = "success", **kwargs: Any) -> dict[str, Any]:
    payload = {"message": message, "status": status}
    payload.update(kwargs)
    return payload
