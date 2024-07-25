from dataclasses import dataclass


@dataclass
class CsvColumns:
    SOURCE_PATH = "source_path"
    QUERY = "Question"
    OPTIONS = "options"
    ANSWER = "Correct Answer"
    SHORT_CONTEXT = "Short_Context?"
    SOURCE_TYPE = "source_type"
