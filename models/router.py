from models.text.gemini_text_response_generator import GeminiTextResponseGenerator
from models.text.openai_text_response_generator import OpenAITextResponseGenerator


class Gateway:
    def __init__(self, text_model: str = None, multimodal_model: str = None):
        self.text_model = text_model
        self.multimodal_model = multimodal_model
        
        if text_model == "gemini":
            self.llm_model = GeminiTextResponseGenerator()
        
        if text_model == "openai":
            self.llm_model = OpenAITextResponseGenerator()
        
    def _start_models(self):
        self.llm_model.start_llm()

    def generate_llm_response(self, system_prompt, user_prompt):
        if not self.text_model:
            return self.llm_model.generate_response(system_prompt, user_prompt)

