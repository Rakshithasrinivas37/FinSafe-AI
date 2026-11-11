from backend.app.schemas.message import MessageAnalysisRequest, MessageAnalysisResponse


def analyze_message(request: MessageAnalysisRequest) -> MessageAnalysisResponse:
    """Analyze the message sent by the user"""

    return MessageAnalysisResponse(
        status="pending_implementation",
        message="Message received successfully.",
        analysis="Scam detection functionality is not implemented yet.",
    )