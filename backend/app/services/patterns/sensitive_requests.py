SENSITIVE_REQUEST_PATTERNS = [
    # Direct requests
    r"\b(?:send|share|provide|reveal|disclose|enter|submit)\s+(?:me|us\s+)?(?:your\s+)?(?:one[- ]time password|otp)\b",
    r"\b(?:send|share|provide|reveal|disclose|enter|submit)\s+(?:me|us\s+)?(?:your\s+)?(?:atm\s+)?pin\b",
    r"\b(?:send|share|provide|reveal|disclose|enter|submit)\s+(?:me|us\s+)?(?:your\s+)?(?:banking\s+)?password\b",
    r"\b(?:send|share|provide|reveal|disclose|enter|submit)\s+(?:me|us\s+)?(?:your\s+)?(?:card\s+)?cvv\b",
    r"\b(?:send|share|provide|reveal|disclose|enter|submit)\s+(?:me|us\s+)?(?:your\s+)?(?:debit|credit|bank)\s+card\s+details\b",
    r"\b(?:send|share|provide|reveal|disclose|enter|submit)\s+(?:me|us\s+)?(?:your\s+)?(?:internet banking|online banking|banking)\s+credentials\b",

    # Gerund forms: "sharing your credentials"
    r"\b(?:sharing|providing|revealing|disclosing|entering|submitting)\s+(?:your\s+)?(?:one[- ]time password|otp|pin|password|cvv|(?:debit|credit|bank)\s+card\s+details|(?:internet banking|online banking|banking)\s+credentials)\b",

    # Indirect requests: "We need your OTP"
    r"\b(?:we|i|our team|the verification team)\s+(?:need|needs|require|requires|want|wants)\s+(?:you\s+to\s+)?(?:provide|share|send|enter|submit\s+)?(?:your\s+)?(?:one[- ]time password|otp|pin|password|cvv|(?:debit|credit|bank)\s+card\s+details|(?:internet banking|online banking|banking)\s+credentials)\b",
]

