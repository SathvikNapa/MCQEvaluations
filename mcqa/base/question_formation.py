import random
import re
import string
from typing import List

from mcqa.base.prompt_crafter import PromptCrafter
from mcqa.commons import logger
from mcqa.domain.question_formation import QuestionFormationInterface

logger = logger.setup_logger()


class QuestionFormation(QuestionFormationInterface):
    """Class for forming questions based on the given request."""

    def __init__(self):
        """Initializes the QuestionFormation."""
        self.prompt_crafter = PromptCrafter()

    def options_randomizer(self, options: List[str]):
        """Randomizes the order of options."""
        # split_options = self._extract_regex(options, Patterns.question_options_pattern)
        split_options = [
            re.sub(r"\s{2,}", "", option).replace("\n", "") for option in options
        ]
        shuffled_cleansed = random.sample(split_options, len(split_options))
        alphabet_sequence = random.sample(string.ascii_uppercase, len(split_options))

        shuffled_options = dict()
        for letter, option in zip(alphabet_sequence, shuffled_cleansed):
            new_option = letter + ". " + re.sub(r"\s*[A-J]\.\s*", " ", option)
            shuffled_options[new_option] = option

        return dict(
            zip(
                shuffled_cleansed,
                [
                    letter + ". " + re.sub(r"\s*[A-Z]\.\s*", "", option)
                    for letter, option in zip(alphabet_sequence, shuffled_cleansed)
                ],
            )
        )

    def use_raw_question(
        self,
        query: str,
        options: List[str],
        full_context_path: str,
        answer: str,
        question_format: str,
        short_context: str = None,
        options_randomizer: bool = False,
    ):
        """Uses a raw question as is."""
        if not options_randomizer:
            options_text = "\n ".join(options)
            return (
                self.prompt_crafter.craft_prompt(
                    query,
                    options=options_text,
                    full_context_path=full_context_path,
                    answer=answer,
                    question_format=question_format,
                    short_context=short_context,
                ),
                options_text,
                answer,
            )

        options_dt = self.options_randomizer(options)
        options_text = "\n ".join(options_dt.values())
        return (
            self.prompt_crafter.craft_prompt(
                query,
                options=options_text,
                full_context_path=full_context_path,
                answer=options_dt[answer],
                question_format=question_format,
                short_context=short_context,
            ),
            options_text,
            options_dt[answer],
        )

    def create_synthetic_questions(
        self,
        query: str,
        options: List[str],
        full_context_path: str,
        answer: str,
        short_context: str,
        options_randomizer: bool = False,
    ):
        """Creates synthetic questions based on a given question."""

        if not options_randomizer:
            options_text = "\n ".join(options)
            return (
                self.prompt_crafter.craft_prompt(
                    query,
                    options=options_text,
                    full_context_path=full_context_path,
                    answer=answer,
                    question_format="synthetic",
                    short_context=short_context,
                ),
                options_text,
                answer,
            )

        options_dt = self.options_randomizer(options)
        options_text = "\n ".join(options_dt.values())

        return (
            self.prompt_crafter.craft_prompt(
                query,
                options=options_text,
                full_context_path=full_context_path,
                answer=options_dt[answer],
                question_format="synthetic",
                short_context=short_context,
            ),
            options_text,
            options_dt[answer],
        )

    def rephrase_question(
        self,
        query: str,
        options: List[str],
        full_context_path: str,
        answer: str,
        short_context: str,
        options_randomizer: bool = False,
    ):
        """Rephrases a question with the given options and answer."""
        if not options_randomizer:
            options_text = "\n ".join(options)
            return (
                self.prompt_crafter.craft_prompt(
                    query,
                    options=options_text,
                    full_context_path=full_context_path,
                    answer=answer,
                    question_format="rephrase",
                    short_context=short_context,
                ),
                options_text,
                answer,
            )

        options_dt = self.options_randomizer(options)
        options_text = "\n ".join(options_dt.values())
        return (
            self.prompt_crafter.craft_prompt(
                query,
                options=options_text,
                full_context_path=full_context_path,
                answer=options_dt[answer],
                question_format="rephrase",
                short_context=short_context,
            ),
            options_text,
            options_dt[answer],
        )
