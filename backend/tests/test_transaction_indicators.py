
import pytest

from backend.app.services.indicator_service import (
    extract_financial_transaction_requests,
)


@pytest.mark.parametrize(
    "message",
    [
        "Transfer $500 to this account to unlock your funds.",
        "Please pay the processing fee to receive your prize.",
        "Deposit $200 into the following account.",
        "Buy gift cards and send us the codes.",
        "Send money to this account immediately.",
    ],
)
def test_detect_financial_transaction_requests(message):
    indicators = extract_financial_transaction_requests(message)

    assert len(indicators) >= 1
    assert all(
        indicator.category == "transaction_request"
        for indicator in indicators
    )


@pytest.mark.parametrize(
    "message",
    [
        "I transferred $500 yesterday.",
        "Never transfer money to unknown accounts.",
        "I received a payment today.",
        "The article explains how scammers request money transfers.",
    ],
)
def test_ignore_non_request_transaction_mentions(message):
    indicators = extract_financial_transaction_requests(message)

    assert indicators == []

def test_ignore_reported_transaction_request():
    message = (
        "I received a request asking me to transfer money, "
        "but I ignored it."
    )

    indicators = extract_financial_transaction_requests(message)

    assert indicators == []


def test_detect_direct_transaction_request_after_reported_context():
    message = (
        "I received a suspicious message yesterday. "
        "Transfer $500 to this account immediately."
    )

    indicators = extract_financial_transaction_requests(message)

    assert len(indicators) >= 1
