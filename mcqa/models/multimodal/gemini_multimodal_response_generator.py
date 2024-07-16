from dataclasses import dataclass
from typing import Any

import google.generativeai as genai

from mcqa import logger
from mcqa.domain.multimodal_response_generator import MultimodalResponseGenerator
from mcqa.models.multimodal.config.gemini_multimodal_config import GeminiMultimodalConfig

logger = logger.setup_logger()


@dataclass
class GeminiMultimodalResponseGenerator(MultimodalResponseGenerator):
    """Class responsible for generating multimodal responses using the Gemini LLM model.

    This class inherits from the MultimodalResponseGenerator and implements its abstract methods.
    """

    def __init__(self):
        self.llm_model = None
        self.gemini_config = GeminiMultimodalConfig()

    def start_llm(self):
        """Starts the LLM (Language Learning Model) client.

        This function initializes the LLM client with the custom model specified in config.
        """
        logger.debug(f"Initiating {self.gemini_config.multimodal_generation_model} Multimodal model")
        self.llm_model = genai.GenerativeModel(self.gemini_config.multimodal_generation_model)

    def generate_multimodal_response(self, system_prompt: str, user_prompt: str,
                                     multimodal_object: Any, url: str = None) -> str:
        """Generates a multimodal response.

        This function generates a multimodal response using the system prompt, user prompt, and a multimodal object.

        Args:
            system_prompt (str): The system prompt.
            user_prompt (str): The user prompt.
            multimodal_object (Any): The multimodal object.
            url (str): The URL of the multimodal object.

        Returns:
            str: The generated response text.
        """

        parsed_multimodal_object = {"mime_type": "image/png", "data": multimodal_object}

        response = self.llm_model.generate_content(
            ([system_prompt, user_prompt, parsed_multimodal_object]))
        logger.debug(f"Generated response: {response.text}")
        return response.text
