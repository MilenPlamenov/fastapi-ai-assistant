from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=4000,
        examples=["Explain FastAPI"],
    )


class ChatResponse(BaseModel):
    response: str = Field(..., examples=["FastAPI is a modern Python web framework..."])
