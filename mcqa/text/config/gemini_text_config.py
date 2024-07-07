import os
from dataclasses import dataclass


@dataclass
class GeminiTextConfig:
    google_api_key: str = os.environ.get("GOOGLE_API_KEY", None)
    text_generation_model: str = "gemini-1.5-flash"
    temperature: float = 0.01
