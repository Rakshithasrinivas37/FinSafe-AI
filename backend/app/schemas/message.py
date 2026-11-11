from pydantic import BaseModel, Field, field_validator


class MessageAnalysisRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Message that needs to be analyzed"
    )

    jurisdiction: str | None = Field(
        default=None,
        description="Optional jursidiction or Country code"
    )

    @field_validator("message")
    @classmethod
    def validate_message(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Message cannot be empty")

        return value

class MessageAnalysisResponse(BaseModel):
    status: str
    message: str
    analysis: str