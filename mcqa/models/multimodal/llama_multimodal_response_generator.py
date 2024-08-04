from dataclasses import dataclass
from typing import Any, List

import ollama

from mcqa.commons import logger
from mcqa.domain.multimodal_response_generator import \
    MultimodalResponseGenerator
from mcqa.models.multimodal.config.llama_multimodal_config import \
    LlamaMultimodalConfig

logger = logger.setup_logger()


@dataclass
class LlamaMultimodalResponseGenerator(MultimodalResponseGenerator):
    """Class responsible for generating multimodal responses using the Gemini LLM model.

    This class inherits from the MultimodalResponseGenerator and implements its abstract methods.
    """

    def __init__(self, model_name="llama3.1"):
        self.llm_model = model_name
        self.llama_config = LlamaMultimodalConfig()

    def start_llm(self):
        """Starts the LLM (Language Learning Model) client.

        This function initializes the LLM client with the custom model specified in config.
        """
        logger.info(f"Using {self.llama_config.multimodal_generation_model} model")

    def generate_multimodal_response(
        self,
        system_prompt: str,
        user_prompt: str,
        multimodal_objects: List[Any],
        url: str = None,
    ) -> str:
        """Generates a multimodal response.

        This function generates a multimodal response using the system prompt, user prompt, and a multimodal object.

        Args:
            system_prompt (str): The system prompt.
            user_prompt (str): The user prompt.
            multimodal_objects (Any): The multimodal object.
            url (str): The URL of the multimodal object.

        Returns:
            str: The generated response text.
        """

        prompt = system_prompt + user_prompt
        response = ollama.generate(
            self.llama_config.multimodal_generation_model,
            prompt,
            images=multimodal_objects,
        )
        logger.debug(f"Generated multimodal response: {response['response']}")
        return response["response"]
