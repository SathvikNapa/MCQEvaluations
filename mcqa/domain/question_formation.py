from typing import Any, Protocol, Tuple


class QuestionFormationInterface(Protocol):
    """Protocol for question formation strategies.

    This protocol defines the interface for classes that implement various strategies
    for question formation, including using raw questions, creating synthetic questions,
    and rephrasing questions.
    """

    def use_raw_question(
            self,
            query: str,
            options: str,
            full_context_path: str,
            answer: str,
            question_format: str,
            short_context: str
    ) -> Tuple[Any, Any]:
        """Uses a raw question as is.

        Args:
            question (str): The raw question to be used.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError("use_raw_question() is not implemented")

    def create_synthetic_questions(
            self, query: str, options: str, full_context_path: str, answer: str, short_context: str
    ) -> Tuple[Any, Any]:
        """Creates synthetic questions based on a given question.

        Args:
            question (str): The base question to create synthetic questions from.
            n (int): The number of synthetic questions to create.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError("create_synthetic_questions() is not implemented")

    def rephrase_question(
            self, query: str, options: str, full_context_path: str, answer: str
    ) -> Tuple[Any, Any]:
        """Rephrases a given question.

        Args:
            query (str): The question to be rephrased.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError("rephrase_question() is not implemented")
