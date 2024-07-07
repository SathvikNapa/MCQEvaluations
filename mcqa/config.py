import os
from dataclasses import dataclass


@dataclass
class McqaConfig:
    """Configuration class for MCQA."""

    text_model: str = os.environ.get("TEXT_MODEL", "gemini")
