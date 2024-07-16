import logging
import random
import re
import string

from mcqa.application.prompt_crafter import PromptCrafter
from mcqa.domain.patterns import Patterns
from mcqa.domain.question_formation import QuestionFormationInterface
from mcqa.domain.response_generator import Context

logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.DEBUG)


class QuestionFormation(QuestionFormationInterface):
    """Class for forming questions based on the given request."""

    def __init__(self):
        """Initializes the QuestionFormation."""
        self.prompt_crafter = PromptCrafter()

    def _extract_regex(self, text: str, pattern: str):
        """Extracts text using a given regex pattern."""
        return re.findall(pattern, text)

    def options_randomizer(self, options: str):
        """Randomizes the order of options."""
        split_options = self._extract_regex(options, Patterns.question_options_pattern)
        split_options = [re.sub(r"\s{2,}", repl="", string=options) for options in split_options]

        shuffled_cleansed = random.sample(split_options, len(split_options))
        return dict(zip(shuffled_cleansed,
                        [random.choice(string.ascii_uppercase) + ". " + re.sub(r'\s*[A-Z]\.\s*', repl="", string=option)
                         for
                         option in shuffled_cleansed]))

    def use_raw_question(
            self,
            query: str,
            options: str,
            context: Context,
            answer: str,
            question_format: str,
    ):
        """Uses a raw question as is."""
        options_dt = self.options_randomizer(options)
        options_text = "\n ".join(options_dt.values())
        logger.debug(options_dt)
        return self.prompt_crafter.craft_prompt(
            query, options=options_text, context=context, answer=options_dt[answer],
            question_format=question_format
        ), options_text, options_dt[answer]

    def create_synthetic_questions(
            self, query: str, options: str, context: Context, answer: str
    ):
        """Creates synthetic questions based on a given question."""
        options_dt = self.options_randomizer(options)
        options_text = "\n ".join(options_dt.values())
        return self.prompt_crafter.craft_prompt(
            query, options=options_text, context=context, answer=options_dt[answer],
            question_format="synthetic"
        ), options_text, options_dt[answer]

    def rephrase_question(
            self, query: str, options: str, context: Context, answer: str
    ):
        """Rephrases a question with the given options and answer."""
        options_dt = self.options_randomizer(options)
        options_text = "\n ".join(options_dt.values())
        return self.prompt_crafter.craft_prompt(
            query, options=options_text, context=context, answer=options_dt[answer],
            question_format="rephrase"
        ), options_text, options_dt[answer]
