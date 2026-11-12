from backend.app.schemas.message import MessageAnalysisRequest, MessageAnalysisResponse
from backend.app.services.indicator_service import (
    extract_sensitive_information_requests,
    extract_threat_indicators,
    extract_urgency_indicators,
)
from backend.app.services.risk_assessment.risk_assessor import assess_risk


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

    risk_assessment = assess_risk(indicators)

    # Step 3: Return structured response
    return MessageAnalysisResponse(
        status="completed",
        message="Message analysis completed.",
        analysis=risk_assessment.explanation,
        indicators=indicators,
        risk_assessment=risk_assessment
    )