from mcqa.application.prompt_crafter import PromptCrafter
from mcqa.config import McqaConfig
from mcqa.domain.mcqa import McqaInterface
from mcqa.domain.response_generator import GeneratorRequest
from mcqa.llm_router import LLMRouter


class Mcqa(McqaInterface):
    """Class to handle MCQA (Multiple Choice Question Answering) operations."""

    def __init__(self, request: GeneratorRequest):
        """Initializes the Mcqa instance with the given request.

        Args:
            request (GeneratorRequest): The generator request containing query, options, and context.
        """
        self.mcqa_config = McqaConfig()
        self.request = request
        self.prompt_crafter = PromptCrafter(
            query=self.request.query,
            options=self.request.options,
            context=self.request.context
        )

    def generate_query_response(self):
        """Generates a response for the given query based on the context type.

        Returns:
            str: The generated response from the LLM.
        """
        if self.request.context.context_type == "pdf":
            llm_router = LLMRouter(text_model=self.mcqa_config.text_model)
            user_prompt, system_prompt = self.prompt_crafter.craft_prompt()
            llm_router.start_model()
            return llm_router.generate_llm_response(
                system_prompt=system_prompt,
                user_prompt=user_prompt
            )
