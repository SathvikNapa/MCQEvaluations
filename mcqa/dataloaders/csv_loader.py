import pandas as pd

from mcqa.commons import logger
from mcqa.commons.regex import extract_regex
from mcqa.dataloaders.CsvColumns import CsvColumns
from mcqa.domain.input_parser import InputParser
from mcqa.domain.patterns import Patterns
from mcqa.domain.response_generator import LongContext

logger = logger.setup_logger()


class CsvLoader(InputParser):
    def handle_csv(self, file_path: str):
        csv_with_sources_df = pd.read_csv(file_path)

        requests = []
        for _, row in csv_with_sources_df.iterrows():
            if not pd.isna(row[CsvColumns.SOURCE_PATH]):
                question = row[CsvColumns.QUERY]
                option = extract_regex(row[CsvColumns.OPTIONS], pattern=Patterns.question_options_pattern),
                answer = row[CsvColumns.ANSWER]
                if row[CsvColumns.SHORT_CONTEXT]:
                    short_context = row[CsvColumns.SHORT_CONTEXT]
                else:
                    short_context = None

                source_path = row[CsvColumns.SOURCE_TYPE]
                source_type = row[CsvColumns.SOURCE_PATH]

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
