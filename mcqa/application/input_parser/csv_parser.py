import logging

import pandas as pd

from mcqa.domain.input_parser import InputParser
from mcqa.domain.response_generator import Context

logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.DEBUG)


class CsvParser(InputParser):
    def handle_csv(self, file_path: str):
        csv_with_sources_df = pd.read_csv(file_path)

        requests = []
        for _, row in csv_with_sources_df.iterrows():
            if not pd.isna(row["source_path"]):
                question = row["Question"]
                option = row["All Answers"]
                answer = row["Correct Answer"]
                source_type = row["source_type"]
                source_path = row["source_path"]

                requests.append(
                    [
                        question,
                        option,
                        answer,
                        Context(context_type=source_type, link_or_text=source_path),
                    ]
                )

                # requests.append(
                #     ResponseGeneratorRequest(query=question, options=option, answer=answer, question_format='raw',
                #                              context=Context(context_type=source_type, link_or_text=source_path)))

        return requests
