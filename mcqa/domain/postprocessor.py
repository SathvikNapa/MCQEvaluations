from typing import Protocol


class PostProcessorInterface(Protocol):
    """Interface for post-processing data."""

    def postprocess(self, generated_response: str, actual_answer: str, question: str):
        """Post-processes the given data.

        Args:
            data: The data to be post-processed.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError("postprocess() is not implemented")
