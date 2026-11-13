import pytest

from backend.app.services.negation_service import is_action_negated
from backend.app.services.negation_service import find_action_start
from backend.app.services.negation_service import (
    is_matched_action_negated,
)

def test_find_action_start_for_direct_request():
    message = "Send me your OTP."
    assert find_action_start(
        message,
        message.index("Send"),
        message.index("OTP") + len("OTP"),
    ) == message.index("Send")


def test_find_action_start_for_indirect_request():
    message = "We need your OTP."
    assert find_action_start(
        message,
        message.index("We"),
        message.index("OTP") + len("OTP"),
    ) == message.index("need")


def test_find_action_start_for_provide_request():
    message = "We need you to provide your OTP."
    assert find_action_start(
        message,
        message.index("provide"),
        message.index("OTP") + len("OTP"),
    ) == message.index("provide")


def test_multiple_occurrences_with_different_negation():
    message = "Do not send your OTP, but send your password."

    first_send = message.index("send")
    second_send = message.index("send", first_send + 1)

    assert is_action_negated(message, first_send) is True
    assert is_action_negated(message, second_send) is False


def test_multiple_occurrences_both_negated():
    message = "Do not send your OTP or send your password."

    first_send = message.index("send")
    second_send = message.index("send", first_send + 1)

    assert is_action_negated(message, first_send) is True
    assert is_action_negated(message, second_send) is True


@pytest.mark.parametrize(
    ("message", "expected"),
    [
        ("Do not send your OTP.", True),
        ("Do not hesitate to send your OTP.", False),
        ("You should not provide your OTP.", True),
        ("Please share your OTP.", False),
    ],
)
def test_action_negation(message, expected):
    target_start = message.lower().find(
        next(
            action
            for action in ["send", "provide", "share"]
            if action in message.lower()
        )
    )

    assert is_action_negated(message, target_start) is expected

def test_negation_shared_by_or_coordinated_actions():
    message = "Do not send your OTP or send your password."

    first_send = message.index("send")
    second_send = message.index("send", first_send + 1)

    assert is_action_negated(message, first_send) is True
    assert is_action_negated(message, second_send) is True


def test_negation_not_shared_across_but():
    message = "Do not send your OTP, but send your password."

    first_send = message.index("send")
    second_send = message.index("send", first_send + 1)

    assert is_action_negated(message, first_send) is True
    assert is_action_negated(message, second_send) is False

def test_negation_with_multiple_coordinated_actions():
    message = "Do not send your OTP or share your PIN or reveal your password."

    actions = [
        message.index("send"),
        message.index("share"),
        message.index("reveal"),
    ]

    for position in actions:
        assert is_action_negated(message, position) is True


def test_negation_with_contrastive_but():
    message = "Do not send your OTP, but share your password."

    assert is_action_negated(message, message.index("send")) is True
    assert is_action_negated(message, message.index("share")) is False


def test_negation_with_unrelated_action():
    message = "Do not hesitate to share your OTP."

    assert is_action_negated(message, message.index("share")) is False


def test_matched_action_direct_negation():
    message = "Do not send your OTP."

    assert is_matched_action_negated(
        message,
        message.index("send"),
        message.index("OTP") + len("OTP"),
    ) is True


def test_matched_action_indirect_negation():
    message = "Do not provide your password."

    assert is_matched_action_negated(
        message,
        message.index("provide"),
        message.index("password") + len("password"),
    ) is True


def test_matched_action_without_negation():
    message = "Please share your OTP."

    assert is_matched_action_negated(
        message,
        message.index("share"),
        message.index("OTP") + len("OTP"),
    ) is False


def test_matched_action_with_unrelated_negation():
    message = "Do not hesitate to share your OTP."

    assert is_matched_action_negated(
        message,
        message.index("share"),
        message.index("OTP") + len("OTP"),
    ) is False


def test_negated_request_ancestor():
    message = "Your bank will never ask you to share your OTP."

    assert is_action_negated(
        message,
        message.index("share"),
    ) is True


def test_negated_hesitation_does_not_negate_action():
    message = "Do not hesitate to share your OTP."

    assert is_action_negated(
        message,
        message.index("share"),
    ) is False


def test_positive_request_does_not_negate_action():
    message = "Your bank will ask you to share your OTP."

    assert is_action_negated(
        message,
        message.index("share"),
    ) is False