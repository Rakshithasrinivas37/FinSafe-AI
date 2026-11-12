from typing import Literal

from pydantic import BaseModel


class RiskAssessment(BaseModel):
    risk_level: Literal["low", "medium", "high"]
    reasons: list[str]
    explanation: str