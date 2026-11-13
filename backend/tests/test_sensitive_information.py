import pytest

from backend.app.services.indicator_service import (
    extract_sensitive_information_requests,
)


@pytest.mark.parametrize(
    ("message", "expected"),
    [
        ("Send me your OTP.", True),
        ("Please send your OTP to me.", True),
        ("Do not delay and send me your OTP.", True),
        ("Do not send me your OTP.", False),
        ("Never share your OTP with anyone.", False),
        ("Do not hesitate to send me your OTP.", True),
        ("Do not send your OTP and password.", False),
    ],
)
def test_sensitive_information_request_negation(
    message,
    expected,
):
    result = extract_sensitive_information_requests(message)

    assert bool(result) is expected