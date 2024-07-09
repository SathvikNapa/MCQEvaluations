from openai import OpenAI

from mcqa.domain.text_response_generator import TextResponseGenerator
from mcqa.text.config.openai_text_config import OpenAITextConfig


class OpenAITextResponseGenerator(TextResponseGenerator):
    """A class used to generate text responses using the OpenAITextConfig.

    Attributes:
        openai_config (OpenAITextConfig): Configuration for the OpenAI text generator.
        llm_model (OpenAI): The OpenAI model used for text generation.
    """

    def __init__(self):
        """Initializes OpenAITextResponseGenerator with an OpenAITextConfig."""
        self.openai_config = OpenAITextConfig()

    def start_llm(self):
        """Starts the LLM model.

        Configures the OpenAI model with the OpenAI API key and temperature from openai_config.
        """
        self.llm_model = OpenAI(api_key=self.openai_config.openai_api_key)

    def generate_response(self, system_prompt, user_prompt):
        """Generates a response text.

        Args:
            system_prompt (str): The system prompt.
            user_prompt (str): The user prompt.

        Returns:
            str: The generated response text.
        """
        response = self.llm_model.chat.completions.create(
            model=self.openai_config.text_generation_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ])
        return response.choices[0].message.content
