import re


def split_into_clauses(message: str) -> list[str]:
    sentences = re.split(
        r"(?<=[.!?])\s+|\n+",
        message.strip(),
    )

    clauses = []

    for sentence in sentences:
        sentence_clauses = re.split(
            r"\b(?:but|however|yet|instead)\b|[,;]",
            sentence,
            flags=re.IGNORECASE,
        )

        clauses.extend(
            clause.strip()
            for clause in sentence_clauses
            if clause.strip()
        )

    return clauses