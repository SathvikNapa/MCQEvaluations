import base64
from io import BytesIO

import google.generativeai as genai
import PyPDF2

from mcqa.commons.logger import setup_logger
from mcqa.domain.input_parser import InputParser

logger = setup_logger()


class PdfParser(InputParser):
    """A class used to parse PDF files.

    This class implements the InputParser protocol for PDF files.

    """

    def parse(self, file_path: str) -> str:
        """Parses a PDF file and extracts the text.

        Args:
            file_path (str): The path to the PDF file.

        Returns:
            str: The extracted text from the PDF file.
        """
        texts = []
        pdf_reader = PyPDF2.PdfReader(open(file_path, "rb"))

        num_pages = len(pdf_reader.pages)
        pdf_text = []
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            pdf_text.append(page.extract_text())
            pdf_text.append("\n\n\n")
        texts.append(pdf_text)

        return " ".join(texts[0])

    def _handle_pdf(self, file_path: str):
        bytes_ = BytesIO(file_path).getvalue()
        return base64.b64encode(bytes_).decode("utf-8")

    def upload_pdf(self, file_path: str):
        return genai.upload_file(file_path)
