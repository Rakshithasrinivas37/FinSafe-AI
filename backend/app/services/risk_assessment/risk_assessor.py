"""
The responsibility of risk_assessor.py will be to:
    1. Accept the detected indicators.
    2. Evaluate their severity and combinations.
    3. Determine a risk level.
    4. Generate evidence-based explanations.
    5. Return the assessment.
"""


from backend.app.schemas.indicators import DetectedIndicator
from backend.app.schemas.risk import RiskAssessment


def assess_risk(
    indicators: list[DetectedIndicator],
) -> RiskAssessment:
    """Assess message risk using detected indicators."""

    categories = {indicator.category for indicator in indicators}

    reasons = []

    has_urgency = "urgency" in categories
    has_threat = "threats" in categories
    has_sensitive_request = (
        "sensitive_information_request" in categories
    )

    if has_sensitive_request:
        reasons.append(
            "The message requests sensitive information "
            "such as an OTP, PIN, or password."
        )

    if has_threat:
        reasons.append(
            "The message contains threatening language "
            "such as account blocking or suspension."
        )

    if has_urgency:
        reasons.append(
            "The message creates pressure to act quickly."
        )

    # Rule 1: Requests for sensitive information
    if has_sensitive_request or has_threat and has_urgency:
        risk_level = "high"

    # Rule 3: Threat without urgency
    elif has_threat:
        risk_level = "medium"

    # Rule 4: Urgency without other indicators
    elif has_urgency:
        risk_level = "low"

    # Rule 5: No indicators detected
    else:
        risk_level = "low"
        reasons.append(
            "No known risk indicators were detected."
        )

    if risk_level == "high":
        explanation = (
            "Multiple concerning indicators or a sensitive "
            "information request were detected. Verify the "
            "message independently before taking action."
        )
    elif risk_level == "medium":
        explanation = (
            "The message contains potentially concerning "
            "language. Verify the claim through an official "
            "channel before responding."
        )
    else:
        explanation = (
            "Few or no known risk indicators were detected. "
            "This does not guarantee that the message is safe."
        )

    return RiskAssessment(
        risk_level=risk_level,
        reasons=reasons,
        explanation=explanation,
    )
