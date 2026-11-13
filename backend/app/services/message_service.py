import logging

logger = logging.getLogger(__name__)

from backend.app.schemas.message import MessageAnalysisRequest, MessageAnalysisResponse
from backend.app.services.indicator_service import (
    extract_financial_transaction_requests,
    extract_secrecy_indicators,
    extract_sensitive_information_requests,
    extract_threat_indicators,
    extract_urgency_indicators,
)
from backend.app.services.llm.llm_service import (
    LLMServiceError,
    generate_explanation,
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

    transaction_indicators = extract_financial_transaction_requests(
        request.message
    )

    secrecy_indicators = extract_secrecy_indicators(
        request.message
    )

    indicators = (
        urgency_indicators 
        + threat_indicators 
        + sensitive_information_indicators
        + transaction_indicators
        + secrecy_indicators
        )

    risk_assessment = assess_risk(indicators)

    # Step 3: Generate an LLM explanation
    # Fall back to the deterministic explanation if the LLM fails.
    analysis = risk_assessment.explanation

    try:
        analysis = generate_explanation(
            indicators,
            risk_assessment,
        )
    except LLMServiceError as exc:
        logger.warning(
        "LLM explanation failed; using deterministic fallback: %s",
        exc,
    )

    # Step 3: Return structured response
    response = MessageAnalysisResponse(
        status="completed",
        message="Message analysis completed.",
        analysis=analysis,
        indicators=indicators,
        risk_assessment=risk_assessment
    )

    return response