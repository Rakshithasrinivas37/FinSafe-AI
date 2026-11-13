from typing import Literal

from pydantic import BaseModel, Field


class IndicatorExplanation(BaseModel):
    category: Literal[
        "urgency",
        "threats",
        "sensitive_information_request",
        "transaction_request",
        "secrecy_request",
    ]

    evidence: str
    explanation: str


class LLMExplanation(BaseModel):
    summary: str

    indicator_explanations: list[IndicatorExplanation] = Field(
        default_factory=list
    )

    recommended_actions: list[str] = Field(
        default_factory=list
    )

    limitations: str