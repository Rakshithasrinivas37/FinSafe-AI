import json

import httpx
import pytest

from backend.app.schemas.indicators import DetectedIndicator
from backend.app.schemas.risk import RiskAssessment
from backend.app.services.llm import llm_service
from backend.app.services.llm.llm_service import LLMServiceError


@pytest.fixture
def sample_indicators():
    return [
        DetectedIndicator(
            category="urgency",
            matched_text="immediately",
        ),
        DetectedIndicator(
            category="transaction_request",
            matched_text="Transfer $500",
        ),
    ]


@pytest.fixture
def sample_risk_assessment():
    return RiskAssessment(
        risk_level="high",
        reasons=[
            "The message creates pressure to act quickly.",
            "The message requests a financial transaction.",
        ],
        explanation="The message contains multiple warning signs.",
    )


def test_generate_explanation_success(
    monkeypatch,
    sample_indicators,
    sample_risk_assessment,
):
    monkeypatch.setattr(
        llm_service,
        "GROQ_API_URL",
        "https://test.example.com",
    )
    monkeypatch.setenv("GROQ_API_KEY", "test-api-key")
    monkeypatch.setenv("GROQ_MODEL", "test-model")

    def mock_post(*args, **kwargs):
        return httpx.Response(
            200,
            json={
                "choices": [
                    {
                        "message": {
                            "content": json.dumps({
                            "summary": "This message contains warning signs.",
                            "indicator_explanations": [
                                {
                                    "category": "urgency",
                                    "evidence": "immediately",
                                    "explanation": "The wording pressures the recipient to act quickly."
                                },
                                {
                                    "category": "transaction_request",
                                    "evidence": "Transfer $500",
                                    "explanation": "The message requests a financial transfer."
                                }
                            ],
                            "recommended_actions": [
                                "Verify the request through an independently obtained official channel."
                            ],
                            "limitations": "These indicators do not prove that the message is fraudulent."
                        })
                        }
                    }
                ]
            },
            request=httpx.Request("POST", "https://test.example.com"),
        )

    monkeypatch.setattr(llm_service.httpx, "post", mock_post)

    result = llm_service.generate_explanation(
        sample_indicators,
        sample_risk_assessment,
    )

    assert "## Summary" in result
    assert "This message contains warning signs." in result
    assert "## Detected warning signs" in result
    assert "immediately" in result
    assert "Transfer $500" in result
    assert "## Recommended actions" in result
    assert "## Important limitation" in result


def test_generate_explanation_missing_configuration(
    monkeypatch,
    sample_indicators,
    sample_risk_assessment,
):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    monkeypatch.delenv("GROQ_MODEL", raising=False)

    with pytest.raises(llm_service.LLMServiceError):
        llm_service.generate_explanation(
            sample_indicators,
            sample_risk_assessment,
        )


def test_generate_explanation_timeout(
    monkeypatch,
    sample_indicators,
    sample_risk_assessment,
):
    monkeypatch.setenv("GROQ_API_KEY", "test-api-key")
    monkeypatch.setenv("GROQ_MODEL", "test-model")

    def mock_post(*args, **kwargs):
        raise httpx.TimeoutException("Request timed out")

    monkeypatch.setattr(llm_service.httpx, "post", mock_post)

    with pytest.raises(
        llm_service.LLMServiceError,
        match="timed out",
    ):
        llm_service.generate_explanation(
            sample_indicators,
            sample_risk_assessment,
        )


def test_generate_explanation_http_error(
    monkeypatch,
    sample_indicators,
    sample_risk_assessment,
):
    monkeypatch.setenv("GROQ_API_KEY", "test-api-key")
    monkeypatch.setenv("GROQ_MODEL", "test-model")

    def mock_post(*args, **kwargs):
        request = httpx.Request("POST", "https://test.example.com")

        response = httpx.Response(
            429,
            request=request,
        )

        raise httpx.HTTPStatusError(
            "Rate limit exceeded",
            request=request,
            response=response,
        )

    monkeypatch.setattr(llm_service.httpx, "post", mock_post)

    with pytest.raises(
        llm_service.LLMServiceError,
        match="HTTP 429",
    ):
        llm_service.generate_explanation(
            sample_indicators,
            sample_risk_assessment,
        )

@pytest.mark.parametrize(
    "indicator_explanations",
    [
        # Scenario 1: LLM invents additional evidence.
        [
            {
                "category": "urgency",
                "evidence": "immediately",
                "explanation": "The message creates urgency."
            },
            {
                "category": "transaction_request",
                "evidence": "Transfer $500",
                "explanation": "The message requests money."
            },
            {
                "category": "threats",
                "evidence": "account will be blocked",
                "explanation": "The message threatens account suspension."
            }
        ],

        # Scenario 2: LLM omits detected evidence.
        [
            {
                "category": "urgency",
                "evidence": "immediately",
                "explanation": "The message creates urgency."
            }
        ]
    ],
    ids=[
        "reject-invented-evidence",
        "reject-missing-evidence"
    ]
)
def test_generate_explanation_rejects_invalid_evidence(
    monkeypatch,
    sample_indicators,
    sample_risk_assessment,
    indicator_explanations,
):
    monkeypatch.setattr(
        llm_service,
        "GROQ_API_URL",
        "https://test.example.com",
    )
    monkeypatch.setenv("GROQ_API_KEY", "test-api-key")

    response_content = {
        "summary": "This message contains warning signs.",
        "indicator_explanations": indicator_explanations,
        "recommended_actions": [
            "Verify the request independently."
        ],
        "limitations": "These indicators do not prove fraud."
    }

    def mock_post(*args, **kwargs):
        return httpx.Response(
            200,
            json={
                "choices": [
                    {
                        "message": {
                            "content": json.dumps(response_content)
                        }
                    }
                ]
            },
            request=httpx.Request(
                "POST",
                "https://test.example.com",
            ),
        )

    monkeypatch.setattr(
        llm_service.httpx,
        "post",
        mock_post,
    )

    with pytest.raises(LLMServiceError):
        llm_service.generate_explanation(
            sample_indicators,
            sample_risk_assessment,
        )