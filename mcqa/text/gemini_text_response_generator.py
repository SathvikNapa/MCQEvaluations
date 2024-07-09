import google.generativeai as genai

from mcqa.domain.text_response_generator import TextResponseGenerator
from mcqa.text.config.gemini_text_config import GeminiTextConfig


class GeminiTextResponseGenerator(TextResponseGenerator):
    """A class used to generate text responses using the GeminiTextConfig.

    Attributes:
        gemini_config (GeminiTextConfig): Configuration for the Gemini text generator.
        llm_model (genai.GenerativeModel): The generative model used for text generation.
    """

    def __init__(self):
        """Initializes GeminiTextResponseGenerator with a GeminiTextConfig."""
        self.gemini_config = GeminiTextConfig()

    def start_llm(self):
        """Starts the LLM model.

        Configures genai with the Google API key from gemini_config and initializes the generative model.
        """
        genai.configure(api_key=self.gemini_config.google_api_key)
        self.llm_model = genai.GenerativeModel(self.gemini_config.text_generation_model)

    def generate_response(self, system_prompt, user_prompt):
        """Generates a response text.

        Args:
            system_prompt (str): The system prompt.
            user_prompt (str): The user prompt.

        Returns:
            str: The generated response text.
        """
        response = self.llm_model.generate_content([system_prompt, user_prompt])
        return response.text
