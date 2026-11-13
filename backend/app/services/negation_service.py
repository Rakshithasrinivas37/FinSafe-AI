
import spacy

nlp = spacy.load("en_core_web_sm")


SENSITIVE_ACTIONS = {
    "send",
    "share",
    "provide",
    "reveal",
    "disclose",
    "enter",
    "submit",
    "sharing",
    "providing",
    "revealing",
    "disclosing",
    "entering",
    "submitting",
    "need",
    "needs",
    "require",
    "requires",
    "want",
    "wants",
}

NEGATED_REQUEST_VERBS = {
    "ask",
    "request",
    "require",
    "instruct",
    "tell",
}


def find_action_start(
    text: str,
    match_start: int,
    match_end: int,
) -> int | None:
    doc = nlp(text)

    for token in doc:
        if (
            token.idx >= match_start
            and token.idx < match_end
            and token.text.lower() in SENSITIVE_ACTIONS
        ):
            return token.idx

    return None



def has_direct_negation(token) -> bool:
    return any(
        child.dep_ == "neg"
        for child in token.children
    )


def has_or_coordination(token) -> bool:
    return any(
        child.dep_ == "cc"
        and child.text.lower() == "or"
        and child.i < token.i
        for child in token.head.children
    )


def is_action_negated(
    text: str,
    target_start: int,
) -> bool:
    doc = nlp(text)

    target = next(
        (
            token
            for token in doc
            if token.idx <= target_start < token.idx + len(token)
        ),
        None,
    )

    if target is None:
        return False

    # Check direct negation.
    if has_direct_negation(target):
        return True

    if has_negated_request_ancestor(target):
        return True

    # Traverse the coordinated action chain.
    current = target

    while current.dep_ == "conj":
        parent = current.head

        # Negation propagates through an "or" coordination.
        if (
            has_or_coordination(current)
            and has_direct_negation(parent)
        ):
            return True

        current = parent

    return False


def is_matched_action_negated(
    text: str,
    match_start: int,
    match_end: int,
) -> bool:
    action_start = find_action_start(
        text,
        match_start,
        match_end,
    )

    if action_start is None:
        return False

    return is_action_negated(text, action_start)


def has_negated_request_ancestor(token) -> bool:
    current = token.head

    while current != token:
        if (
            current.pos_ == "VERB"
            and current.lemma_.lower() in NEGATED_REQUEST_VERBS
            and has_direct_negation(current)
        ):
            return True

        if current.head == current:
            break

        current = current.head

    return False