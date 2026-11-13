from backend.app.schemas.indicators import DetectedIndicator
from backend.app.schemas.risk import RiskAssessment


def assess_risk(
    indicators: list[DetectedIndicator],
) -> RiskAssessment:

    categories = {indicator.category for indicator in indicators}
    reasons = []

    has_urgency = "urgency" in categories
    has_threat = "threats" in categories
    has_sensitive_request = (
        "sensitive_information_request" in categories
    )
    has_financial_transaction = (
        "transaction_request" in categories
    )
    has_secrecy_request = "secrecy_request" in categories

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

    if has_financial_transaction:
        reasons.append(
            "The message requests a financial action "
            "such as transferring money or making a payment."
        )

    if has_secrecy_request:
        reasons.append(
            "The message encourages secrecy or discourages "
            "the recipient from discussing the request with others."
        )

    # High-risk conditions
    if (
        has_sensitive_request
        or (
            has_threat
            and (has_urgency or has_financial_transaction)
        )
        or (
            has_secrecy_request
            and (
                has_urgency
                or has_threat
                or has_financial_transaction
            )
        )
    ):
        risk_level = "high"

    # Medium-risk conditions
    elif (
        has_secrecy_request
        or has_threat
        or (has_financial_transaction and has_urgency)
    ):
        risk_level = "medium"

    else:
        risk_level = "low"

    if risk_level == "high":
        explanation = (
            "Multiple concerning indicators or a sensitive "
            "information request were detected. Verify the "
            "message independently before taking action."
        )

    elif risk_level == "medium":
        explanation = (
            "The message contains potentially concerning "
            "language, such as secrecy instructions or threats. "
            "Verify the request through an official channel "
            "before responding or making a payment."
        )

    elif has_financial_transaction:
        explanation = (
            "The message requests a financial transaction. "
            "Verify the recipient and purpose independently "
            "before transferring money or making a payment."
        )

    elif has_urgency:
        explanation = (
            "The message contains urgency-related language. "
            "Take time to verify the request before acting."
        )

    else:
        explanation = (
            "Few or no known risk indicators were detected. "
            "This does not guarantee that the message is safe."
        )

    if not indicators:
        reasons.append("No known risk indicators were detected.")

    return RiskAssessment(
        risk_level=risk_level,
        reasons=reasons,
        explanation=explanation,
    )
