from dataclasses import dataclass
import os

@dataclass
class GeminiTextConfig:
    google_api_key: str = os.environ.get("GOOGLE_API_KEY")
    text_generation_model: str = "gemini-1.5-flash"
    temperature: float = 0.01
