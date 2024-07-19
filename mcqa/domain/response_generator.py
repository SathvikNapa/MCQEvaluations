from __future__ import annotations

from typing import Optional, List

from pydantic import BaseModel


class RequestMetadata(BaseModel):
    """A class used to store request metadata."""

    temperature: float
    max_tokens: int


class ResponseMetadata(BaseModel):
    """A class used to store response metadata."""

    model: str


class LongContext(BaseModel):
    """A class used to store context."""

    file_type: str
    link_or_text: Optional[str] = None


class Question(BaseModel):
    """A class used to define the structure of a generator request."""

    query: str
    options: List[str]
    answer: str
    question_format: str  # rephrase, raw, synthetic
    long_context: LongContext
    short_context: Optional[str] = None


class ResponseGeneratorResponse(BaseModel):
    """A class used to define the structure of a generator response."""

    generated_answer: str
    actual_answer: str
    question: str
    options: str
    evaluation: float
    excerpts: str
    thinking: str
    foundational_knowledge: str
    metadata: ResponseMetadata


class ResponsesGeneratorRequest(BaseModel):
    """A class used to define the structure of responses generator request."""

    file_type: str
    file_path: str
    question_format: str  # rephrase, raw, synthetic


class ResponsesGeneratorResponse(BaseModel):
    """A class used to define the structure of responses generator response."""

    evaluation: float
    list_of_responses: list[ResponseGeneratorResponse]


class RequestResponseLogs(BaseModel):
    """A class used to define the structure of a request response log."""

    request: Question
    response: ResponsesGeneratorResponse

# class RequestResponseLog(BaseModel):
#     """A class used to define the structure of a request response log."""
#
#     request: ResponseGeneratorRequest
#     response: ResponseGeneratorResponse
