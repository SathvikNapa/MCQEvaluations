from typing import Protocol, Any


class InputParser(Protocol):
    """Protocol for input parsers.

    This class defines the protocol for classes that implement the parsing of input files.

    """

    def parse(self, file_path: str) -> Any:
        """Parses an input file.

        This function should be overridden in a subclass. It is expected to parse an input file.

        Args:
            file_path (str): The path to the input file.

        Returns:
            Any: The result of parsing the file.

        Raises:
            NotImplementedError: If the function is not implemented in a subclass.
        """
        raise NotImplementedError("parse() is not implemented")
