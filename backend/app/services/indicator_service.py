import re

from backend.app.schemas.indicators import DetectedIndicator

from backend.app.services.patterns.threats import THREAT_PATTERNS
from backend.app.services.patterns.urgency import URGENCY_PATTERNS
from backend.app.services.patterns.sensitive_requests import SENSITIVE_REQUEST_PATTERNS


def extract_urgency_indicators(
    message: str,
) -> list[DetectedIndicator]:

    detected_indicators = []

    for pattern in URGENCY_PATTERNS:

        matches = re.finditer(
            pattern,
            message,
            flags=re.IGNORECASE,
        )

        for match in matches:

            detected_indicators.append(
                DetectedIndicator(
                    category="urgency",
                    matched_text=match.group(),
                )
            )

    return detected_indicators

def extract_threat_indicators(
    message: str,
) -> list[DetectedIndicator]:

    detected_indicators = []

    for pattern in THREAT_PATTERNS:
        matches = re.finditer(
            pattern,
            message,
            flags=re.IGNORECASE,
        )

        for match in matches:
            detected_indicators.append(
                DetectedIndicator(
                    category="threats",
                    matched_text=match.group(),
                )
            )

    return detected_indicators

def extract_sensitive_information_requests(
    message: str,
) -> list[DetectedIndicator]:

    detected_indicators = []

    for pattern in SENSITIVE_REQUEST_PATTERNS:
        matches = re.finditer(
            pattern,
            message,
            flags=re.IGNORECASE,
        )

        for match in matches:
            detected_indicators.append(
                DetectedIndicator(
                    category="sensitive_information_request",
                    matched_text=match.group(),
                )
            )

    return detected_indicators