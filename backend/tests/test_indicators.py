from backend.app.services.indicator_service import (
    extract_sensitive_information_requests,
    extract_threat_indicators,
    extract_urgency_indicators,
)


def test_detect_immediately():

    message = "Verify your account immediately."

    result = extract_urgency_indicators(message)

    assert len(result) == 1
    assert result[0].category == "urgency"
    assert result[0].matched_text == "immediately"


def test_detect_multiple_urgency_indicators():

    message = (
        "Act now. Your account will be blocked "
        "within 2 hours."
    )

    result = extract_urgency_indicators(message)

    assert len(result) == 2


def test_case_insensitive_urgency_detection():

    message = "ACT NOW to verify your account."

    result = extract_urgency_indicators(message)

    assert len(result) == 1


def test_no_urgency_indicator():

    message = "Your bank statement is ready."

    result = extract_urgency_indicators(message)

    assert len(result) == 0


def test_urgency_within_minutes():

    message = "Respond within 10 minutes."

    result = extract_urgency_indicators(message)

    assert len(result) == 1
    assert result[0].matched_text == "within 10 minutes"

def test_detect_account_blocked():
    result = extract_threat_indicators(
        "Your account will be blocked."
    )

    assert len(result) == 1
    assert result[0].category == "threats"
    assert result[0].matched_text == "account will be blocked"


def test_detect_account_suspended():
    result = extract_threat_indicators(
        "Your account may be suspended."
    )

    assert len(result) == 1


def test_detect_legal_action():
    result = extract_threat_indicators(
        "Legal action will be taken against you."
    )

    assert len(result) == 1


def test_detect_payment_frozen():
    result = extract_threat_indicators(
        "Your payment may be frozen."
    )

    assert len(result) == 1


def test_no_threat_detected():
    result = extract_threat_indicators(
        "Your bank account is active and secure."
    )

    assert len(result) == 0


def test_case_insensitive_threat_detection():
    result = extract_threat_indicators(
        "YOUR ACCOUNT WILL BE BLOCKED."
    )

    assert len(result) == 1

def test_detect_otp_request():
    result = extract_sensitive_information_requests(
        "Send us your OTP."
    )
    assert len(result) == 1


def test_detect_pin_request():
    result = extract_sensitive_information_requests(
        "Please provide your ATM PIN."
    )
    assert len(result) == 1


def test_detect_password_request():
    result = extract_sensitive_information_requests(
        "Enter your banking password."
    )
    assert len(result) == 1


def test_detect_cvv_request():
    result = extract_sensitive_information_requests(
        "Share your card CVV."
    )
    assert len(result) == 1


def test_detect_card_details_request():
    result = extract_sensitive_information_requests(
        "Provide your debit card details."
    )
    assert len(result) == 1


def test_no_sensitive_request():
    result = extract_sensitive_information_requests(
        "Your password has been changed successfully."
    )
    assert len(result) == 0


def test_case_insensitive_sensitive_info_detection():
    result = extract_sensitive_information_requests(
        "SEND YOUR OTP."
    )
    assert len(result) == 1
