FINANCIAL_TRANSACTION_PATTERNS = [
    # Transfer or send money
    (
        r"\b(?:transfer|send|wire|remit)\s+"
        r"(?:the\s+)?(?:money|funds|payment|amount)\b"
    ),
    (
        r"\b(?:transfer|send|wire|remit)\s+"
        r"(?:[$€£₹]\s*)?\d[\d,]*(?:\.\d{1,2})?\b"
    ),

    # Requests to pay fees or charges
    (
        r"\b(?:pay|settle)\s+(?:the\s+)?"
        r"(?:processing|verification|registration|release|"
        r"service|transaction)\s+(?:fee|charge)\b"
    ),

    # Deposit money
    (
        r"\bdeposit\s+(?:[$€£₹]\s*)?\d[\d,]*(?:\.\d{1,2})?\b"
    ),
    (
        r"\bdeposit\s+(?:the\s+)?(?:money|funds|amount)\b"
    ),

    # Gift cards and cryptocurrency
    (
        r"\b(?:buy|purchase)\s+(?:some\s+)?"
        r"(?:gift cards?|prepaid cards?|cryptocurrency|crypto)\b"
    ),

    # Send gift card codes or cryptocurrency
    (
        r"\b(?:send|share|provide)\s+"
        r"(?:the\s+)?(?:gift card codes?|crypto|cryptocurrency)\b"
    ),
]