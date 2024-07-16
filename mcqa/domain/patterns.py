import re
from dataclasses import dataclass


@dataclass
class Patterns:
    answer = r"<Answer>(.*?)</Answer>"
    excerpts = r"<RelevantExcerpts>(.*?)</RelevantExcerpts>"
    thinking = r"<Thinking>(.*?)</Thinking>"
    foundational_knowledge = "<FoundationalKnowledge>(.*?)</FoundationalKnowledge>"

    question_pattern = re.compile(r"<Question>\s*(.*?)\s*</Question>", re.DOTALL)
    options_pattern = re.compile(r"<Options>\s*(.*?)\s*</Options>", re.DOTALL)
    answer_pattern = re.compile(r"<Answer>\s*(.*?)\s*</Answer>", re.DOTALL)
    question_options_pattern = re.compile(r"([A-Z]\.\s.*?(?=\s[A-Z]\.|$))", re.DOTALL)
