from typing import Any

from mcqa.commons import logger
from mcqa.models.multimodal.gemini_multimodal_response_generator import GeminiMultimodalResponseGenerator
from mcqa.models.multimodal.openai_multimodal_response_generator import OpenaiMultimodalResponseGenerator
from mcqa.models.text.gemini_text_response_generator import GeminiTextResponseGenerator
from mcqa.models.text.openai_text_response_generator import OpenAITextResponseGenerator

logger = logger.setup_logger()


class LLMRouter:
    """Router class for selecting and interfacing with language models."""

    def __init__(self, text_model: str = None, multimodal_model: str = None):
        """Initializes the LLMRouter with the specified text and multimodal models.

        Args:
            text_model (str, optional): The name of the text model to use. Defaults to None.
            multimodal_model (str, optional): The name of the multimodal model to use. Defaults to None.
        """
        self.text_model = text_model
        self.multimodal_model = multimodal_model
        self._select_llm_model()

    def _select_llm_model(self):
        """Selects the appropriate LLM model based on the text model specified.

        Returns:
            object: An instance of the selected LLM model.
        """
        if self.text_model:
            if self.text_model == "gemini":
                self.llm_model = GeminiTextResponseGenerator()

            elif self.text_model == "openai":
                self.llm_model = OpenAITextResponseGenerator()
            else:
                raise ValueError(f"Unsupported text model: {self.text_model}")

        if self.multimodal_model:
            if self.multimodal_model == "gemini":
                self.llm_model = GeminiMultimodalResponseGenerator()
            elif self.multimodal_model == "openai":
                self.llm_model = OpenaiMultimodalResponseGenerator()
            else:
                raise ValueError(f"Unsupported multimodal model: {self.multimodal_model}")

    def start_model(self):
        """Starts the selected language model."""
        self.llm_model.start_llm()

    def generate_llm_response(self, system_prompt: str, user_prompt: str, multimodal_object: Any = None) -> Any:
        """Generates a response using the selected language model.

        Args:
            system_prompt (str): The system prompt to be used by the model.
            user_prompt (str): The user prompt to be used by the model.
            multimodal_object (Any): The multimodal object to be used by the model. Defaults to None.

        Returns:
            str: The generated response from the language model.
        """
        if self.multimodal_model:
            return self.llm_model.generate_multimodal_response(system_prompt, user_prompt, multimodal_object)

        if self.text_model:
            return self.llm_model.generate_response(system_prompt, user_prompt)
