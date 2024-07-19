from typing import Any

from mcqa.application.input_parser.image_parser import ImageParser
from mcqa.application.input_parser.pdf_parser import PdfParser
from mcqa.application.prompts import (
    MULTIMODAL_SYSTEM_PROMPT,
    MULTIMODAL_USER_PROMPT,
    REPHRASE_SYSTEM_PROMPT,
    REPHRASE_USER_PROMPT,
    SYNTHETIC_SYSTEM_PROMPT,
    SYNTHETIC_USER_PROMPT,
    SYSTEM_PROMPT,
    TEXT_USER_PROMPT,
    AnswerTemplate,
    ContextTemplate,
    NumberOfQuestionsTemplate,
    OptionsTemplate,
    QuestionTemplate, MULTIMODAL_SYNTHETIC_SYSTEM_PROMPT, MULTIMODAL_SYNTHETIC_USER_PROMPT, ShortContextTemplate,
)
from mcqa.domain.response_generator import LongContext


class PromptCrafter:
    """Class responsible for crafting prompts based on the given context, query, and options."""

    def __init__(self):
        """Initializes the PromptCrafter instance."""
        self.image_parser = ImageParser()
        self.pdf_parser = PdfParser()

    def craft_prompt(
            self,
            query: str,
            options: str,
            context: LongContext,
            answer: str,
            question_format: str,
            short_context: str
    ):
        """Crafts the appropriate prompt based on the context type and question format."""
        if context.file_type in ["image"]:
            if question_format == "rephrase":
                return self._craft_rephrase_prompt(query, options, answer, context)
            if question_format == "synthetic":
                return self._craft_synthetic_prompt(n_questions=5, query=query, options=options, answer=answer,
                                                    context=context, short_context=short_context)
            return self._craft_multimodal_prompt(context.link_or_text, query, options, short_context)

        elif context.file_type in ["pdf", "text"]:
            if question_format == "rephrase":
                return self._craft_rephrase_prompt(query, options, answer, context)
            if question_format == "synthetic":
                return self._craft_synthetic_prompt(
                    5, query, options, answer, context, short_context
                )
            return self._craft_text_based_prompt(
                context, query, options, short_context
            )

    def _craft_rephrase_prompt(self, query: str, options: str, answer: str, context: LongContext):
        """Crafts a rephrasing prompt."""
        if context.file_type in ["image"]:
            parsed_multimodal_object = self.image_parser.parse(file_path=context.link_or_text)
            question = QuestionTemplate.format(question_text=query)
            option = OptionsTemplate.format(option_text=options)
            answer = AnswerTemplate.format(answer=answer)
            user_prompt = REPHRASE_USER_PROMPT.format(
                question=question, option=option, answer=answer
            )
            return user_prompt, REPHRASE_SYSTEM_PROMPT, parsed_multimodal_object

        question = QuestionTemplate.format(question_text=query)
        option = OptionsTemplate.format(option_text=options)
        answer = AnswerTemplate.format(answer=answer)
        user_prompt = REPHRASE_USER_PROMPT.format(
            question=question, option=option, answer=answer
        )
        return user_prompt, REPHRASE_SYSTEM_PROMPT

    def _craft_text_based_prompt(
            self, context: LongContext, query: str, options: str, short_context: str
    ):
        """Crafts a text-based prompt for PDF or text context."""
        if context.file_type == "pdf":
            context_text = self.pdf_parser.parse(context.link_or_text)
        else:
            context_text = context.link_or_text

        question = QuestionTemplate.format(question_text=query)
        context = ContextTemplate.format(relevant_context=context_text)
        option = OptionsTemplate.format(option_text=options)
        short_context = ShortContextTemplate.format(short_context=short_context)

        user_prompt = TEXT_USER_PROMPT.format(
            question=question, option=option, context=context, short_context=short_context
        )
        return user_prompt, SYSTEM_PROMPT

    def _craft_multimodal_prompt(self, context_url: str, query: str, options: str, short_context: str):
        """Crafts a multimodal prompt for image context."""
        parsed_multimodal_object = self.image_parser.parse(file_path=context_url)
        question = QuestionTemplate.format(question_text=query)
        option = OptionsTemplate.format(option_text=options)
        short_context = ShortContextTemplate.format(short_context=short_context)
        user_prompt = MULTIMODAL_USER_PROMPT.format(question=question, option=option, short_context=short_context)
        return user_prompt, MULTIMODAL_SYSTEM_PROMPT, parsed_multimodal_object

    def _craft_synthetic_prompt(
            self, n_questions: int, query: str, options: str, answer: str, context: Any, short_context: str
    ):
        if context.file_type in ["text", "pdf"]:

            if context.file_type == "pdf":
                context_text = self.pdf_parser.parse(context.link_or_text)
            else:
                context_text = context.link_or_text

            """Crafts a synthetic prompt for generating multiple questions."""
            question = QuestionTemplate.format(question_text=query)
            option = OptionsTemplate.format(option_text=options)
            answer = AnswerTemplate.format(answer=answer)
            context = ContextTemplate.format(relevant_context=context_text)
            short_context = ShortContextTemplate.format(short_context=short_context)
            n_questions = NumberOfQuestionsTemplate.format(n_questions=n_questions)
            user_prompt = SYNTHETIC_USER_PROMPT.format(
                n_questions=n_questions,
                query=question,
                option=option,
                answer=answer,
                context=context,
                short_context=short_context,
            )
            return user_prompt, SYNTHETIC_SYSTEM_PROMPT

        if context.file_type in ["image"]:
            """Crafts a synthetic prompt for generating multiple questions."""
            parsed_multimodal_object = self.image_parser.parse(file_path=context.link_or_text)
            question = QuestionTemplate.format(question_text=query)
            option = OptionsTemplate.format(option_text=options)
            answer = AnswerTemplate.format(answer=answer)
            short_context = ShortContextTemplate.format(short_context=short_context)
            n_questions = NumberOfQuestionsTemplate.format(n_questions=n_questions)
            user_prompt = MULTIMODAL_SYNTHETIC_USER_PROMPT.format(
                n_questions=n_questions,
                query=question,
                option=option,
                answer=answer,
                short_context=short_context
            )
            return user_prompt, MULTIMODAL_SYNTHETIC_SYSTEM_PROMPT, parsed_multimodal_object
