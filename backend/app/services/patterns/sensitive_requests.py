
SENSITIVE_REQUEST_PATTERNS = [
    # OTP requests
    r"\b(?:send|share|provide|reveal|disclose|enter)\s+(?:me|us\s+)?(?:your\s+)?(?:one[- ]time password|otp)\b",

    # PIN requests
    r"\b(?:send|share|provide|reveal|disclose|enter)\s+(?:me|us\s+)?(?:your\s+)?(?:atm\s+)?pin\b",

    # Password requests
    r"\b(?:send|share|provide|reveal|disclose|enter)\s+(?:me|us\s+)?(?:your\s+)?(?:banking\s+)?password\b",

    # CVV requests
    r"\b(?:send|share|provide|reveal|disclose|enter)\s+(?:me|us\s+)?(?:your\s+)?(?:card\s+)?cvv\b",

    # Card detail requests
    r"\b(?:send|share|provide|reveal|disclose|enter)\s+(?:me|us\s+)?(?:your\s+)?(?:debit|credit|bank)\s+card\s+details\b",

    # Banking credential requests
    r"\b(?:send|share|provide|reveal|disclose|enter)\s+(?:me|us\s+)?(?:your\s+)?(?:internet banking|online banking|banking)\s+credentials\b",
]
