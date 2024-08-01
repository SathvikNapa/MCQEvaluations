import re
from typing import Any

from mcqa.base.input_parser.image_parser import ImageParser
from mcqa.base.input_parser.pdf_parser import PdfParser
from mcqa.base.prompts import (
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
    BASE_MULTIMODAL_USER_PROMPT, BASE_SYSTEM_PROMPT,
)


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
            full_context_path: str,
            answer: str,
            question_format: str,
            short_context: str
    ):
        """Crafts the appropriate prompt based on the context type and question format."""
        if re.search("|".join(['.pdf', '.png', '.jpeg', '.jpg']), full_context_path):
            if question_format == "naive":
                return self._craft_naive_prompt(query, options, answer,
                                                full_context_path, short_context)
            if question_format == "rephrase":
                return self._craft_rephrase_prompt(query, options, answer, full_context_path)
            if question_format == "synthetic":
                return self._craft_synthetic_prompt(n_questions=5, query=query, options=options, answer=answer,
                                                    full_context_path=full_context_path, short_context=short_context)
            return self._craft_multimodal_prompt(full_context_path, query, options, short_context)

        if "text" in full_context_path:
            if question_format == "rephrase":
                return self._craft_rephrase_prompt(query, options, answer, full_context_path)
            if question_format == "synthetic":
                return self._craft_synthetic_prompt(
                    5, query, options, answer, full_context_path, short_context
                )
            return self._craft_text_based_prompt(
                full_context_path, query, options, short_context
            )

    def _craft_naive_prompt(self, query: str, options: str,
                            answer: str, full_context_path: str, short_context: str):
        """Crafts the appropriate prompt based on the context type and question format.
        """
        user_prompt = BASE_MULTIMODAL_USER_PROMPT.format(question_text=query, option_text=options,
                                                         short_context=short_context)
        return user_prompt, BASE_SYSTEM_PROMPT

    def _craft_rephrase_prompt(self, query: str, options: str,
                               answer: str, full_context_path: str):
        """Crafts a rephrasing prompt."""
        question = QuestionTemplate.format(question_text=query)
        option = OptionsTemplate.format(option_text=options)
        answer = AnswerTemplate.format(answer=answer)
        user_prompt = REPHRASE_USER_PROMPT.format(
            question=question, option=option, answer=answer
        )
        return user_prompt, REPHRASE_SYSTEM_PROMPT

    def _craft_text_based_prompt(
            self, full_context_path: str, query: str, options: str, short_context: str
    ):
        """Crafts a text-based prompt for PDF or text context."""
        if '.pdf' in full_context_path:
            context_text = self.pdf_parser.parse(full_context_path)
        else:
            context_text = full_context_path

        question = QuestionTemplate.format(question_text=query)
        full_context_path = ContextTemplate.format(relevant_context=context_text)
        option = OptionsTemplate.format(option_text=options)
        short_context = ShortContextTemplate.format(short_context=short_context)

        user_prompt = TEXT_USER_PROMPT.format(
            question=question, option=option, context=full_context_path, short_context=short_context
        )
        return user_prompt, SYSTEM_PROMPT

    def _craft_multimodal_prompt(self, full_context_path: str, query: str, options: str, short_context: str):
        """Crafts a multimodal prompt for image context."""

        question = QuestionTemplate.format(question_text=query)
        option = OptionsTemplate.format(option_text=options)
        short_context = ShortContextTemplate.format(short_context=short_context)
        user_prompt = MULTIMODAL_USER_PROMPT.format(question=question, option=option, short_context=short_context)
        return user_prompt, MULTIMODAL_SYSTEM_PROMPT

    def _craft_synthetic_prompt(
            self, n_questions: int, query: str, options: str, answer: str, full_context_path: Any, short_context: str
    ):
        if not re.search("|".join(['.png', '.jpeg', '.jpg', '.pdf']), full_context_path):
            context_text = full_context_path

            """Crafts a synthetic prompt for generating multiple questions."""
            question = QuestionTemplate.format(question_text=query)
            option = OptionsTemplate.format(option_text=options)
            answer = AnswerTemplate.format(answer=answer)
            full_context_path = ContextTemplate.format(relevant_context=context_text)
            short_context = ShortContextTemplate.format(short_context=short_context)
            n_questions = NumberOfQuestionsTemplate.format(n_questions=n_questions)
            user_prompt = SYNTHETIC_USER_PROMPT.format(
                n_questions=n_questions,
                query=question,
                option=option,
                answer=answer,
                context=full_context_path,
                short_context=short_context,
            )
            return user_prompt, SYNTHETIC_SYSTEM_PROMPT

        if re.search("|".join(['.png', '.jpeg', '.jpg', '.pdf']), full_context_path):
            """Crafts a synthetic prompt for generating multiple questions."""
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
            return user_prompt, MULTIMODAL_SYNTHETIC_SYSTEM_PROMPT
