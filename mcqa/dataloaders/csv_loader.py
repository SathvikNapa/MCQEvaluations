import ast
import re

import pandas as pd

from mcqa.commons import logger
from mcqa.dataloaders.CsvColumns import CsvColumns
from mcqa.domain.input_parser import InputParser
from mcqa.domain.patterns import Patterns
from mcqa.domain.response_generator import LongContext

logger = logger.setup_logger()


class CsvLoader(InputParser):

    def _convert_string_list(self, cell):
        """Converts a CSV cell with string to a list of strings."""
        if isinstance(cell, str):
            try:
                return ast.literal_eval(cell.replace('\u200b', ''))
            except (ValueError, SyntaxError) as e:
                logger.debug(e)
        return cell

    def handle_csv(self, file_path: str):
        csv_with_sources_df = pd.read_csv(file_path)

        requests = []
        for _, row in csv_with_sources_df.iterrows():
            if pd.isna(row[CsvColumns.SOURCE_PATH]):
                continue
            question = row[CsvColumns.QUERY]
            option = re.findall(Patterns.question_options_pattern,
                                row[CsvColumns.OPTIONS].replace('\u200b', '').replace("'", "").replace(
                                    ']', '').replace(
                                    ",", ""))

            answer = row[CsvColumns.ANSWER].replace('\u200b', '').replace("'", '').strip()
            if not pd.isna(row[CsvColumns.SHORT_CONTEXT]):
                short_context = row[CsvColumns.SHORT_CONTEXT]
            else:
                short_context = None

            source_path = row[CsvColumns.SOURCE_PATH]
            file_type = row[CsvColumns.SOURCE_TYPE]

            requests.append(
                [
                    question,
                    option,
                    answer,
                    LongContext(file_type=file_type, link_or_text=source_path),
                    short_context
                ]
            )

        return requests
