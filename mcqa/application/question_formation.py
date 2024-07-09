from mcqa.application.prompt_crafter import PromptCrafter
from mcqa.domain.question_formation import QuestionFormationInterface


class QuestionFormation(QuestionFormationInterface):
    """Class for forming questions based on the given request."""

    def __init__(self, request):
        """Initializes the QuestionFormation with the given request.

        Args:
            request: The request containing query, options, context, answer, and question format.
        """
        self.request = request
        self.prompt_crafter = PromptCrafter(
            query=self.request.query,
            options=self.request.options,
            context=self.request.context,
            answer=self.request.answer,
            question_format=self.request.question_format,
        )

    def use_raw_question(self, question: str):
        """Uses a raw question as is.

        Args:
            question (str): The raw question to be used.

        Returns:
            tuple: A tuple containing the user prompt and system prompt.
        """
        user_prompt, system_prompt = self.prompt_crafter.craft_prompt()
        return user_prompt, system_prompt

    def create_synthetic_questions(self, question: str, answer: str, context: str):
        """Creates synthetic questions based on a given question.

        Args:
            question (str): The base question to create synthetic questions from.
            answer (str): The answer to the base question.
            context (str): The context for the base question.

        Returns:
            tuple: A tuple containing the user prompt and system prompt.
        """
        user_prompt, system_prompt = self.prompt_crafter.craft_prompt()
        return user_prompt, system_prompt

    def rephrase_question(self, question: str, options: str, answer: str):
        """Rephrases a question with the given options and answer.

        Args:
            question (str): The question to be rephrased.
            options (str): The options for the question.
            answer (str): The answer to the question.

        Returns:
            tuple: A tuple containing the user prompt and system prompt.
        """
        user_prompt, system_prompt = self.prompt_crafter.craft_prompt()
        return user_prompt, system_prompt
