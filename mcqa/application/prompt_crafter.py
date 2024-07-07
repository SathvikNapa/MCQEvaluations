from mcqa.application.input_parser.image_parser import ImageParser
from mcqa.application.input_parser.pdf_parser import PdfParser
from mcqa.application.prompts import (
    ContextTemplate,
    QuestionTemplate,
    OptionsTemplate,
    MULTIMODAL_USER_PROMPT,
    MULTIMODAL_SYSTEM_PROMPT,
    TEXT_USER_PROMPT,
    SYSTEM_PROMPT
)
from mcqa.domain.response_generator import Context


class PromptCrafter:
    """Class responsible for crafting prompts based on the given context, query, and options."""

    def __init__(self, query: str, options: str, context: Context):
        """Initializes the PromptCrafter instance with query, options, and context.

        Args:
            query (str): The query string.
            options (str): The options string.
            context (Context): The context containing context type and context URL.
        """
        self.image_parser = ImageParser()
        self.pdf_parser = PdfParser()
        self.query = query
        self.context = context
        self.options = options

    def craft_prompt(self):
        """Crafts the appropriate prompt based on the context type.

        Returns:
            tuple: A tuple containing the user prompt and system prompt, and possibly the parsed multimodal object.
        """
        if self.context.context_type == "image":
            return self.craft_multimodal_prompt(
                context_url=self.context.context_url,
                query=self.query,
                options=self.options
            )
        if self.context.context_type == "pdf":
            return self.craft_text_prompt(
                context_url=self.context.context_url,
                query=self.query,
                options=self.options
            )

    def craft_text_prompt(self, context_url: str, query: str, options: str):
        """Crafts a text-based prompt for PDF context.

        Args:
            context_url (str): The URL or file path to the PDF context.
            query (str): The query string.
            options (str): The options string.

        Returns:
            tuple: A tuple containing the user prompt and system prompt.
        """
        pdf_text = self.pdf_parser.handle_pdf(file_path=context_url)
        context = ContextTemplate.format(relevant_context=pdf_text)
        question = QuestionTemplate.format(question_text=query)
        option = OptionsTemplate.format(option_text=options)
        user_prompt = TEXT_USER_PROMPT.format(question=question, option=option, context=context)
        return user_prompt, SYSTEM_PROMPT

    def craft_multimodal_prompt(self, context_url: str, query: str, options: str):
        """Crafts a multimodal prompt for image context.

        Args:
            context_url (str): The URL or file path to the image context.
            query (str): The query string.
            options (str): The options string.

        Returns:
            tuple: A tuple containing the user prompt, system prompt, and the parsed multimodal object.
        """
        parsed_multimodal_object = self.image_parser.parse(file_path=context_url)
        question = QuestionTemplate.format(question_text=query)
        option = OptionsTemplate.format(option_text=options)
        user_prompt = MULTIMODAL_USER_PROMPT.format(question=question, option=option)
        system_prompt = MULTIMODAL_SYSTEM_PROMPT
        return user_prompt, system_prompt, parsed_multimodal_object
