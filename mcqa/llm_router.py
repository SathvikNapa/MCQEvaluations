from mcqa.text.gemini_text_response_generator import GeminiTextResponseGenerator
from mcqa.text.openai_text_response_generator import OpenAITextResponseGenerator


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
        if self.text_model == "gemini":
            self.llm_model = GeminiTextResponseGenerator()
        elif self.text_model == "openai":
            self.llm_model = OpenAITextResponseGenerator()
        else:
            raise ValueError(f"Unsupported text model: {self.text_model}")

    def start_model(self):
        """Starts the selected language model."""
        self.llm_model.start_llm()

    def generate_llm_response(self, system_prompt: str, user_prompt: str) -> str:
        """Generates a response using the selected language model.

        Args:
            system_prompt (str): The system prompt to be used by the model.
            user_prompt (str): The user prompt to be used by the model.

        Returns:
            str: The generated response from the language model.
        """
        if self.text_model:
            return self.llm_model.generate_response(system_prompt, user_prompt)
