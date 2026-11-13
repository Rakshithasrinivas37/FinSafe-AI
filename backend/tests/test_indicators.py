import pytest

from backend.app.services.indicator_service import (
    extract_secrecy_indicators,
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


def test_never_share_otp_is_not_a_request():
    result = extract_sensitive_information_requests(
        "Never share your OTP with anyone."
    )
    assert len(result) == 0


def test_bank_never_asks_for_otp():
    result = extract_sensitive_information_requests(
        "Your bank will never ask you to share your OTP."
    )
    assert len(result) == 0


def test_negation_does_not_suppress_later_request():
    result = extract_sensitive_information_requests(
        "Never share your OTP. Send your OTP to this number."
    )
    assert len(result) == 1


def test_mixed_warning_and_request():
    result = extract_sensitive_information_requests(
        "Never share your OTP, but enter your OTP on this page."
    )
    assert len(result) == 1


def test_positive_request_is_still_detected():
    result = extract_sensitive_information_requests(
        "Please share your OTP immediately."
    )
    assert len(result) == 1

@pytest.mark.parametrize(
    "message",
    [
        "Keep this transaction secret.",
        "Do not inform your bank about this transfer.",
        "Never tell anyone about this payment.",
        "Do not discuss this transaction.",
    ],
)
def test_detect_secrecy_requests(message):
    indicators = extract_secrecy_indicators(message)

    assert any(
        indicator.category == "secrecy_request"
        for indicator in indicators
    )


@pytest.mark.parametrize(
    "message",
    [
        "There is no need to keep this transaction secret.",
        "I received a message asking me to keep the transfer secret.",
        "Scammers often tell victims to keep transactions confidential.",
        "Never share your banking password with anyone.",
    ],
)
def test_ignore_non_secrecy_requests(message):
    indicators = extract_secrecy_indicators(message)

    assert not any(
        indicator.category == "secrecy_request"
        for indicator in indicators
    )