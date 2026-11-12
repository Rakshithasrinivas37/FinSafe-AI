THREAT_PATTERNS = [
    (
        r"\b(?:account|access|card|payment)\s+"
        r"(?:will be|has been|may be|could be|might be|can be)\s+"
        r"(?:blocked|suspended|terminated|restricted|frozen)\b"
    ),
    (
        r"\blegal action\s+"
        r"(?:will be|may be|could be|might be)\s+taken\b"
    ),
]