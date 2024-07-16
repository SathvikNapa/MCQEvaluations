import os
from dataclasses import dataclass


@dataclass
class GeminiMultimodalConfig:
    google_api_key: str = os.environ.get("GOOGLE_API_KEY", None)
    multimodal_generation_model: str = "gemini-1.5-pro-latest"
    temperature: float = 0.01
