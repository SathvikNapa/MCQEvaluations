from dataclasses import dataclass
from typing import Any

from openai import OpenAI

from mcqa.commons import logger
from mcqa.domain.multimodal_response_generator import MultimodalResponseGenerator
from mcqa.models.multimodal.config.openai_multimodal_config import OpenaiMultimodalConfig

logger = logger.setup_logger()


@dataclass
class OpenaiMultimodalResponseGenerator(MultimodalResponseGenerator):
    """Class responsible for generating multimodal responses using the Gemini LLM model.

    This class inherits from the MultimodalResponseGenerator and implements its abstract methods.
    """

    def __init__(self):
        self.llm_model = None
        self.openai_config = OpenaiMultimodalConfig()

    def start_llm(self):
        """Starts the LLM (Language Learning Model) client.

        This function initializes the LLM client with the custom model specified in config.
        """
        logger.debug(f"Initiating {self.openai_config.openai_api_key} Multimodal model")
        self.llm_model = OpenAI(api_key=self.openai_config.openai_api_key)

    def generate_multimodal_response(self, system_prompt: str, user_prompt: str,
                                     multimodal_object: Any, url: str = None) -> str:
        """Generates a multimodal response.

        This function generates a multimodal response using the system prompt, user prompt, and a multimodal object.

        Args:
            system_prompt (str): The system prompt.
            user_prompt (str): The user prompt.
            multimodal_object (Any): The multimodal object.
            url (str): The URL of the multimodal object

        Returns:
            str: The generated response text.
        """
        logger.debug(f"Multimodal object: {multimodal_object}")
        response = self.llm_model.chat.completions.create(
            model=self.openai_config.multimodal_generation_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": [
                    {"type": "text", "text": user_prompt},
                    {"type": "image_url", "image_url": {
                        "url": f"data:image/png;base64,{multimodal_object}"}
                     }
                ]}
            ],
            temperature=self.openai_config.temperature,
        )
        logger.debug(f"Generated response: {response.text}")
        return response.choices[0].message.content
