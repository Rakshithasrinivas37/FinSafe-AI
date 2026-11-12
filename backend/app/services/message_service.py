from backend.app.schemas.message import MessageAnalysisRequest, MessageAnalysisResponse
from backend.app.services.indicator_service import (
    extract_sensitive_information_requests,
    extract_threat_indicators,
    extract_urgency_indicators,
)


def analyze_message(request: MessageAnalysisRequest) -> MessageAnalysisResponse:
    """Analyze the message sent by the user"""

    # Step 1: Extract indicators
    urgency_indicators = extract_urgency_indicators(
        request.message
    )

    threat_indicators = extract_threat_indicators(
        request.message
    )

    sensitive_information_indicators = extract_sensitive_information_requests(
        request.message
    )

    indicators = urgency_indicators + threat_indicators + sensitive_information_indicators

    # Step 2: Generate a basic analysis summary
    if indicators:
        analysis = (
            "Urgency-related language was detected "
            "in the submitted message."
        )
    else:
        analysis = (
            "No urgency-related language was detected."
        )

    # Step 3: Return structured response
    return MessageAnalysisResponse(
        status="completed",
        message="Message analysis completed.",
        analysis=analysis,
        indicators=indicators,
    )