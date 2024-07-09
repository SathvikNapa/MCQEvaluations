from mcqa.application.input_parser.image_parser import ImageParser
from mcqa.application.input_parser.pdf_parser import PdfParser
from mcqa.application.prompts import (
    ContextTemplate,
    QuestionTemplate,
    OptionsTemplate,
    MULTIMODAL_USER_PROMPT,
    MULTIMODAL_SYSTEM_PROMPT,
    TEXT_USER_PROMPT,
    SYSTEM_PROMPT,
    AnswerTemplate,
    REPHRASE_USER_PROMPT,
    REPHRASE_SYSTEM_PROMPT,
    SYNTHETIC_USER_PROMPT,
    NumberOfQuestionsTemplate,
    SYNTHETIC_SYSTEM_PROMPT,
)
from mcqa.domain.response_generator import Context


class PromptCrafter:
    """Class responsible for crafting prompts based on the given context, query, and options."""

    def __init__(
        self,
        query: str,
        options: str,
        context: Context,
        answer: str,
        question_format: str,
    ):
        """Initializes the PromptCrafter instance with query, options, context, answer, and question format.

        Args:
            query (str): The query string.
            options (str): The options string.
            context (Context): The context containing context type and context URL.
            answer (str): The answer string.
            question_format (str): The format of the question (e.g., rephrase, synthetic).
        """
        self.image_parser = ImageParser()
        self.pdf_parser = PdfParser()
        self.query = query
        self.context = context
        self.options = options
        self.answer = answer
        self.question_format = question_format
        self.context_text = None

    def craft_prompt(self):
        """Crafts the appropriate prompt based on the context type and question format.

        Returns:
            tuple: A tuple containing the user prompt and system prompt, and possibly the parsed multimodal object.
        """
        if self.context.context_type == "image":
            return self.craft_multimodal_prompt(
                context_url=self.context.link_or_text,
                query=self.query,
                options=self.options,
            )
        if self.context.context_type in ["pdf", "text"]:
            if self.question_format == "rephrase":
                return self.craft_rephrase_prompt(
                    query=self.query, options=self.options, answer=self.answer
                )
            if self.question_format == "synthetic":
                return self.craft_synthetic_prompt(
                    n_questions=5,
                    query=self.query,
                    options=self.options,
                    answer=self.answer,
                    context=self.context.link_or_text,
                )
            return self.craft_text_prompt(
                link_or_text=self.context.link_or_text,
                query=self.query,
                options=self.options,
            )

    def craft_text_prompt(self, link_or_text: str, query: str, options: str):
        """Crafts a text-based prompt for PDF or text context.

        Args:
            link_or_text (str): The URL or file path to the context.
            query (str): The query string.
            options (str): The options string.

        Returns:
            tuple: A tuple containing the user prompt and system prompt.
        """
        if self.context.context_type == "pdf":
            self.context_text = self.pdf_parser.handle_pdf(file_path=link_or_text)
        elif self.context.context_type == "text":
            self.context_text = link_or_text

        context = ContextTemplate.format(relevant_context=self.context_text)
        question = QuestionTemplate.format(question_text=query)
        option = OptionsTemplate.format(option_text=options)

        user_prompt = TEXT_USER_PROMPT.format(
            question=question, option=option, context=context
        )
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

    def craft_rephrase_prompt(self, query: str, options: str, answer: str):
        """Crafts a rephrasing prompt for the given context.

        Args:
            query (str): The query string.
            options (str): The options string.
            answer (str): The answer string.

        Returns:
            tuple: A tuple containing the user prompt and system prompt.
        """
        question = QuestionTemplate.format(question_text=query)
        option = OptionsTemplate.format(option_text=options)
        answer = AnswerTemplate.format(answer=answer)
        user_prompt = REPHRASE_USER_PROMPT.format(
            question=question, option=option, answer=answer
        )
        return user_prompt, REPHRASE_SYSTEM_PROMPT

    def craft_synthetic_prompt(
        self, n_questions: int, query: str, options: str, answer: str, context: str
    ):
        """Crafts a synthetic prompt for generating multiple questions.

        Args:
            n_questions (int): The number of synthetic questions to generate.
            query (str): The query string.
            options (str): The options string.
            answer (str): The answer string.
            context (str): The context string.

        Returns:
            tuple: A tuple containing the user prompt and system prompt.
        """
        question = QuestionTemplate.format(question_text=query)
        option = OptionsTemplate.format(option_text=options)
        answer = AnswerTemplate.format(answer=answer)
        context = ContextTemplate.format(relevant_context=context)
        n_questions = NumberOfQuestionsTemplate.format(n_questions=n_questions)
        user_prompt = SYNTHETIC_USER_PROMPT.format(
            n_questions=n_questions,
            query=question,
            option=option,
            answer=answer,
            context=context,
        )
        return user_prompt, SYNTHETIC_SYSTEM_PROMPT
