from dataclasses import dataclass


@dataclass
class TextResponseGenerator:
    """A class used to generate text responses."""

    def start_llm(self):
        """Creates an llm client.

        This function should be overridden in a subclass. It is expected to create an llm client.

        Raises:
            NotImplementedError: If the function is not implemented in a subclass.
        """
        raise NotImplementedError("create_llm_client is not implemented")

    def generate_text_response(self):
        """Generates a text response.

        This function should be overridden in a subclass. It is expected to generate a text response.

        Raises:
            NotImplementedError: If the function is not implemented in a subclass.
        """
        raise NotImplementedError("generate_text_response is not implemented")
