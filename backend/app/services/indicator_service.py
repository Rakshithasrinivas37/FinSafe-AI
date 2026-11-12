import re

from backend.app.schemas.indicators import DetectedIndicator
from backend.app.services.patterns.negation import NEGATION_PATTERNS
from backend.app.services.patterns.sensitive_requests import SENSITIVE_REQUEST_PATTERNS
from backend.app.services.patterns.threats import THREAT_PATTERNS
from backend.app.services.patterns.transactions import FINANCIAL_TRANSACTION_PATTERNS
from backend.app.services.patterns.urgency import URGENCY_PATTERNS
from backend.app.services.text_preprocessing.clause_splitter import split_into_clauses
from backend.app.services.text_preprocessing.reference_resolver import (
    resolve_sensitive_references,
)

EDUCATIONAL_CONTEXT_PATTERNS = [
    r"\b(?:scammers?|fraudsters?|criminals?|attackers?)\b",
    r"\b(?:this article|this guide|this example|the security guide)\b",
    r"\b(?:training|educational)\s+example\b",
]


REPORTING_CONTEXT_PATTERNS = [
    r"\b(?:the\s+)?(?:message|text|email|sms)\s+",
    r"(?:says|said|reads|contains)\s*['\"]?\s*$",
    r"\b(?:i|we)\s+(?:received|got)\s+",
    r"(?:a|the)\s+(?:message|request|email|text)\s+",   
    r"(?:asking|telling|instructing)\s+(?:me|us)\s+to\b",
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
                if (
                    is_indicator_negated(clause, match.start())
                    or is_quoted_content(clause, match.start())
                    or is_educational_context(clause)
                    ):
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
    resolved_clauses = resolve_sensitive_references(clauses)

    for clause in resolved_clauses:
        for pattern in SENSITIVE_REQUEST_PATTERNS:
            matches = re.finditer(
                pattern,
                clause,
                flags=re.IGNORECASE,
            )

            for match in matches:
                if (
                    is_indicator_negated(clause, match.start()) 
                    or is_reported_content(clause, match.start())
                    or is_quoted_content(clause, match.start())
                    or is_educational_context(clause)
                ):
                    continue

                detected_indicators.append(
                    DetectedIndicator(
                        category="sensitive_information_request",
                        matched_text=match.group(),
                    )
                )

    return detected_indicators


def extract_financial_transaction_requests(
    message: str,
) -> list[DetectedIndicator]:

    indicators = []

    clauses = split_into_clauses(message)

    for clause in clauses:
        for pattern in FINANCIAL_TRANSACTION_PATTERNS:
            for match in re.finditer(
                pattern,
                clause,
                flags=re.IGNORECASE,
            ):
                if is_indicator_negated(clause, match.start()):
                    continue

                if is_reported_content(clause, match.start()):
                    continue

                if is_educational_context(clause):
                    continue

                if is_quoted_content(clause, match.start()):
                    continue

                indicators.append(
                    DetectedIndicator(
                        category="transaction_request",
                        matched_text=match.group(0),
                    )
                )

    return indicators


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

def is_educational_context(clause: str) -> bool:
    return any(
        re.search(pattern, clause, flags=re.IGNORECASE)
        for pattern in EDUCATIONAL_CONTEXT_PATTERNS
    )


def is_quoted_content(clause: str, match_start: int) -> bool:
    """Return True when a match falls inside quoted text."""

    quote_pattern = r"""(['"])(.*?)\1"""

    for match in re.finditer(
        quote_pattern,
        clause,
        flags=re.DOTALL,
    ):
        if match.start(2) <= match_start < match.end(2):
            return True

    return False
