from dataclasses import dataclass


@dataclass
class LlamaMultimodalConfig:
    multimodal_generation_model: str = "llama3.1"
    temperature: float = 0.01
