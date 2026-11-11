from fastapi import FastAPI

from backend.app.schemas.message import MessageAnalysisRequest, MessageAnalysisResponse
from backend.app.services.message_service import analyze_message

app = FastAPI()


@app.get("/")
async def root():
    return {
        "application": "FinSafe AI",
        "message": "Welcome to FinSafe AI API",
        "version": "0.1.0",
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "application": "FinSafe AI",
    }

@app.get("/api/v1/info")
async def application_info():
    return {
        "name": "FinSafe AI",
        "description": "GenAI-powered personal financial safety assistant",
        "version": "0.1.0",
        "status": "development",
    }

@app.post(
    "/api/v1/analyse/message",
    response_model=MessageAnalysisResponse,
)
async def analyse_user_message(
    request: MessageAnalysisRequest,
):
    return analyze_message(request)