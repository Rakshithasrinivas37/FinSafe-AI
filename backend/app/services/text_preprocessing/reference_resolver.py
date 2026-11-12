import re

SENSITIVE_ENTITY_PATTERN = re.compile(
    r"\b(?:"
    r"one[- ]time password|"
    r"otp|"
    r"atm pin|"
    r"pin|"
    r"banking password|"
    r"password|"
    r"cvv|"
    r"(?:debit|credit|bank) card details|"
    r"(?:internet banking|online banking|banking) credentials"
    r")\b",
    flags=re.IGNORECASE,
)

REQUEST_PRONOUN_PATTERN = re.compile(
    r"\b(?P<verb>send|share|provide|reveal|disclose|enter|submit)"
    r"\s+it\b",
    flags=re.IGNORECASE,
)



def resolve_sensitive_references(clauses: list[str]) -> list[str]:
    resolved_clauses = []
    previous_sensitive_entity = None

    for clause in clauses:

        # Resolve references using only the preceding clause.
        if previous_sensitive_entity:
            clause = REQUEST_PRONOUN_PATTERN.sub(
                lambda match, entity=previous_sensitive_entity: (
                    f"{match.group('verb')} your {entity}"
                ),
                clause,
            )

        resolved_clauses.append(clause)

        # Extract sensitive entities from the current clause.
        matches = list(SENSITIVE_ENTITY_PATTERN.finditer(clause))

        if matches:
            previous_sensitive_entity = matches[-1].group()
        else:
            # Do not carry references across unrelated clauses.
            previous_sensitive_entity = None

    return resolved_clauses
