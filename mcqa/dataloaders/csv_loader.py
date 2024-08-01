import ast
import re

import pandas as pd
from tqdm import tqdm

from mcqa.commons import logger
from mcqa.dataloaders.CsvColumns import CsvColumns
from mcqa.domain.input_parser import InputParser
from mcqa.domain.patterns import Patterns

logger = logger.setup_logger()


class CsvLoader(InputParser):
    def __init__(self, options_randomizer: bool):
        self.options_randomizer = options_randomizer

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
        for _, row in tqdm(csv_with_sources_df.iterrows()):

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
                # short_context = None
            else:
                short_context = None

            full_context_path = row[CsvColumns.SOURCE_PATH]

            requests.append(
                [
                    question,
                    option,
                    answer,
                    full_context_path,
                    short_context,
                    self.options_randomizer,
                ]
            )

        return requests
