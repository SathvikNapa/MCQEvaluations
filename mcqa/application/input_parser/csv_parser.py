import pandas as pd

from mcqa import logger
from mcqa.domain.input_parser import InputParser
from mcqa.domain.response_generator import LongContext

logger = logger.setup_logger()


class CsvParser(InputParser):
    def handle_csv(self, file_path: str):
        csv_with_sources_df = pd.read_csv(file_path)

        requests = []
        for _, row in csv_with_sources_df.iterrows():
            if not pd.isna(row["source_path"]):
                question = row["Question"]
                option = row["All Answers"]
                answer = row["Correct Answer"]
                if row['Short_Context?']:
                    short_context = row['Short_Context?']
                else:
                    short_context = None

                source_type = row["source_type"]
                source_path = row["source_path"]

                requests.append(
                    [
                        question,
                        option,
                        answer,
                        LongContext(context_type=source_type, link_or_text=source_path),
                        short_context
                    ]
                )

        return requests
