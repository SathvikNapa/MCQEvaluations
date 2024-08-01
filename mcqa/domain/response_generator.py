from __future__ import annotations

from typing import Optional, List, Any

from pydantic import BaseModel


class RequestMetadata(BaseModel):
    """A class used to store request metadata."""

    temperature: float
    max_tokens: int


class ResponseMetadata(BaseModel):
    """A class used to store response metadata."""

    model: str


class Question(BaseModel):
    """A class used to define the structure of a generator request."""

    question: str
    options: List[str]
    answer: str
    question_format: str  # rephrase, raw, synthetic
    attachments: Optional[List] = []
    options_randomizer: Optional[bool] = None
    full_context_path: str
    question_context: Optional[str] = None


class QuestionResponse(BaseModel):
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


class QuestionsFromSourcesRequest(BaseModel):
    """A class used to define the structure of responses generator request."""

    file_type: str
    file_path: str
    output_path: str
    options_randomizer: Optional[bool] = None
    question_format: str  # rephrase, raw, synthetic


class ResponsesGeneratorResponse(BaseModel):
    """A class used to define the structure of responses generator response."""

    evaluation: float
    list_of_responses: list[QuestionResponse]


class RequestResponseLogs(BaseModel):
    """A class used to define the structure of a request response log."""

    request: Question
    response: ResponsesGeneratorResponse


class RequestResponseLog(BaseModel):
    """A class used to define the structure of a request response log."""

    request: Question
    response: QuestionResponse


class ExceptionLog(BaseModel):
    request: Any
    exception: Any
