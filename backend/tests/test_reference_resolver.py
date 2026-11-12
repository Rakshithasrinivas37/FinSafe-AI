
from backend.app.services.text_preprocessing.clause_splitter import (
    split_into_clauses,
)
from backend.app.services.text_preprocessing.reference_resolver import (
    resolve_sensitive_references,
)


def test_resolve_otp_reference():
    message = "Your bank will never ask for your OTP. Send it to our agent."

    clauses = split_into_clauses(message)
    resolved = resolve_sensitive_references(clauses)

    assert resolved[1] == "Send your OTP to our agent."


def test_resolve_password_reference():
    message = (
        "Do not provide your password over the phone. "
        "Instead, enter it in this verification form."
    )

    clauses = split_into_clauses(message)
    resolved = resolve_sensitive_references(clauses)

    assert resolved[1] == (
        "enter your password in this verification form."
    )


def test_resolve_pin_reference():
    message = (
        "Do not send your PIN to anyone. "
        "Your account will be blocked unless you provide it to this agent."
    )

    clauses = split_into_clauses(message)
    resolved = resolve_sensitive_references(clauses)

    assert "provide your PIN" in resolved[1]


def test_unrelated_clause_does_not_resolve_pronoun():
    message = (
        "Your bank mentioned your OTP. "
        "The weather is good. Send it to our agent."
    )

    clauses = split_into_clauses(message)
    resolved = resolve_sensitive_references(clauses)

    assert resolved[-1] == "Send it to our agent."
