from dataclasses import dataclass
from typing import Any


@dataclass
class MultimodalResponseGenerator:
    """Class responsible for generating multimodal responses.

    This class should be subclassed and the methods `start_llm` and
    `generate_multimodal_response` should be implemented in the subclass.
    """

    def start_llm(self):
        """Creates an LLM (Language Learning Model) client.

        This function should be overridden in a subclass. It is expected to create an LLM client.

        Raises:
            NotImplementedError: If the function is not implemented in a subclass.
        """
        raise NotImplementedError("start_llm is not implemented")

    def generate_multimodal_response(
        self,
        system_prompt: str,
        user_prompt: str,
        multimodal_object: Any,
        url: str = None,
    ):
        """Generates a multimodal response.

        This function should be overridden in a subclass. It is expected to generate a multimodal response.

        Raises:
            NotImplementedError: If the function is not implemented in a subclass.
        """
        raise NotImplementedError("generate_multimodal_response is not implemented")
