from mcqa.application.prompt_crafter import PromptCrafter
from mcqa.domain.question_formation import QuestionFormationInterface
from mcqa.domain.response_generator import Context


class QuestionFormation(QuestionFormationInterface):
    """Class for forming questions based on the given request."""

    def __init__(self):
        """Initializes the QuestionFormation."""
        self.prompt_crafter = PromptCrafter()

    def use_raw_question(
        self,
        query: str,
        options: str,
        context: Context,
        answer: str,
        question_format: str,
    ):
        """Uses a raw question as is."""
        return self.prompt_crafter.craft_prompt(
            query, options, context, answer, question_format
        )

    def create_synthetic_questions(
        self, query: str, options: str, context: Context, answer: str
    ):
        """Creates synthetic questions based on a given question."""
        return self.prompt_crafter.craft_prompt(
            query, options, context, answer, "synthetic"
        )

    def rephrase_question(
        self, query: str, options: str, context: Context, answer: str
    ):
        """Rephrases a question with the given options and answer."""
        return self.prompt_crafter.craft_prompt(
            query, options, context, answer, "rephrase"
        )
