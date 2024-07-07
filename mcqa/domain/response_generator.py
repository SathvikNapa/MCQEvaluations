from typing import Optional

from pydantic import BaseModel


class RequestMetadata(BaseModel):
    """A class used to store request metadata."""

    temperature: float
    max_tokens: int


class ResponseMetadata(BaseModel):
    """A class used to store response metadata."""

    model: str


class Context(BaseModel):
    """A class used to store context."""

    context_type: str
    context_url: Optional[str] = None


class GeneratorRequest(BaseModel):
    """A class used to define the structure of a generator request."""

    query: str
    options: str
    context: Context


class GeneratorResponse(BaseModel):
    """A class used to define the structure of a generator response."""

    response: str
    metadata: ResponseMetadata
