from dataclasses import dataclass
from typing import Protocol

from mcqa.domain.response_generator import GeneratorRequest


@dataclass
class McqaInterface(Protocol):
    """Protocol for MCQA interface."""

    request: GeneratorRequest

    def generate_query_response(self):
        """Generates a response for a given query.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError("generate_query_response method not implemented")
