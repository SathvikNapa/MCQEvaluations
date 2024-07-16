import os
from dataclasses import dataclass


@dataclass
class OpenaiMultimodalConfig:
    openai_api_key: str = os.environ.get("OPENAI_API_KEY", None)
    multimodal_generation_model: str = "gpt-4o"
    temperature: float = 0.01
