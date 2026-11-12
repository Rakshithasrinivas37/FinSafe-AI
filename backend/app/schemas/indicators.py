from typing import Literal

from pydantic import BaseModel


class DetectedIndicator(BaseModel):
    category: Literal[
        "urgency", 
        "threats", 
        "sensitive_information_request", 
        "transaction_request",
        ]
    matched_text: str
