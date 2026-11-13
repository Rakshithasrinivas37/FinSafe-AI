import json
import os
from collections import Counter

import httpx
from dotenv import load_dotenv

from backend.app.schemas.indicators import DetectedIndicator
from backend.app.schemas.llm import LLMExplanation
from backend.app.schemas.risk import RiskAssessment
from backend.app.services.llm.prompts import (
    SYSTEM_PROMPT,
    USER_PROMPT_TEMPLATE,
)

load_dotenv()

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
REQUEST_TIMEOUT = 30.0


class LLMServiceError(Exception):
    """Raised when the LLM service cannot generate an explanation."""


def generate_explanation(
    indicators: list[DetectedIndicator],
    risk_assessment: RiskAssessment,
) -> str:
    """Generate an explanation using the existing detection results."""

    api_key = os.getenv("GROQ_API_KEY")
    model = "openai/gpt-oss-120b"

    if not api_key or not model:
        raise LLMServiceError(
            "LLM configuration is missing. Check GROQ_API_KEY and GROQ_MODEL."
        )

    indicator_data = [
        indicator.model_dump()
        for indicator in indicators
    ]

    user_prompt = USER_PROMPT_TEMPLATE.format(
        risk_level=risk_assessment.risk_level,
        indicators=json.dumps(indicator_data, indent=2),
    )

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.2,
        "max_tokens": 800,
        "top_p": 0.9,
        "response_format": {
        "type": "json_object"
        },
    }

    try:
        response = httpx.post(
            GROQ_API_URL,
            headers=headers,
            json=payload,
            timeout=REQUEST_TIMEOUT,
        )

        try:
            response_data = response.json()
        except ValueError as exc:
            raise LLMServiceError(
                "The LLM provider returned a non-JSON response."
            ) from exc

        if not isinstance(response_data, dict):
            raise LLMServiceError(
                "The LLM provider returned an unexpected response format."
            )

        choices = response_data.get("choices")

        if not isinstance(choices, list) or not choices:
            raise LLMServiceError(
                f"The LLM provider returned no choices. "
                f"Response keys: {list(response_data.keys())}"
            )

        choice = choices[0]
        message = choice.get("message", {})

        if not isinstance(message, dict):
            raise LLMServiceError(
                "The LLM provider returned an invalid message structure."
            )

        content = message.get("content")

        if not isinstance(content, str) or not content.strip():
            finish_reason = choice.get("finish_reason")

            raise LLMServiceError(
                f"The LLM provider returned empty content. "
                f"Finish reason: {finish_reason}"
            )

        try:
            parsed_content = json.loads(content)
            explanation = LLMExplanation.model_validate(parsed_content)
            expected_evidence = Counter(
                (indicator.category, indicator.matched_text)
                for indicator in indicators
            )

            returned_evidence = Counter(
                (item.category, item.evidence)
                for item in explanation.indicator_explanations
            )

            if expected_evidence != returned_evidence:
                raise LLMServiceError(
                    "The LLM returned evidence that does not match "
                    "the detected indicators."
                )
        except (json.JSONDecodeError, ValueError) as exc:
            raise LLMServiceError(
                "The LLM returned an invalid structured explanation."
            ) from exc

        return render_explanation(explanation, indicators)

    except httpx.TimeoutException as exc:
        raise LLMServiceError(
            "The LLM request timed out."
        ) from exc

    except httpx.HTTPStatusError as exc:
        raise LLMServiceError(
            f"The LLM provider returned HTTP {exc.response.status_code}."
        ) from exc

    except httpx.RequestError as exc:
        raise LLMServiceError(
            "Unable to connect to the LLM provider."
        ) from exc

    except (KeyError, IndexError, ValueError) as exc:
        raise LLMServiceError(
            "The LLM provider returned an invalid response."
        ) from exc

def render_explanation(
    explanation: LLMExplanation,
    indicators: list[DetectedIndicator],
) -> str:
    """Render the explanation using original Python-detected evidence."""

    original_evidence = {
        (indicator.category, indicator.matched_text): indicator.matched_text
        for indicator in indicators
    }

    sections = [
        f"## Summary\n\n{explanation.summary}"
    ]

    if explanation.indicator_explanations:
        indicator_section = ["## Detected warning signs"]

        for item in explanation.indicator_explanations:
            evidence = original_evidence[
                (item.category, item.evidence)
            ]

            indicator_section.append(
                f"### {item.category.replace('_', ' ').title()}\n\n"
                f"**Evidence:** {evidence}\n\n"
                f"{item.explanation}"
            )

        sections.append("\n\n".join(indicator_section))

    if explanation.recommended_actions:
        actions = "\n".join(
            f"{index}. {action}"
            for index, action in enumerate(
                explanation.recommended_actions,
                start=1,
            )
        )

        sections.append(
            f"## Recommended actions\n\n{actions}"
        )

    sections.append(
        f"## Important limitation\n\n{explanation.limitations}"
    )

    return "\n\n".join(sections)