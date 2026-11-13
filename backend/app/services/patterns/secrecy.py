SECRECY_PATTERNS = [
    # Direct requests to keep information secret
    (
        r"\b(?:keep|keep this|keep it)\s+"
        r"(?:secret|confidential|private)\b"
    ),

    # Instructions not to disclose information
    (
        r"\b(?:do not|don't|never)\s+"
        r"(?:tell|inform|notify|disclose|reveal|discuss|share)\s+"
        r"(?:anyone|anybody|someone|others|your family|your bank)\b"
    ),

    # Requests for secrecy around transactions
    (
        r"\b(?:keep|maintain)\s+(?:this|the)\s+"
        r"(?:transaction|transfer|payment|conversation|matter)\s+"
        r"(?:secret|confidential|private)\b"
    ),

    # Instructions not to discuss a transaction
    (
        r"\b(?:do not|don't|never)\s+"
        r"(?:discuss|mention|talk about|disclose|share)\s+"
        r"(?:this|the)\s+"
        r"(?:transaction|transfer|payment|matter)\b"
    ),
]

