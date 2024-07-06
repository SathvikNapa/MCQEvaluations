from dataclasses import dataclass
import os

@dataclass
class OpenAITextConfig:
    openai_api_key: str = os.environ.get("OPENAI_API_KEY", None)
    text_generation_model: str = "gpt-4o"
    temperature: float = 0.001
