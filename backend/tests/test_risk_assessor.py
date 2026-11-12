from backend.app.schemas.indicators import DetectedIndicator
from backend.app.services.risk_assessment.risk_assessor import assess_risk


def test_no_indicators_returns_low_risk():
    result = assess_risk([])

    assert result.risk_level == "low"


def test_urgency_alone_returns_low_risk():
    indicators = [
        DetectedIndicator(
            category="urgency",
            matched_text="immediately",
        )
    ]

    result = assess_risk(indicators)

    assert result.risk_level == "low"


def test_threat_returns_medium_risk():
    indicators = [
        DetectedIndicator(
            category="threats",
            matched_text="account will be blocked",
        )
    ]

    result = assess_risk(indicators)

    assert result.risk_level == "medium"


def test_threat_and_urgency_return_high_risk():
    indicators = [
        DetectedIndicator(
            category="threats",
            matched_text="account will be blocked",
        ),
        DetectedIndicator(
            category="urgency",
            matched_text="immediately",
        ),
    ]

    result = assess_risk(indicators)

    assert result.risk_level == "high"


def test_sensitive_information_request_returns_high_risk():
    indicators = [
        DetectedIndicator(
            category="sensitive_information_request",
            matched_text="send your OTP",
        )
    ]

    result = assess_risk(indicators)

    assert result.risk_level == "high"


def test_financial_transaction_request_alone_is_low_risk():
    indicators = [
        DetectedIndicator(
            category="transaction_request",
            matched_text="Transfer $500",
        )
    ]

    result = assess_risk(indicators)

    assert result.risk_level == "low"


def test_financial_transaction_with_urgency_is_medium_risk():
    indicators = [
        DetectedIndicator(
            category="transaction_request",
            matched_text="Transfer $500",
        ),
        DetectedIndicator(
            category="urgency",
            matched_text="immediately",
        ),
    ]

    result = assess_risk(indicators)

    assert result.risk_level == "medium"


def test_financial_transaction_with_threat_is_high_risk():
    indicators = [
        DetectedIndicator(
            category="transaction_request",
            matched_text="Transfer $500",
        ),
        DetectedIndicator(
            category="threats",
            matched_text="account will be blocked",
        ),
    ]

    result = assess_risk(indicators)

    assert result.risk_level == "high"

