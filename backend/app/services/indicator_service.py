import re

from backend.app.schemas.indicators import DetectedIndicator
from backend.app.services.patterns.negation import NEGATION_PATTERNS
from backend.app.services.patterns.sensitive_requests import SENSITIVE_REQUEST_PATTERNS
from backend.app.services.patterns.threats import THREAT_PATTERNS
from backend.app.services.patterns.urgency import URGENCY_PATTERNS
from backend.app.services.text_preprocessing.clause_splitter import split_into_clauses

REPORTING_CONTEXT_PATTERNS = [
    r"\b(?:the\s+)?(?:message|text|email|sms)\s+",
    r"(?:says|said|reads|contains)\s*['\"]?\s*$"
]


def extract_urgency_indicators(
    message: str,
) -> list[DetectedIndicator]:

    detected_indicators = []

    clauses = split_into_clauses(message)

    for clause in clauses:
        for pattern in URGENCY_PATTERNS:

            matches = re.finditer(
                pattern,
                clause,
                flags=re.IGNORECASE,
            )

            for match in matches:
                if is_indicator_negated(clause, match.start()):
                    continue

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

    clauses = split_into_clauses(message)

    for clause in clauses:
        for pattern in THREAT_PATTERNS:
            matches = re.finditer(
                pattern,
                clause,
                flags=re.IGNORECASE,
            )

            for match in matches:
                if is_indicator_negated(clause, match.start()):
                    continue

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

    clauses = split_into_clauses(message)

    for clause in clauses:
        for pattern in SENSITIVE_REQUEST_PATTERNS:
            matches = re.finditer(
                pattern,
                clause,
                flags=re.IGNORECASE,
            )

            for match in matches:
                if is_indicator_negated(clause, match.start()) or is_reported_content(clause, match.start()):
                    continue

                detected_indicators.append(
                    DetectedIndicator(
                        category="sensitive_information_request",
                        matched_text=match.group(),
                    )
                )

    return detected_indicators


def is_indicator_negated(clause: str, match_start: int) -> bool:
    preceding_text = clause[:match_start]

    for pattern in NEGATION_PATTERNS:
        if re.search(
            pattern,
            preceding_text,
            flags=re.IGNORECASE,
        ):
            return True

    return False


def is_reported_content(clause: str, match_start: int) -> bool:
    preceding_text = clause[:match_start]

    for pattern in REPORTING_CONTEXT_PATTERNS:
        if re.search(
            pattern,
            preceding_text,
            flags=re.IGNORECASE,
        ):
            return True

    return False